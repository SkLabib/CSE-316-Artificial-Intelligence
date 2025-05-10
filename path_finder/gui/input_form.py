import streamlit as st
import pandas as pd
import os
import tempfile
from io import StringIO

class InputForm:
    def __init__(self):
        """Initialize the input form component for the Streamlit GUI."""
        self.sample_addresses = [
            "Gulshan Circle 1, Dhaka",
            "Dhanmondi 32, Dhaka",
            "Uttara Sector 7, Dhaka",
            "Mirpur 10, Dhaka",
            "Banani Circle 1, Dhaka",
            "Bashundhara City Shopping Complex, Dhaka"
        ]
    
    def render(self):
        """Render the input form in the Streamlit sidebar."""
        st.sidebar.title("Input Options")
        
        input_method = st.sidebar.radio(
            "Choose input method:",
            ["Manual Entry", "CSV Upload", "Sample Addresses"]
        )
        
        addresses = []
        
        if input_method == "Manual Entry":
            addresses = self._manual_entry_form()
        elif input_method == "CSV Upload":
            addresses = self._csv_upload_form()
        else:  # Sample Addresses
            addresses = self._use_sample_addresses()
        
        if addresses:
            # Show the addresses in the main area
            st.subheader("Delivery Addresses")
            for i, addr in enumerate(addresses, 1):
                st.write(f"{i}. {addr}")
        
        return addresses
    
    def _manual_entry_form(self):
        """Render the manual entry form for addresses."""
        st.sidebar.subheader("Enter Addresses")
        
        # Starting point
        starting_point = st.sidebar.text_input("Starting Point (first address):", 
                                              value="Gulshan Circle 1, Dhaka")
        
        # Dynamic address inputs
        addresses = [starting_point]
        
        # Add initial additional address fields
        num_addresses = st.sidebar.number_input("Number of additional addresses:", 
                                              min_value=1, max_value=20, value=3)
        
        for i in range(1, num_addresses + 1):
            address = st.sidebar.text_input(f"Address {i+1}:", key=f"addr_{i}")
            if address.strip():
                addresses.append(address)
        
        if st.sidebar.button("Process Addresses"):
            if len(addresses) < 2:
                st.sidebar.error("Please enter at least 2 addresses (starting point + 1 destination).")
                return []
            
            # Filter out empty addresses
            addresses = [addr for addr in addresses if addr.strip()]
            return addresses
        
        return []
    
    def _csv_upload_form(self):
        """Render the CSV upload form for addresses."""
        st.sidebar.subheader("Upload CSV File")
        st.sidebar.markdown("""
        CSV file should have a column named 'address' with the addresses.
        The first address will be considered as the starting point.
        """)
        
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(uploaded_file)
                
                # Check if 'address' column exists
                if 'address' not in df.columns:
                    st.sidebar.error("CSV file must contain a column named 'address'.")
                    return []
                
                # Extract addresses
                addresses = df['address'].dropna().tolist()
                
                if len(addresses) < 2:
                    st.sidebar.error("Please provide at least 2 addresses in the CSV file.")
                    return []
                
                return addresses
            
            except Exception as e:
                st.sidebar.error(f"Error reading CSV file: {str(e)}")
                return []
        
        return []
    
    def _use_sample_addresses(self):
        """Use sample addresses for testing."""
        st.sidebar.subheader("Sample Addresses from Dhaka")
        
        # Allow selecting which sample addresses to use
        selected_addresses = []
        for addr in self.sample_addresses:
            if st.sidebar.checkbox(addr, value=True, key=f"sample_{addr}"):
                selected_addresses.append(addr)
        
        if st.sidebar.button("Use Selected Addresses"):
            if len(selected_addresses) < 2:
                st.sidebar.error("Please select at least 2 addresses.")
                return []
            
            return selected_addresses
        
        return []
    
    def get_algorithm_params(self):
        """Get algorithm parameters from the sidebar."""
        st.sidebar.title("Algorithm Settings")
        
        # Select which algorithms to run
        st.sidebar.subheader("Select Algorithms")
        use_genetic = st.sidebar.checkbox("Genetic Algorithm", value=True)
        use_astar = st.sidebar.checkbox("A* Search", value=True)
        use_qlearning = st.sidebar.checkbox("Q-Learning", value=True)
        
        # Algorithm-specific parameters
        params = {}
        
        if use_genetic:
            st.sidebar.subheader("Genetic Algorithm Parameters")
            params['genetic'] = {
                'population_size': st.sidebar.slider("Population Size", 10, 200, 100, 10),
                'generations': st.sidebar.slider("Generations", 10, 300, 100, 10),
                'crossover_prob': st.sidebar.slider("Crossover Probability", 0.1, 1.0, 0.8, 0.1),
                'mutation_prob': st.sidebar.slider("Mutation Probability", 0.01, 0.5, 0.2, 0.01)
            }
        
        if use_qlearning:
            st.sidebar.subheader("Q-Learning Parameters")
            params['qlearning'] = {
                'episodes': st.sidebar.slider("Episodes", 100, 2000, 1000, 100),
                'learning_rate': st.sidebar.slider("Learning Rate", 0.01, 0.5, 0.1, 0.01),
                'discount_factor': st.sidebar.slider("Discount Factor", 0.5, 0.99, 0.9, 0.01)
            }
        
        # A* doesn't have many adjustable parameters, but we can add them if needed
        
        return {
            'use_genetic': use_genetic,
            'use_astar': use_astar,
            'use_qlearning': use_qlearning,
            'params': params
        } 