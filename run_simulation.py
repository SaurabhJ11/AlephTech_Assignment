
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data.generate_data import generate_aircraft_data, save_aircraft_data
from model.airport_model import AirportModel
from analytics.metrics import analyze_simulation
import pandas as pd


def run_complete_simulation():
    """
    Execute the complete simulation pipeline:
    1. Generate aircraft data
    2. Run simulation
    3. Save results
    4. Analyze metrics
    """
    print("="*70)
    print("AIRPORT STAND ALLOCATION SIMULATION")
    print("Event-Driven Greedy Allocation with Mesa")
    print("="*70)
    
    # Step 1: Generate aircraft data
    print("\n📋 STEP 1: Generating Aircraft Data...")
    aircraft_data = save_aircraft_data('data/input_aircraft.csv')
    
    # Step 2: Initialize and run simulation
    print("\n🛫 STEP 2: Initializing Simulation...")
    model = AirportModel(
        aircraft_data=aircraft_data,
        plb_stands=35,
        simulation_duration=360
    )
    
    print("\n⚙️  STEP 3: Running Simulation...")
    minute_df, aircraft_results_df = model.run_simulation()
    
    # Step 3: Save results
    print("\n💾 STEP 4: Saving Results...")
    model.save_results('data/simulation_output.csv')
    
    # Step 4: Analyze metrics
    print("\n📊 STEP 5: Analyzing Metrics...")
    metrics = analyze_simulation(
        aircraft_csv='data/simulation_output.csv',
        minute_csv='data/simulation_output_minute.csv'
    )
    
    print("\n✅ Simulation Complete!")
    print("="*70)
    
    return model, metrics


if __name__ == '__main__':
    run_complete_simulation()