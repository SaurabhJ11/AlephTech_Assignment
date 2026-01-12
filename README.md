Airport Stand Allocation Simulation 

1. What Was Built:
      Overview
        This project implements an event-driven airport stand allocation simulation using Python's Mesa agent-based modeling framework. The simulation models aircraft arriving at an airport, being assigned to parking stands using a greedy first-come-first-served allocation strategy, occupying the stand for their turnaround duration, and departing.
        Core Components
      1. Aircraft Agents (agents/aircraft.py)
        Passive agents representing individual flights
        Track arrival time, departure time, assigned stand type, and operational state
        State transitions: scheduled → parked → departed
      2. Airport Model (model/airport_model.py)
        Central simulation controller implementing event-driven architecture
        Manages a priority queue (min-heap) for chronological event processing
        Handles ARRIVAL and DEPARTURE events
        Implements greedy allocation: assigns PLB stands if available, otherwise Remote stands
        Collects time-series metrics at 1-minute resolution
      3. Data Generation (data/generate_data.py)
        Generates synthetic aircraft arrival data
        Arrival times: Uniformly distributed across simulation period
        Turnaround times: Truncated normal distribution (mean=58, range=30-120 minutes)
      4. Analytics Module (analytics/metrics.py)
        Post-simulation analysis calculating 4 operational metrics
        PLB Stand Utilization, PLB Assignment Rate, Peak Concurrent Aircraft, Average Ground Time
        Exports formatted reports and CSV files

  2. How to Run:
    Prerequisites
      Python 3.14.2
      Mesa 3.4.0
      Numpy 2.4.0
      Pandas 2.3.3
     
Installation
      Step 1: Navigate to project directory
      cd airport_simulation

      Step 2: Install dependencies
      pip install mesa pandas numpy

Execution
      Run complete simulation pipeline:
      python run_simulation.py
      
This executes:
      Generates synthetic aircraft data (270 aircraft)
      Initializes simulation with 35 PLB stands
      Runs 6-hour simulation (360 time steps)
      Saves results to CSV files
      Calculates and displays 4 key metrics
      Expected Runtime: 5-10 seconds
      Individual Components
      
      Generate data only:
      python -m data.generate_data
      
      Analyze existing results:
      python -m analytics.metrics
      

Average turnaround time: 58 minutes  
Average parked aircraft at steady state: ~40 
Number of PLB stands: 35 (limited) 
Average aircraft movements (arrivals + departures): 90 per hour
Remote stands: Unlimited
Simulation duration: 6 hours (360 minutes)
Time resolution: 1 minute per simulation step


Algorithm Complexity
Event Queue Operations: O(log n) per insertion/deletion
Total Simulation: O(n log n) where n ≈ 540 events
Memory: O(n) for storing aircraft and event queue
Key Design Patterns
Event-Driven Architecture: Chronological event processing via priority queue
Agent-Based Modeling: Aircraft as passive agents with state
Greedy Strategy: First-come-first-served allocation
Observer Pattern: Data collection at each step

 
 Design Philosophy
      "Code explains how things work. Documentation explains why they exist."
      
      This simulation prioritizes:
        Clarity over complexity
        Explainability over optimization
        Reproducibility over randomness
        Modularity over monolithic design
        
      Why Greedy? 
      While suboptimal, greedy allocation is deterministic, fast, and easy to explain. Establishes baseline for future optimization.
      
      Why Event-Driven? 
      Efficiency and realism. Real airports operate on event triggers, not uniform polling.
      
      Why Mesa? 
      Clean agent-based framework with minimal overhead. Provides structure without unnecessary complexity.
