"""
Aircraft Data Generation Module
Generates synthetic aircraft arrival and turnaround data
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_aircraft_data(
    simulation_hours=6,
    arrivals_per_hour=45,
    mean_turnaround=58,
    min_turnaround=30,
    max_turnaround=120,
    random_seed=42
):
    """
    Generate synthetic aircraft data for simulation.
    
    Args:
        simulation_hours: Total simulation duration in hours
        arrivals_per_hour: Average number of arrivals per hour
        mean_turnaround: Mean turnaround time in minutes
        min_turnaround: Minimum turnaround time in minutes
        max_turnaround: Maximum turnaround time in minutes
        random_seed: Random seed for reproducibility
    
    Returns:
        DataFrame with columns: aircraft_id, arrival_time, turnaround_time
    """
    np.random.seed(random_seed)
    
    total_minutes = simulation_hours * 60
    total_aircraft = int(arrivals_per_hour * simulation_hours)
    
    # Generate arrival times - uniformly distributed across simulation period
    arrival_times = np.random.uniform(0, total_minutes, total_aircraft)
    arrival_times = np.sort(arrival_times).astype(int)
    
    # Generate turnaround times using truncated normal distribution
    # Use normal distribution centered at mean, then clip to min/max
    std_dev = (max_turnaround - min_turnaround) / 6  # ~99.7% within range
    turnaround_times = np.random.normal(mean_turnaround, std_dev, total_aircraft)
    turnaround_times = np.clip(turnaround_times, min_turnaround, max_turnaround)
    turnaround_times = turnaround_times.astype(int)
    
    # Create DataFrame
    aircraft_data = pd.DataFrame({
        'aircraft_id': [f'AC{i:04d}' for i in range(total_aircraft)],
        'arrival_time': arrival_times,
        'turnaround_time': turnaround_times
    })
    
    return aircraft_data


def save_aircraft_data(output_path='data/input_aircraft.csv'):
    """
    Generate and save aircraft data to CSV.
    
    Args:
        output_path: Path to save the CSV file
    """
    # Ensure data directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate data
    aircraft_data = generate_aircraft_data()
    
    # Save to CSV
    aircraft_data.to_csv(output_path, index=False)
    
    print(f"Generated {len(aircraft_data)} aircraft records")
    print(f"Saved to: {output_path}")
    print(f"\nData Summary:")
    print(f"  Arrival time range: {aircraft_data['arrival_time'].min()} - {aircraft_data['arrival_time'].max()} minutes")
    print(f"  Mean turnaround time: {aircraft_data['turnaround_time'].mean():.1f} minutes")
    print(f"  Turnaround time range: {aircraft_data['turnaround_time'].min()} - {aircraft_data['turnaround_time'].max()} minutes")
    
    return aircraft_data


if __name__ == '__main__':
    save_aircraft_data()