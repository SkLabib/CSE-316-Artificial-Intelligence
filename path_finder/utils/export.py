import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class ExportManager:
    def __init__(self, output_dir="exports"):
        """Initialize the export manager with an output directory."""
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def export_to_csv(self, comparison_df, locations_df, filename=None):
        """Export the algorithm comparison and location data to CSV."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"path_finder_results_{timestamp}.csv"
        
        # Ensure the filename has .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Save the comparison data
        comparison_df.to_csv(filepath, index=False)
        
        # Save the location data to a separate file
        locations_filename = filename.replace('.csv', '_locations.csv')
        locations_filepath = os.path.join(self.output_dir, locations_filename)
        locations_df.to_csv(locations_filepath, index=False)
        
        return filepath, locations_filepath
    
    def export_to_pdf(self, comparison_df, locations_df, route_map=None, comparison_plot=None, filename=None):
        """Export the algorithm comparison, location data, and visualizations to PDF."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"path_finder_report_{timestamp}.pdf"
        
        # Ensure the filename has .pdf extension
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF instance
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Path Finder - Route Optimization Report", ln=True, align='C')
        pdf.ln(5)
        
        # Date and time
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 5, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(5)
        
        # Algorithm Comparison Table
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Algorithm Comparison", ln=True)
        pdf.set_font("Arial", "", 8)
        
        # Table header
        col_width = 40
        row_height = 7
        pdf.set_fill_color(200, 220, 255)
        for header in comparison_df.columns:
            pdf.cell(col_width, row_height, header, border=1, fill=True)
        pdf.ln(row_height)
        
        # Table data
        for _, row in comparison_df.iterrows():
            for value in row:
                pdf.cell(col_width, row_height, str(value)[:38], border=1)
            pdf.ln(row_height)
        
        pdf.ln(10)
        
        # Location Data
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Delivery Locations", ln=True)
        pdf.set_font("Arial", "", 8)
        
        # Table header
        col_width = 40
        for header in ['Address', 'Latitude', 'Longitude']:
            if header in locations_df.columns:
                pdf.cell(col_width, row_height, header, border=1, fill=True)
        pdf.ln(row_height)
        
        # Table data (limit to first 20 locations for readability)
        max_locations = min(20, len(locations_df))
        for i in range(max_locations):
            row = locations_df.iloc[i]
            pdf.cell(col_width, row_height, str(row.get('address', ''))[:38], border=1)
            pdf.cell(col_width, row_height, str(row.get('lat', ''))[:38], border=1)
            pdf.cell(col_width, row_height, str(row.get('lng', ''))[:38], border=1)
            pdf.ln(row_height)
        
        pdf.ln(10)
        
        # Add Comparison Plot if provided
        if comparison_plot:
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Algorithm Performance Comparison", ln=True)
            
            img_file = os.path.join(self.output_dir, "temp_comparison_plot.png")
            comparison_plot.savefig(img_file, dpi=300, bbox_inches='tight')
            pdf.image(img_file, x=20, w=170)
            os.remove(img_file)  # Clean up temp file
            
            pdf.ln(10)
        
        # Add Route Map if provided
        if route_map:
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Optimized Route Map", ln=True)
            
            img_file = os.path.join(self.output_dir, "temp_route_map.png")
            route_map.savefig(img_file, dpi=300, bbox_inches='tight')
            pdf.image(img_file, x=20, w=170)
            os.remove(img_file)  # Clean up temp file
        
        # Save the PDF
        pdf.output(filepath)
        
        return filepath
    
    def fig_to_base64(self, fig):
        """Convert a matplotlib figure to a base64 encoded string for embedding in HTML."""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return image_data 