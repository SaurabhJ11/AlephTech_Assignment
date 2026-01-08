"""
Analytics Module
Post-simulation metrics and analysis
"""

import pandas as pd
import numpy as np


class SimulationMetrics:
    """
    Calculate and display key operational metrics from simulation results.
    """
    
    def __init__(self, aircraft_df, minute_df):
        """
        Initialize metrics calculator.
        
        Args:
            aircraft_df: DataFrame with per-aircraft results
            minute_df: DataFrame with minute-by-minute system state
        """
        self.aircraft_df = aircraft_df
        self.minute_df = minute_df
    
    def calculate_all_metrics(self):
        """
        Calculate all required metrics and return as dictionary.
        """
        metrics = {
            'plb_utilization': self.plb_utilization(),
            'plb_assignment_rate': self.plb_assignment_rate(),
            'peak_parked_aircraft': self.peak_concurrent_parked(),
            'average_ground_time': self.average_ground_time()
        }
        return metrics
    
    def plb_utilization(self):
        """
        Calculate PLB stand utilization percentage.
        
        Operational Relevance:
        Indicates how effectively scarce PLB resources are used.
        High utilization means infrastructure is well-utilized but may indicate
        capacity constraints. Low utilization suggests over-capacity or
        inefficient scheduling.
        
        Returns:
            Dictionary with metric value and explanation
        """
        plb_total = 35  # Fixed assumption
        avg_plb_occupied = self.minute_df['plb_occupied'].mean()
        utilization_pct = (avg_plb_occupied / plb_total) * 100
        
        return {
            'value': utilization_pct,
            'unit': '%',
            'description': 'Average PLB Stand Utilization',
            'explanation': (
                'Indicates how effectively scarce PLB resources are used. '
                'High utilization (>80%) suggests capacity constraints and potential need '
                'for expansion. Low utilization (<60%) may indicate over-capacity or '
                'inefficient scheduling patterns.'
            ),
            'avg_occupied': avg_plb_occupied,
            'total_stands': plb_total
        }
    
    def plb_assignment_rate(self):
        """
        Calculate percentage of aircraft assigned to PLB stands.
        
        Operational Relevance:
        Measures quality of service and infrastructure sufficiency.
        Higher PLB assignment rates indicate better passenger experience
        (shorter distances, jet bridges) but require adequate capacity.
        
        Returns:
            Dictionary with metric value and explanation
        """
        total_aircraft = len(self.aircraft_df)
        plb_aircraft = len(self.aircraft_df[self.aircraft_df['assigned_stand_type'] == 'PLB'])
        assignment_rate_pct = (plb_aircraft / total_aircraft) * 100
        
        return {
            'value': assignment_rate_pct,
            'unit': '%',
            'description': 'Percentage of Aircraft Assigned PLB',
            'explanation': (
                'Measures quality of service and infrastructure sufficiency. '
                'Higher PLB rates (>70%) indicate better passenger experience with '
                'jet bridges and shorter walking distances. Lower rates suggest '
                'capacity shortfalls requiring remote stands with bus transport.'
            ),
            'plb_count': plb_aircraft,
            'remote_count': total_aircraft - plb_aircraft,
            'total_count': total_aircraft
        }
    
    def peak_concurrent_parked(self):
        """
        Identify maximum concurrent parked aircraft.
        
        Operational Relevance:
        Identifies maximum congestion levels and peak capacity requirements.
        Critical for infrastructure planning and understanding worst-case
        operational scenarios.
        
        Returns:
            Dictionary with metric value and explanation
        """
        peak_parked = self.minute_df['total_parked'].max()
        peak_time = self.minute_df['total_parked'].idxmax()
        
        return {
            'value': peak_parked,
            'unit': 'aircraft',
            'description': 'Peak Concurrent Parked Aircraft',
            'explanation': (
                'Identifies maximum congestion levels and peak capacity requirements. '
                'This metric is critical for infrastructure planning, staffing decisions, '
                'and understanding worst-case operational scenarios during peak periods.'
            ),
            'peak_time_minutes': peak_time,
            'peak_time_hours': peak_time / 60
        }
    
    def average_ground_time(self):
        """
        Calculate average aircraft ground time.
        
        Operational Relevance:
        Validates realism of simulation against operational assumptions.
        Ground time affects stand occupancy, capacity planning, and
        scheduling efficiency.
        
        Returns:
            Dictionary with metric value and explanation
        """
        avg_ground_time = self.aircraft_df['turnaround_time'].mean()
        std_ground_time = self.aircraft_df['turnaround_time'].std()
        min_ground_time = self.aircraft_df['turnaround_time'].min()
        max_ground_time = self.aircraft_df['turnaround_time'].max()
        
        return {
            'value': avg_ground_time,
            'unit': 'minutes',
            'description': 'Average Ground Time',
            'explanation': (
                'Validates realism of simulation against operational assumptions (target: 58 min). '
                'Ground time directly affects stand occupancy rates, capacity planning, '
                'and overall scheduling efficiency. Variability impacts buffer requirements.'
            ),
            'std_dev': std_ground_time,
            'min': min_ground_time,
            'max': max_ground_time
        }
    
    def print_summary(self):
        """
        Print a formatted summary of all metrics.
        """
        metrics = self.calculate_all_metrics()
        
        print("\n" + "="*70)
        print("SIMULATION METRICS SUMMARY")
        print("="*70)
        
        # Metric 1: PLB Utilization
        plb_util = metrics['plb_utilization']
        print(f"\n1️⃣  {plb_util['description']}")
        print(f"   Value: {plb_util['value']:.2f}{plb_util['unit']}")
        print(f"   Average Occupied: {plb_util['avg_occupied']:.1f} / {plb_util['total_stands']} stands")
        print(f"   \n   📊 {plb_util['explanation']}")
        
        # Metric 2: PLB Assignment Rate
        plb_assign = metrics['plb_assignment_rate']
        print(f"\n2️⃣  {plb_assign['description']}")
        print(f"   Value: {plb_assign['value']:.2f}{plb_assign['unit']}")
        print(f"   PLB: {plb_assign['plb_count']} aircraft | Remote: {plb_assign['remote_count']} aircraft")
        print(f"   \n   📊 {plb_assign['explanation']}")
        
        # Metric 3: Peak Concurrent Parked
        peak = metrics['peak_parked_aircraft']
        print(f"\n3️⃣  {peak['description']}")
        print(f"   Value: {peak['value']} {peak['unit']}")
        print(f"   Occurred at: {peak['peak_time_hours']:.2f} hours ({peak['peak_time_minutes']} minutes)")
        print(f"   \n   📊 {peak['explanation']}")
        
        # Metric 4: Average Ground Time
        ground = metrics['average_ground_time']
        print(f"\n4️⃣  {ground['description']}")
        print(f"   Value: {ground['value']:.2f} {ground['unit']}")
        print(f"   Range: {ground['min']} - {ground['max']} minutes (±{ground['std_dev']:.1f} std dev)")
        print(f"   \n   📊 {ground['explanation']}")
        
        print("\n" + "="*70)
    
    def export_metrics(self, output_path='analytics/metrics_summary.txt'):
        """
        Export metrics summary to text file.
        
        Args:
            output_path: Path to save metrics summary
        """
        from pathlib import Path
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        metrics = self.calculate_all_metrics()
        
        with open(output_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("SIMULATION METRICS SUMMARY\n")
            f.write("="*70 + "\n\n")
            
            for i, (key, metric) in enumerate(metrics.items(), 1):
                f.write(f"{i}. {metric['description']}\n")
                f.write(f"   Value: {metric['value']:.2f} {metric['unit']}\n")
                f.write(f"   {metric['explanation']}\n\n")
        
        print(f"\nMetrics exported to: {output_path}")


def analyze_simulation(aircraft_csv='data/simulation_output.csv',
                       minute_csv='data/simulation_output_minute.csv'):
    """
    Load simulation results and perform analysis.
    
    Args:
        aircraft_csv: Path to aircraft results CSV
        minute_csv: Path to minute-by-minute results CSV
    
    Returns:
        SimulationMetrics object
    """
    aircraft_df = pd.read_csv(aircraft_csv)
    minute_df = pd.read_csv(minute_csv)
    
    metrics = SimulationMetrics(aircraft_df, minute_df)
    metrics.print_summary()
    metrics.export_metrics()
    
    return metrics


if __name__ == '__main__':
    analyze_simulation()