import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from bs4 import BeautifulSoup
import requests

# Constants for mission phases and Link Budget calculation
EARTH_ORBIT_END = 1000  # Example placeholder (update with actual value)
MOON_ORBIT_START = 5000  # Example placeholder (update with actual value)


def load_data(file_path):
    """
    Load Artemis II trajectory data from a file.
    """
    try:
        data = pd.read_excel(file_path)
        print(f"Data loaded successfully with {len(data)} records.")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def visualize_trajectory(data):
    """
    Visualize the 3D trajectory of Artemis II using Plotly,
    with the velocity vector magnitude plotted as color.
    """
    # Calculate velocity magnitude
    data['Velocity Magnitude (km/s)'] = np.sqrt(
        data['Vx(km/s)[J2000-EARTH]']**2 +
        data['Vy(km/s)[J2000-EARTH]']**2 +
        data['Vz(km/s)[J2000-EARTH]']**2
    )
    """
    Visualize the 3D trajectory of Artemis II using Plotly.
    """
    fig = px.line_3d(
        data, 
        x='Vx(km/s)[J2000-EARTH]', 
        y='Vy(km/s)[J2000-EARTH]', 
        z='Vz(km/s)[J2000-EARTH]', 
        color='MISSION ELAPSED TIME (mins)',
        title='Artemis II Mission Path'
    )
    fig.show()

def scrape_slant_range(url):
    """
    Scrape slant range data from a given website.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Example: Update with actual tag/class for slant range
        slant_range = soup.find('div', {'class': 'slant-range'}).text.strip()
        print(f"Slant Range: {slant_range}")
        return float(slant_range)
    except Exception as e:
        print(f"Error scraping slant range: {e}")
        return None

def calculate_link_budget(EIRP, G, FSPL, losses):
    """
    Calculate the Link Budget.
    """
    return EIRP + G - FSPL - losses

def main():
    # Step 1: Load trajectory data
    file_path = 'project/data/fy25-adc-high-school-data.xlsx'
    data = load_data(file_path)
    if data is None:
        return -1

    # Step 2: Visualize trajectory
    visualize_trajectory(data)

    # Step 3: Scrape slant range data
    url = "https://scan-now.gsfc.nasa.gov/scan"  # Replace with actual URL
    slant_range = scrape_slant_range(url)
    slant_range = 10

    # Step 4: Perform Link Budget calculation (placeholder values)
    if slant_range:
        link_budget = calculate_link_budget(EIRP=50, G=30, FSPL=slant_range, losses=10)
        print(f"Link Budget: {link_budget} dB")

if __name__ == "__main__":
    main()
