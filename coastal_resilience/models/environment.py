"""
Environmental model for simulating ecosystem dynamics in coastal Bangladesh.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime

@dataclass
class EnvironmentalParameters:
    """Parameters for environmental model simulation."""
    start_year: int = 2024
    end_year: int = 2039
    time_step: int = 1  # years
    
    # Mangrove parameters
    mangrove_degradation_rate: float = 0.013  # %/year
    mangrove_restoration_rate: float = 0.02  # %/year
    mangrove_carbon_sequestration: float = 0.5  # tons CO2/ha/year
    
    # Salinity parameters
    salinity_intrusion_rate: float = 0.03  # %/year
    groundwater_salinity_increase: float = 0.02  # %/year
    
    # Biodiversity parameters
    species_loss_rate: float = 0.01  # %/year
    habitat_fragmentation_rate: float = 0.015  # %/year
    
    # Water quality parameters
    water_pollution_increase: float = 0.02  # %/year
    nutrient_loading_increase: float = 0.025  # %/year

class EnvironmentalModel:
    """Environmental model for simulating ecosystem dynamics."""
    
    def __init__(self, parameters: Optional[EnvironmentalParameters] = None):
        """Initialize the environmental model with parameters."""
        self.parameters = parameters or EnvironmentalParameters()
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
        self.mangrove_coverage = np.zeros(len(self.years))
        self.salinity_levels = np.zeros(len(self.years))
        self.biodiversity_index = np.zeros(len(self.years))
        self.water_quality_index = np.zeros(len(self.years))
        self.carbon_sequestration = np.zeros(len(self.years))
        
        # Set initial conditions
        self.mangrove_coverage[0] = 100.0  # % relative to 2024
        self.salinity_levels[0] = 100.0  # % relative to 2024
        self.biodiversity_index[0] = 100.0  # % relative to 2024
        self.water_quality_index[0] = 100.0  # % relative to 2024
        self.carbon_sequestration[0] = 0.0  # tons CO2
    
    def simulate_step(self) -> Dict[str, float]:
        """Simulate one time step of environmental change."""
        if self.current_year >= self.parameters.end_year:
            raise ValueError("Simulation has reached end year")
        
        current_idx = np.where(self.years == self.current_year)[0][0]
        next_idx = current_idx + 1
        
        # Update mangrove coverage
        self.mangrove_coverage[next_idx] = (
            self.mangrove_coverage[current_idx] * 
            (1 - self.parameters.mangrove_degradation_rate) +
            self.parameters.mangrove_restoration_rate
        )
        
        # Update salinity levels
        self.salinity_levels[next_idx] = (
            self.salinity_levels[current_idx] * 
            (1 + self.parameters.salinity_intrusion_rate)
        )
        
        # Update biodiversity index
        self.biodiversity_index[next_idx] = (
            self.biodiversity_index[current_idx] * 
            (1 - self.parameters.species_loss_rate - 
             self.parameters.habitat_fragmentation_rate)
        )
        
        # Update water quality index
        self.water_quality_index[next_idx] = (
            self.water_quality_index[current_idx] * 
            (1 - self.parameters.water_pollution_increase - 
             self.parameters.nutrient_loading_increase)
        )
        
        # Update carbon sequestration
        self.carbon_sequestration[next_idx] = (
            self.carbon_sequestration[current_idx] +
            self.mangrove_coverage[next_idx] * 
            self.parameters.mangrove_carbon_sequestration
        )
        
        # Update current year
        self.current_year += self.parameters.time_step
        
        return {
            'year': self.current_year,
            'mangrove_coverage': self.mangrove_coverage[next_idx],
            'salinity_levels': self.salinity_levels[next_idx],
            'biodiversity_index': self.biodiversity_index[next_idx],
            'water_quality_index': self.water_quality_index[next_idx],
            'carbon_sequestration': self.carbon_sequestration[next_idx]
        }
    
    def simulate_all(self) -> Dict[str, np.ndarray]:
        """Simulate the entire time period."""
        while self.current_year < self.parameters.end_year:
            self.simulate_step()
        
        return {
            'years': self.years,
            'mangrove_coverage': self.mangrove_coverage,
            'salinity_levels': self.salinity_levels,
            'biodiversity_index': self.biodiversity_index,
            'water_quality_index': self.water_quality_index,
            'carbon_sequestration': self.carbon_sequestration
        }
    
    def get_current_state(self) -> Dict[str, float]:
        """Get the current state of the environmental model."""
        current_idx = np.where(self.years == self.current_year)[0][0]
        return {
            'year': self.current_year,
            'mangrove_coverage': self.mangrove_coverage[current_idx],
            'salinity_levels': self.salinity_levels[current_idx],
            'biodiversity_index': self.biodiversity_index[current_idx],
            'water_quality_index': self.water_quality_index[current_idx],
            'carbon_sequestration': self.carbon_sequestration[current_idx]
        }
    
    def reset(self):
        """Reset the model to initial conditions."""
        self._initialize_state() 