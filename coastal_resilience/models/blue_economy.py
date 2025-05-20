"""
Blue economy model for simulating marine economic activities in coastal Bangladesh.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime

@dataclass
class BlueEconomyParameters:
    """Parameters for blue economy model simulation."""
    start_year: int = 2024
    end_year: int = 2039
    time_step: int = 1  # years
    
    # Fisheries parameters
    initial_fisheries_value: float = 1.0  # billion USD
    fisheries_growth_rate: float = 0.05  # %/year
    sustainable_harvest_rate: float = 0.7  # % of maximum sustainable yield
    
    # Aquaculture parameters
    initial_aquaculture_value: float = 0.5  # billion USD
    aquaculture_growth_rate: float = 0.08  # %/year
    sustainable_aquaculture_rate: float = 0.8  # % of carrying capacity
    
    # Marine tourism parameters
    initial_tourism_value: float = 0.3  # billion USD
    tourism_growth_rate: float = 0.1  # %/year
    tourism_carrying_capacity: float = 1.0  # million visitors/year
    
    # Marine renewable energy parameters
    initial_renewable_energy: float = 0.1  # GW
    renewable_energy_growth_rate: float = 0.15  # %/year
    maximum_potential: float = 5.0  # GW
    
    # Marine biotechnology parameters
    initial_biotech_value: float = 0.05  # billion USD
    biotech_growth_rate: float = 0.12  # %/year
    research_investment_rate: float = 0.1  # % of biotech value

class BlueEconomyModel:
    """Blue economy model for simulating marine economic activities."""
    
    def __init__(self, parameters: Optional[BlueEconomyParameters] = None):
        """Initialize the blue economy model with parameters."""
        self.parameters = parameters or BlueEconomyParameters()
        self._initialize_state()
    
    def _initialize_state(self):
        """Initialize the model state variables."""
        self.years = np.arange(
            self.parameters.start_year,
            self.parameters.end_year + 1,
            self.parameters.time_step
        )
        self.current_year = self.parameters.start_year
        
        # Initialize state variables
        self.fisheries_value = np.zeros(len(self.years))
        self.aquaculture_value = np.zeros(len(self.years))
        self.tourism_value = np.zeros(len(self.years))
        self.renewable_energy = np.zeros(len(self.years))
        self.biotech_value = np.zeros(len(self.years))
        self.total_value = np.zeros(len(self.years))
        
        # Set initial conditions
        self.fisheries_value[0] = self.parameters.initial_fisheries_value
        self.aquaculture_value[0] = self.parameters.initial_aquaculture_value
        self.tourism_value[0] = self.parameters.initial_tourism_value
        self.renewable_energy[0] = self.parameters.initial_renewable_energy
        self.biotech_value[0] = self.parameters.initial_biotech_value
        self.total_value[0] = (
            self.fisheries_value[0] +
            self.aquaculture_value[0] +
            self.tourism_value[0] +
            self.biotech_value[0]
        )
    
    def simulate_step(self) -> Dict[str, float]:
        """Simulate one time step of blue economy change."""
        if self.current_year >= self.parameters.end_year:
            raise ValueError("Simulation has reached end year")
        
        current_idx = np.where(self.years == self.current_year)[0][0]
        next_idx = current_idx + 1
        
        # Update fisheries value
        self.fisheries_value[next_idx] = (
            self.fisheries_value[current_idx] * 
            (1 + self.parameters.fisheries_growth_rate) *
            self.parameters.sustainable_harvest_rate
        )
        
        # Update aquaculture value
        self.aquaculture_value[next_idx] = (
            self.aquaculture_value[current_idx] * 
            (1 + self.parameters.aquaculture_growth_rate) *
            self.parameters.sustainable_aquaculture_rate
        )
        
        # Update tourism value
        self.tourism_value[next_idx] = (
            self.tourism_value[current_idx] * 
            (1 + self.parameters.tourism_growth_rate)
        )
        
        # Update renewable energy
        self.renewable_energy[next_idx] = min(
            self.renewable_energy[current_idx] * 
            (1 + self.parameters.renewable_energy_growth_rate),
            self.parameters.maximum_potential
        )
        
        # Update biotech value
        self.biotech_value[next_idx] = (
            self.biotech_value[current_idx] * 
            (1 + self.parameters.biotech_growth_rate) *
            (1 + self.parameters.research_investment_rate)
        )
        
        # Update total value
        self.total_value[next_idx] = (
            self.fisheries_value[next_idx] +
            self.aquaculture_value[next_idx] +
            self.tourism_value[next_idx] +
            self.biotech_value[next_idx]
        )
        
        # Update current year
        self.current_year += self.parameters.time_step
        
        return {
            'year': self.current_year,
            'fisheries_value': self.fisheries_value[next_idx],
            'aquaculture_value': self.aquaculture_value[next_idx],
            'tourism_value': self.tourism_value[next_idx],
            'renewable_energy': self.renewable_energy[next_idx],
            'biotech_value': self.biotech_value[next_idx],
            'total_value': self.total_value[next_idx]
        }
    
    def simulate_all(self) -> Dict[str, np.ndarray]:
        """Simulate the entire time period."""
        while self.current_year < self.parameters.end_year:
            self.simulate_step()
        
        return {
            'years': self.years,
            'fisheries_value': self.fisheries_value,
            'aquaculture_value': self.aquaculture_value,
            'tourism_value': self.tourism_value,
            'renewable_energy': self.renewable_energy,
            'biotech_value': self.biotech_value,
            'total_value': self.total_value
        }
    
    def get_current_state(self) -> Dict[str, float]:
        """Get the current state of the blue economy model."""
        current_idx = np.where(self.years == self.current_year)[0][0]
        return {
            'year': self.current_year,
            'fisheries_value': self.fisheries_value[current_idx],
            'aquaculture_value': self.aquaculture_value[current_idx],
            'tourism_value': self.tourism_value[current_idx],
            'renewable_energy': self.renewable_energy[current_idx],
            'biotech_value': self.biotech_value[current_idx],
            'total_value': self.total_value[current_idx]
        }
    
    def reset(self):
        """Reset the model to initial conditions."""
        self._initialize_state() 