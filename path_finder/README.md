# Path Finder - AI-Powered Delivery Route Optimization

Path Finder is a delivery route optimization system that uses multiple AI algorithms (Genetic Algorithm, A* Search, and Q-Learning) to find optimal routes for deliveries based on real-world data from Google Maps API.

## Features

- Convert addresses to geographic coordinates using Google Maps Geocoding API
- Calculate real distances and durations using Google Distance Matrix API
- Optimize delivery routes using three algorithms:
  - Genetic Algorithm
  - A* Search
  - Q-Learning (Reinforcement Learning)
- Compare algorithm performance (distance, time, computational cost)
- Visualize routes on interactive maps
- Export route details to CSV and PDF
- User-friendly Streamlit interface

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/path-finder.git
cd path-finder
```

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Google Maps API Key
1. The project already includes an API key in the `.env` file. If you want to use your own:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the following APIs:
     - Geocoding API
     - Distance Matrix API
     - Maps Static API
   - Create an API key
   - Replace the key in the `.env` file

### Step 5: Run the Application
```bash
streamlit run main.py
```

## Usage Guide

1. **Input Delivery Addresses**:
   - Enter addresses manually in the form
   - Or upload a CSV file with addresses

2. **Choose Algorithm**:
   - Select one or more algorithms to run
   - Adjust algorithm parameters if needed

3. **View Results**:
   - Compare algorithm performance
   - View routes on the map
   - Export results to CSV or PDF

## Sample Addresses for Testing

The application includes sample addresses from Dhaka city:
- Gulshan Circle 1, Dhaka
- Dhanmondi 32, Dhaka
- Uttara Sector 7, Dhaka
- Mirpur 10, Dhaka
- Banani Circle 1, Dhaka
- Bashundhara City Shopping Complex, Dhaka

## Project Structure

```
path_finder/
├── algorithms/
│   ├── a_star.py
│   ├── genetic_algorithm.py
│   ├── q_learning.py
│   └── __init__.py
├── api/
│   ├── geocoding.py
│   ├── distance_matrix.py
│   └── __init__.py
├── gui/
│   ├── dashboard.py
│   ├── input_form.py
│   ├── map_visualization.py
│   └── __init__.py
├── utils/
│   ├── graph.py
│   ├── comparison.py
│   ├── export.py
│   └── __init__.py
├── main.py
├── .env
└── requirements.txt
``` 