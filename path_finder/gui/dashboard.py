import streamlit as st
import pandas as pd
import time
import os
import sys

# Try importing with the package structure first, fall back to local imports
try:
    from path_finder.gui.input_form import InputForm
    from path_finder.gui.map_visualization import MapVisualization
    from path_finder.api.geocoding import GeocodingAPI
    from path_finder.api.distance_matrix import DistanceMatrixAPI
    from path_finder.utils.graph import GraphBuilder
    from path_finder.utils.comparison import AlgorithmComparison
    from path_finder.utils.export import ExportManager
    from path_finder.algorithms.genetic_algorithm import GeneticAlgorithm
    from path_finder.algorithms.a_star import AStar
    from path_finder.algorithms.q_learning import QLearning
except ImportError:
    # Local imports for standalone version
    from gui.input_form import InputForm
    from gui.map_visualization import MapVisualization
    from api.geocoding import GeocodingAPI
    from api.distance_matrix import DistanceMatrixAPI
    from utils.graph import GraphBuilder
    from utils.comparison import AlgorithmComparison
    from utils.export import ExportManager
    from algorithms.genetic_algorithm import GeneticAlgorithm
    from algorithms.a_star import AStar
    from algorithms.q_learning import QLearning

class Dashboard:
    def __init__(self):
        """Initialize the main dashboard for the Streamlit app."""
        self.input_form = InputForm()
        self.map_vis = MapVisualization()
        self.geocoding_api = GeocodingAPI()
        self.distance_api = DistanceMatrixAPI()
        self.graph_builder = None
        self.comparison = AlgorithmComparison()
        self.export_manager = ExportManager()
        
        # Initialize algorithm instances to None
        self.ga_instance = None
        self.astar_instance = None
        self.ql_instance = None
        
        # Initialize session state if not already done
        if 'addresses' not in st.session_state:
            st.session_state.addresses = []
        if 'locations_df' not in st.session_state:
            st.session_state.locations_df = pd.DataFrame()
        if 'distances' not in st.session_state:
            st.session_state.distances = None
        if 'durations' not in st.session_state:
            st.session_state.durations = None
        if 'algorithm_results' not in st.session_state:
            st.session_state.algorithm_results = []
        if 'comparison_df' not in st.session_state:
            st.session_state.comparison_df = pd.DataFrame()
    
    def run(self):
        """Run the main dashboard application."""
        st.title("Path Finder - AI-Powered Delivery Route Optimization")
        
        # Render input form and get addresses
        addresses = self.input_form.render()
        
        if addresses and addresses != st.session_state.addresses:
            # Reset state if addresses change
            st.session_state.addresses = addresses
            st.session_state.locations_df = pd.DataFrame()
            st.session_state.distances = None
            st.session_state.durations = None
            st.session_state.algorithm_results = []
            st.session_state.comparison_df = pd.DataFrame()
        
        # Get algorithm parameters
        algorithm_params = self.input_form.get_algorithm_params()
        
        # Process data and run algorithms if addresses are available
        if st.session_state.addresses:
            self._process_data()
            
            # Run algorithms if locations are available
            if not st.session_state.locations_df.empty:
                # Button to run selected algorithms
                if st.button("Run Selected Algorithms"):
                    self._run_algorithms(algorithm_params)
                
                # Display results if available
                self._display_results()
    
    def _process_data(self):
        """Process input addresses to get location data and distance matrix."""
        # Add detailed error logging
        try:
            # Geocoding step
            if st.session_state.locations_df.empty:
                with st.spinner("Geocoding addresses..."):
                    st.write("Debug - Addresses to geocode:", st.session_state.addresses)
                    raw_locations = self.geocoding_api.batch_geocode(st.session_state.addresses)
                    st.write("Debug - Raw geocoding output:", raw_locations)  # 🔴 Inspect this
                    
                    if raw_locations.empty:
                        st.error("Geocoding failed: No coordinates found. Check addresses.")
                        return
                        
                    st.session_state.locations_df = raw_locations
                    st.success(f"Successfully geocoded {len(st.session_state.locations_df)} addresses.")
            
            # Distance Matrix step
            if st.session_state.distances is None or st.session_state.durations is None:
                with st.spinner("Calculating distances..."):
                    try:
                        st.write("Debug - Locations DataFrame:", st.session_state.locations_df)
                        dist_df, dur_df = self.distance_api.get_distance_duration_dataframes(
                            st.session_state.locations_df
                        )
                        st.write("Debug - Distance Matrix:", dist_df.head())  # Check output
                        st.write("Debug - Duration Matrix:", dur_df.head())
                        
                        # Validate matrix data
                        if dist_df.isnull().values.any():
                            st.error("Invalid distance data. Check API key/network.")
                            return
                        
                        st.session_state.distances = dist_df.values
                        st.session_state.durations = dur_df.values
                        
                        st.success("Distance matrix calculated successfully.")
                        
                        # Initialize GraphBuilder
                        self.graph_builder = GraphBuilder(
                            st.session_state.locations_df,
                            st.session_state.distances,
                            st.session_state.durations
                        )
                        
                        # Verify graph_builder.locations is properly initialized
                        st.write("Debug - graph_builder.locations:", self.graph_builder.locations)
                        
                        # Build the complete graph for visualization
                        self.graph_builder.build_complete_graph()
                        st.success("GraphBuilder initialized and graph built!")
                        
                        # Display the network graph
                        with st.expander("View Network Graph", expanded=False):
                            st.pyplot(self.graph_builder.visualize_graph())
                        
                        return True
                        
                    except Exception as e:
                        st.error(f"Error calculating distance matrix: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())  # Show full traceback
                        return False
            else:
                # If we already have distance data but graph_builder is None
                if self.graph_builder is None:
                    try:
                        st.write("Debug - Creating GraphBuilder from existing data")
                        self.graph_builder = GraphBuilder(
                            st.session_state.locations_df,
                            st.session_state.distances,
                            st.session_state.durations
                        )
                        self.graph_builder.build_complete_graph()
                        st.success("GraphBuilder initialized from existing data!")
                        return True
                    except Exception as e:
                        st.error(f"Failed to initialize GraphBuilder from existing data: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
                        return False
                return True
                
        except Exception as e:
            st.error(f"Initialization failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return False
    
    def _run_algorithms(self, algorithm_params):
        """Run the selected route optimization algorithms."""
        # 🔴 CRITICAL CHECK: Add this block first
        if self.graph_builder is None:
            st.error("Route data initialization failed! Check addresses/API key.")
            
            # Try to process the data first
            st.warning("Attempting to initialize data...")
            if not self._process_data():
                st.error("Data initialization failed. Cannot run algorithms.")
                
                # Debug information
                st.write("Debug - Session State:")
                st.write("- Addresses:", st.session_state.addresses)
                st.write("- Locations DataFrame empty:", st.session_state.locations_df.empty if hasattr(st.session_state, 'locations_df') else "Not created")
                st.write("- Distances is None:", st.session_state.distances is None)
                st.write("- Durations is None:", st.session_state.durations is None)
                return  # Stop execution early
        
        # Additional validation
        if not hasattr(self.graph_builder, 'locations') or not self.graph_builder.locations:
            st.error("GraphBuilder is missing location data!")
            return
        
        # Reset results
        st.session_state.algorithm_results = []
        self.comparison = AlgorithmComparison()
        
        # Genetic Algorithm
        if algorithm_params['use_genetic']:
            with st.spinner("Running Genetic Algorithm..."):
                # Get GA parameters
                ga_params = algorithm_params['params'].get('genetic', {})
                
                try:
                    # Initialize the GA
                    self.ga_instance = GeneticAlgorithm(
                        self.graph_builder,
                        population_size=ga_params.get('population_size', 100),
                        generations=ga_params.get('generations', 100),
                        crossover_prob=ga_params.get('crossover_prob', 0.8),
                        mutation_prob=ga_params.get('mutation_prob', 0.2)
                    )
                    
                    # Run the GA
                    ga_result = self.ga_instance.optimize()
                    
                    # Add to results
                    st.session_state.algorithm_results.append(ga_result)
                    self.comparison.add_result(
                        ga_result['algorithm'],
                        ga_result['path'],
                        ga_result['distance'],
                        ga_result['duration'],
                        ga_result['computation_time']
                    )
                except Exception as e:
                    st.error(f"Error running Genetic Algorithm: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # A* Search
        if algorithm_params['use_astar']:
            with st.spinner("Running A* Search..."):
                try:
                    # Initialize A*
                    self.astar_instance = AStar(self.graph_builder)
                    
                    # Run A*
                    astar_result = self.astar_instance.find_optimal_path()
                    
                    # Add to results
                    st.session_state.algorithm_results.append(astar_result)
                    self.comparison.add_result(
                        astar_result['algorithm'],
                        astar_result['path'],
                        astar_result['distance'],
                        astar_result['duration'],
                        astar_result['computation_time']
                    )
                except Exception as e:
                    st.error(f"Error running A* Search: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Q-Learning
        if algorithm_params['use_qlearning']:
            with st.spinner("Running Q-Learning (this may take a while)..."):
                # Get Q-Learning parameters
                ql_params = algorithm_params['params'].get('qlearning', {})
                
                try:
                    # Initialize Q-Learning
                    self.ql_instance = QLearning(
                        self.graph_builder,
                        learning_rate=ql_params.get('learning_rate', 0.1),
                        discount_factor=ql_params.get('discount_factor', 0.9),
                        episodes=ql_params.get('episodes', 1000)
                    )
                    
                    # Run Q-Learning
                    ql_result = self.ql_instance.optimize()
                    
                    # Add to results
                    st.session_state.algorithm_results.append(ql_result)
                    self.comparison.add_result(
                        ql_result['algorithm'],
                        ql_result['path'],
                        ql_result['distance'],
                        ql_result['duration'],
                        ql_result['computation_time']
                    )
                except Exception as e:
                    st.error(f"Error running Q-Learning: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Get comparison DataFrame
        st.session_state.comparison_df = self.comparison.get_comparison_dataframe()
    
    def _display_results(self):
        """Display the results of the route optimization algorithms."""
        if st.session_state.algorithm_results:
            # Display comparison table
            st.subheader("Algorithm Comparison")
            st.dataframe(st.session_state.comparison_df)
            
            # Visualize routes on map
            self.map_vis.visualize_routes(
                st.session_state.locations_df,
                st.session_state.algorithm_results
            )
            
            # Visualize algorithm comparison
            comparison_plot = self.map_vis.visualize_comparison(st.session_state.comparison_df)
            
            # Plot GA evolution if available
            if self.ga_instance:
                ga_plot = self.map_vis.plot_evolution(self.ga_instance)
            else:
                ga_plot = None
            
            # Plot Q-Learning progress if available
            if self.ql_instance:
                ql_plot = self.map_vis.plot_learning_progress(self.ql_instance)
            else:
                ql_plot = None
            
            # Export options
            with st.expander("Export Results"):
                export_format = st.radio("Export Format:", ["CSV", "PDF", "Both"])
                
                filename = st.text_input("Filename (without extension):", "path_finder_results")
                
                if st.button("Export"):
                    with st.spinner("Exporting results..."):
                        if export_format in ["CSV", "Both"]:
                            csv_path, _ = self.export_manager.export_to_csv(
                                st.session_state.comparison_df,
                                st.session_state.locations_df,
                                filename
                            )
                            st.success(f"CSV exported to: {csv_path}")
                        
                        if export_format in ["PDF", "Both"]:
                            # Get the network visualization
                            route_map = self.graph_builder.visualize_graph()
                            
                            pdf_path = self.export_manager.export_to_pdf(
                                st.session_state.comparison_df,
                                st.session_state.locations_df,
                                route_map,
                                comparison_plot,
                                filename
                            )
                            st.success(f"PDF exported to: {pdf_path}")
        
        elif not st.session_state.locations_df.empty:
            st.info("Run selected algorithms to see results.")
            
            # Display the geocoded locations
            st.subheader("Geocoded Locations")
            st.dataframe(st.session_state.locations_df[['address', 'lat', 'lng']]) 