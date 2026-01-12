
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data.generate_data import generate_aircraft_data, save_aircraft_data
from model.airport_model import AirportModel
from analytics.metrics import analyze_simulation
import pandas as pd


def run_complete_simulation():
    print("="*70)
    print("AIRPORT STAND ALLOCATION SIMULATION")
    print("Event-Driven Greedy Allocation with Mesa")
    print("="*70)
    
    print("\nGenerating Aircraft Data...")
    aircraft_data = save_aircraft_data('data/input_aircraft.csv')
    
    print("\nInitializing Simulation...")
    model = AirportModel(
        aircraft_data=aircraft_data,
        plb_stands=35,
        simulation_duration=360
    )
    
    print("\nRunning Simulation...")
    minute_df, aircraft_results_df = model.run_simulation()
    
    print("\nSaving Results...")
    model.save_results('data/simulation_output.csv')
    
    print("\nAnalyzing Metrics...")
    metrics = analyze_simulation(
        aircraft_csv='data/simulation_output.csv',
        minute_csv='data/simulation_output_minute.csv'
    )
    
    print("\nSimulation Complete!")
    print("="*70)
    
    return model, metrics


if __name__ == '__main__':
    run_complete_simulation()