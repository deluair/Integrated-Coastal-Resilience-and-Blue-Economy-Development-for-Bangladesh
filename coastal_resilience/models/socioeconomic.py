"""
Socioeconomic model for simulating population and economic dynamics in coastal Bangladesh.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime

@dataclass
class SocioeconomicParameters:
    """Parameters for socioeconomic model simulation."""
    start_year: int = 2024
    end_year: int = 2039
    time_step: int = 1  # years
    
    # Population parameters
    initial_population: float = 35.0  # million
    population_growth_rate: float = 0.015  # %/year
    climate_migration_rate: float = 0.02  # %/year
    
    # Economic parameters
    initial_gdp: float = 3.0  # % of national GDP
    gdp_growth_rate: float = 0.06  # %/year
    blue_economy_share: float = 0.03  # % of coastal GDP
    
    # Infrastructure parameters
    infrastructure_damage_rate: float = 0.05  # %/year
    infrastructure_investment_rate: float = 0.08  # %/year
    
    # Livelihood parameters
    employment_growth_rate: float = 0.04  # %/year
    poverty_reduction_rate: float = 0.03  # %/year

class SocioeconomicModel:
    """Socioeconomic model for simulating population and economic dynamics."""
    
    def __init__(self, parameters: Optional[SocioeconomicParameters] = None):
        """Initialize the socioeconomic model with parameters."""
        self.parameters = parameters or SocioeconomicParameters()
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
        self.population = np.zeros(len(self.years))
        self.gdp = np.zeros(len(self.years))
        self.blue_economy = np.zeros(len(self.years))
        self.infrastructure_quality = np.zeros(len(self.years))
        self.employment_rate = np.zeros(len(self.years))
        self.poverty_rate = np.zeros(len(self.years))
        
        # Set initial conditions
        self.population[0] = self.parameters.initial_population
        self.gdp[0] = self.parameters.initial_gdp
        self.blue_economy[0] = self.gdp[0] * self.parameters.blue_economy_share
        self.infrastructure_quality[0] = 100.0  # % relative to 2024
        self.employment_rate[0] = 100.0  # % relative to 2024
        self.poverty_rate[0] = 100.0  # % relative to 2024
    
    def simulate_step(self) -> Dict[str, float]:
        """Simulate one time step of socioeconomic change."""
        if self.current_year >= self.parameters.end_year:
            raise ValueError("Simulation has reached end year")
        
        current_idx = np.where(self.years == self.current_year)[0][0]
        next_idx = current_idx + 1
        
        # Update population
        self.population[next_idx] = (
            self.population[current_idx] * 
            (1 + self.parameters.population_growth_rate - 
             self.parameters.climate_migration_rate)
        )
        
        # Update GDP
        self.gdp[next_idx] = (
            self.gdp[current_idx] * 
            (1 + self.parameters.gdp_growth_rate)
        )
        
        # Update blue economy
        self.blue_economy[next_idx] = (
            self.gdp[next_idx] * 
            self.parameters.blue_economy_share
        )
        
        # Update infrastructure quality
        self.infrastructure_quality[next_idx] = (
            self.infrastructure_quality[current_idx] * 
            (1 - self.parameters.infrastructure_damage_rate + 
             self.parameters.infrastructure_investment_rate)
        )
        
        # Update employment rate
        self.employment_rate[next_idx] = (
            self.employment_rate[current_idx] * 
            (1 + self.parameters.employment_growth_rate)
        )
        
        # Update poverty rate
        self.poverty_rate[next_idx] = (
            self.poverty_rate[current_idx] * 
            (1 - self.parameters.poverty_reduction_rate)
        )
        
        # Update current year
        self.current_year += self.parameters.time_step
        
        return {
            'year': self.current_year,
            'population': self.population[next_idx],
            'gdp': self.gdp[next_idx],
            'blue_economy': self.blue_economy[next_idx],
            'infrastructure_quality': self.infrastructure_quality[next_idx],
            'employment_rate': self.employment_rate[next_idx],
            'poverty_rate': self.poverty_rate[next_idx]
        }
    
    def simulate_all(self) -> Dict[str, np.ndarray]:
        """Simulate the entire time period."""
        while self.current_year < self.parameters.end_year:
            self.simulate_step()
        
        return {
            'years': self.years,
            'population': self.population,
            'gdp': self.gdp,
            'blue_economy': self.blue_economy,
            'infrastructure_quality': self.infrastructure_quality,
            'employment_rate': self.employment_rate,
            'poverty_rate': self.poverty_rate
        }
    
    def get_current_state(self) -> Dict[str, float]:
        """Get the current state of the socioeconomic model."""
        current_idx = np.where(self.years == self.current_year)[0][0]
        return {
            'year': self.current_year,
            'population': self.population[current_idx],
            'gdp': self.gdp[current_idx],
            'blue_economy': self.blue_economy[current_idx],
            'infrastructure_quality': self.infrastructure_quality[current_idx],
            'employment_rate': self.employment_rate[current_idx],
            'poverty_rate': self.poverty_rate[current_idx]
        }
    
    def reset(self):
        """Reset the model to initial conditions."""
        self._initialize_state() 