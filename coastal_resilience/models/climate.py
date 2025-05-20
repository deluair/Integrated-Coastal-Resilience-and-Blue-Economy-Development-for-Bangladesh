"""
Climate model for simulating climate change impacts on coastal Bangladesh.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime

@dataclass
class ClimateParameters:
    """Parameters for climate model simulation."""
    start_year: int = 2024
    end_year: int = 2039
    time_step: int = 1  # years
    sea_level_rise_rate: float = 0.5  # cm/year
    temperature_increase_rate: float = 0.03  # °C/year
    rainfall_change_rate: float = 0.02  # %/year
    cyclone_frequency_change: float = 0.05  # %/year
    storm_surge_intensity_change: float = 0.03  # %/year

class ClimateModel:
    """Climate model for simulating climate change impacts."""
    
    def __init__(self, parameters: Optional[ClimateParameters] = None):
        """Initialize the climate model with parameters."""
        self.parameters = parameters or ClimateParameters()
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
        self.sea_level = np.zeros(len(self.years))
        self.temperature = np.zeros(len(self.years))
        self.rainfall = np.zeros(len(self.years))
        self.cyclone_frequency = np.zeros(len(self.years))
        self.storm_surge_intensity = np.zeros(len(self.years))
        
        # Set initial conditions
        self.sea_level[0] = 0.0  # cm relative to 2024
        self.temperature[0] = 0.0  # °C relative to 2024
        self.rainfall[0] = 100.0  # % relative to 2024
        self.cyclone_frequency[0] = 100.0  # % relative to 2024
        self.storm_surge_intensity[0] = 100.0  # % relative to 2024
    
    def simulate_step(self) -> Dict[str, float]:
        """Simulate one time step of climate change."""
        if self.current_year >= self.parameters.end_year:
            raise ValueError("Simulation has reached end year")
        
        current_idx = np.where(self.years == self.current_year)[0][0]
        next_idx = current_idx + 1
        
        # Update state variables
        self.sea_level[next_idx] = (
            self.sea_level[current_idx] + 
            self.parameters.sea_level_rise_rate
        )
        
        self.temperature[next_idx] = (
            self.temperature[current_idx] + 
            self.parameters.temperature_increase_rate
        )
        
        self.rainfall[next_idx] = (
            self.rainfall[current_idx] * 
            (1 + self.parameters.rainfall_change_rate)
        )
        
        self.cyclone_frequency[next_idx] = (
            self.cyclone_frequency[current_idx] * 
            (1 + self.parameters.cyclone_frequency_change)
        )
        
        self.storm_surge_intensity[next_idx] = (
            self.storm_surge_intensity[current_idx] * 
            (1 + self.parameters.storm_surge_intensity_change)
        )
        
        # Update current year
        self.current_year += self.parameters.time_step
        
        return {
            'year': self.current_year,
            'sea_level': self.sea_level[next_idx],
            'temperature': self.temperature[next_idx],
            'rainfall': self.rainfall[next_idx],
            'cyclone_frequency': self.cyclone_frequency[next_idx],
            'storm_surge_intensity': self.storm_surge_intensity[next_idx]
        }
    
    def simulate_all(self) -> Dict[str, np.ndarray]:
        """Simulate the entire time period."""
        while self.current_year < self.parameters.end_year:
            self.simulate_step()
        
        return {
            'years': self.years,
            'sea_level': self.sea_level,
            'temperature': self.temperature,
            'rainfall': self.rainfall,
            'cyclone_frequency': self.cyclone_frequency,
            'storm_surge_intensity': self.storm_surge_intensity
        }
    
    def get_current_state(self) -> Dict[str, float]:
        """Get the current state of the climate model."""
        current_idx = np.where(self.years == self.current_year)[0][0]
        return {
            'year': self.current_year,
            'sea_level': self.sea_level[current_idx],
            'temperature': self.temperature[current_idx],
            'rainfall': self.rainfall[current_idx],
            'cyclone_frequency': self.cyclone_frequency[current_idx],
            'storm_surge_intensity': self.storm_surge_intensity[current_idx]
        }
    
    def reset(self):
        """Reset the model to initial conditions."""
        self._initialize_state() 