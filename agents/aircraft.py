"""
Aircraft Agent Module
Represents individual aircraft in the simulation
"""

from mesa import Agent


class Aircraft(Agent):
    """
    Aircraft agent representing a single flight.
    Passive agent - all decisions made by the model.
    """
    
    def __init__(self, unique_id, model, arrival_time, turnaround_time):
        """
        Initialize an aircraft agent.
        
        Args:
            unique_id: Unique identifier for the aircraft
            model: Reference to the airport model
            arrival_time: Scheduled arrival time (minute)
            turnaround_time: Ground time duration (minutes)
        """
        super().__init__(model)
        self.unique_id = unique_id
        self.aircraft_id = unique_id
        self.arrival_time = arrival_time
        self.turnaround_time = turnaround_time
        self.departure_time = arrival_time + turnaround_time
        self.assigned_stand_type = None  # Will be 'PLB' or 'REMOTE'
        self.state = 'scheduled'  # States: scheduled, parked, departed
    
    def step(self):
        """
        Agent step method (required by Mesa).
        Aircraft are passive - no active behavior.
        """
        pass
    
    def assign_stand(self, stand_type):
        """
        Assign aircraft to a stand type.
        
        Args:
            stand_type: 'PLB' or 'REMOTE'
        """
        self.assigned_stand_type = stand_type
        self.state = 'parked'
    
    def depart(self):
        """
        Mark aircraft as departed.
        """
        self.state = 'departed'
    
    def __repr__(self):
        return (f"Aircraft({self.aircraft_id}, arrival={self.arrival_time}, "
                f"departure={self.departure_time}, stand={self.assigned_stand_type})")