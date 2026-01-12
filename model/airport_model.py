from mesa import Model
import pandas as pd
from collections import deque
import heapq
from agents.aircraft import Aircraft


class AirportModel(Model):
    """
    Event-driven airport stand allocation model.
    Uses greedy allocation strategy for PLB vs Remote stands.
    """
    
    def __init__(self, aircraft_data, plb_stands=35, simulation_duration=360):
        """
        Initialize the airport model.
        
        Args:
            aircraft_data: DataFrame with columns [aircraft_id, arrival_time, turnaround_time]
            plb_stands: Number of available PLB stands
            simulation_duration: Total simulation time in minutes
        """
        super().__init__()
        
        #parameters
        self.plb_total = plb_stands
        self.plb_available = plb_stands
        self.simulation_duration = simulation_duration
        self.current_time = 0
        
        
        self.event_queue = []
        
        self.parked_aircraft = set()
        self.aircraft_by_id = {}
        self.all_agents = []
        
        self.aircraft_results = []
        self.minute_results = []
        
        self.model_reporters_data = []
        
        self._initialize_aircraft(aircraft_data)
        
        print(f"Airport Model Initialized:")
        print(f"  PLB Stands: {self.plb_total}")
        print(f"  Total Aircraft: {len(aircraft_data)}")
        print(f"  Simulation Duration: {self.simulation_duration} minutes")
        print(f"  Total Events: {len(self.event_queue)}")
    
    def _initialize_aircraft(self, aircraft_data):
        """
        Create aircraft agents and schedule ARRIVAL events.
        
        Args:
            aircraft_data: DataFrame with aircraft information
        """
        for idx, row in aircraft_data.iterrows():
            aircraft = Aircraft(
                unique_id=row['aircraft_id'],
                model=self,
                arrival_time=int(row['arrival_time']),
                turnaround_time=int(row['turnaround_time'])
            )
            
            self.all_agents.append(aircraft)
            
            self.aircraft_by_id[aircraft.aircraft_id] = aircraft
            
            self._schedule_event(aircraft.arrival_time, 'ARRIVAL', aircraft.aircraft_id)
    
    def _schedule_event(self, time, event_type, aircraft_id):
        """
        Schedule an event in the priority queue.
        
        Args:
            time: Event time (minute)
            event_type: 'ARRIVAL' or 'DEPARTURE'
            aircraft_id: Aircraft identifier
        """
        heapq.heappush(self.event_queue, (time, event_type, aircraft_id))
    
    def _process_arrival(self, aircraft_id):
        """
        Process an ARRIVAL event using greedy allocation.
        
        Args:
            aircraft_id: Aircraft identifier
        """
        aircraft = self.aircraft_by_id[aircraft_id]
        
        if self.plb_available > 0:
            aircraft.assign_stand('PLB')
            self.plb_available -= 1
        else:
            aircraft.assign_stand('REMOTE')
        
        self.parked_aircraft.add(aircraft_id)
        





        self._schedule_event(aircraft.departure_time, 'DEPARTURE', aircraft_id)
    
    def _process_departure(self, aircraft_id):
        """
        Process a DEPARTURE event.
        
        Args:
            aircraft_id: Aircraft identifier
        """
        aircraft = self.aircraft_by_id[aircraft_id]
        
        if aircraft.assigned_stand_type == 'PLB':
            self.plb_available += 1
        
        aircraft.depart()
        self.parked_aircraft.remove(aircraft_id)
        
        self.aircraft_results.append({
            'aircraft_id': aircraft.aircraft_id,
            'arrival_time': aircraft.arrival_time,
            'departure_time': aircraft.departure_time,
            'turnaround_time': aircraft.turnaround_time,
            'assigned_stand_type': aircraft.assigned_stand_type
        })
    
    def _process_events_at_current_time(self):
        """
        Process all events scheduled for the current time.
        """
        while self.event_queue and self.event_queue[0][0] == self.current_time:
            event_time, event_type, aircraft_id = heapq.heappop(self.event_queue)
            
            if event_type == 'ARRIVAL':
                self._process_arrival(aircraft_id)
            elif event_type == 'DEPARTURE':
                self._process_departure(aircraft_id)
    
    def step(self):
        """
        Advance simulation by one minute.
        Event-driven processing at each time step.
        """

        self._process_events_at_current_time()
        

        self.model_reporters_data.append({
            'current_time': self.current_time,
            'plb_occupied': self.plb_total - self.plb_available,
            'total_parked': len(self.parked_aircraft),
            'remote_occupied': len([a for a in self.parked_aircraft 
                                   if self.aircraft_by_id[a].assigned_stand_type == 'REMOTE']),
            'plb_available': self.plb_available
        })
        

        self.current_time += 1
    
    def run_simulation(self):
        """
        Run the complete simulation from start to finish.
        """
        print("\nRunning simulation...")
        
        while self.current_time <= self.simulation_duration:
            self.step()
            

            if self.current_time % 60 == 0:
                print(f"  Time: {self.current_time // 60} hours ({self.current_time} minutes)")
        
        print("Simulation complete!")
        

        self.minute_results = pd.DataFrame(self.model_reporters_data)
        
        return self.minute_results, pd.DataFrame(self.aircraft_results)
    
    def save_results(self, output_path='data/simulation_output.csv'):
        """
        Save simulation results to CSV.
        
        Args:
            output_path: Path to save results
        """
        aircraft_df = pd.DataFrame(self.aircraft_results)
        aircraft_df.to_csv(output_path, index=False)
        print(f"\nResults saved to: {output_path}")
        

        minute_output = output_path.replace('.csv', '_minute.csv')
        self.minute_results.to_csv(minute_output, index=False)
        print(f"Minute-by-minute data saved to: {minute_output}")