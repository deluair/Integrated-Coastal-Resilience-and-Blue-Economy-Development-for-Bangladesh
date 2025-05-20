"""
Main simulation class for integrated coastal resilience and blue economy development.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .models.climate import ClimateModel, ClimateParameters
from .models.environment import EnvironmentalModel, EnvironmentalParameters
from .models.socioeconomic import SocioeconomicModel, SocioeconomicParameters
from .models.blue_economy import BlueEconomyModel, BlueEconomyParameters
from .models.policy import PolicyModel, PolicyParameters

class IntegratedSimulation:
    """Integrated simulation of coastal resilience and blue economy development."""
    
    def __init__(
        self,
        climate_params: Optional[ClimateParameters] = None,
        env_params: Optional[EnvironmentalParameters] = None,
        socio_params: Optional[SocioeconomicParameters] = None,
        blue_econ_params: Optional[BlueEconomyParameters] = None,
        policy_params: Optional[PolicyParameters] = None
    ):
        """Initialize the integrated simulation with parameters."""
        # Initialize individual models
        self.climate_model = ClimateModel(climate_params)
        self.env_model = EnvironmentalModel(env_params)
        self.socio_model = SocioeconomicModel(socio_params)
        self.blue_econ_model = BlueEconomyModel(blue_econ_params)
        self.policy_model = PolicyModel(policy_params)
        
        # Initialize integrated state
        self._initialize_state()
    
    def _initialize_state(self):
        """Initialize the integrated simulation state."""
        self.current_year = self.climate_model.parameters.start_year
        self.years = self.climate_model.years
        
        # Initialize integrated metrics
        self.resilience_index = np.zeros(len(self.years))
        self.sustainability_index = np.zeros(len(self.years))
        self.development_index = np.zeros(len(self.years))
        
        # Calculate initial indices
        self._update_indices(0)
    
    def _update_indices(self, idx: int):
        """Update integrated indices based on current model states."""
        # Get current states
        climate_state = self.climate_model.get_current_state()
        env_state = self.env_model.get_current_state()
        socio_state = self.socio_model.get_current_state()
        blue_econ_state = self.blue_econ_model.get_current_state()
        policy_state = self.policy_model.get_current_state()
        
        # Calculate resilience index (weighted average of key resilience indicators)
        self.resilience_index[idx] = (
            0.3 * (100 - climate_state['storm_surge_intensity']) +
            0.3 * env_state['mangrove_coverage'] +
            0.2 * socio_state['infrastructure_quality'] +
            0.2 * policy_state['overall_effectiveness']
        )
        
        # Calculate sustainability index (weighted average of sustainability indicators)
        self.sustainability_index[idx] = (
            0.25 * env_state['biodiversity_index'] +
            0.25 * env_state['water_quality_index'] +
            0.25 * blue_econ_state['total_value'] / blue_econ_state['total_value'] +
            0.25 * policy_state['monitoring_effectiveness']
        )
        
        # Calculate development index (weighted average of development indicators)
        self.development_index[idx] = (
            0.3 * socio_state['gdp'] +
            0.3 * blue_econ_state['total_value'] / blue_econ_state['total_value'] +
            0.2 * socio_state['employment_rate'] +
            0.2 * (100 - socio_state['poverty_rate'])
        )
    
    def simulate_step(self) -> Dict[str, float]:
        """Simulate one time step of the integrated system."""
        if self.current_year >= self.climate_model.parameters.end_year:
            raise ValueError("Simulation has reached end year")
        
        # Simulate individual model steps
        climate_state = self.climate_model.simulate_step()
        env_state = self.env_model.simulate_step()
        socio_state = self.socio_model.simulate_step()
        blue_econ_state = self.blue_econ_model.simulate_step()
        policy_state = self.policy_model.simulate_step()
        
        # Update current year
        self.current_year = climate_state['year']
        
        # Update integrated indices
        current_idx = np.where(self.years == self.current_year)[0][0]
        self._update_indices(current_idx)
        
        return {
            'year': self.current_year,
            'resilience_index': self.resilience_index[current_idx],
            'sustainability_index': self.sustainability_index[current_idx],
            'development_index': self.development_index[current_idx],
            'climate_state': climate_state,
            'environment_state': env_state,
            'socioeconomic_state': socio_state,
            'blue_economy_state': blue_econ_state,
            'policy_state': policy_state
        }
    
    def simulate_all(self) -> Dict[str, np.ndarray]:
        """Simulate the entire time period."""
        while self.current_year < self.climate_model.parameters.end_year:
            self.simulate_step()
        
        return {
            'years': self.years,
            'resilience_index': self.resilience_index,
            'sustainability_index': self.sustainability_index,
            'development_index': self.development_index,
            'climate_data': self.climate_model.simulate_all(),
            'environment_data': self.env_model.simulate_all(),
            'socioeconomic_data': self.socio_model.simulate_all(),
            'blue_economy_data': self.blue_econ_model.simulate_all(),
            'policy_data': self.policy_model.simulate_all()
        }
    
    def get_current_state(self) -> Dict[str, float]:
        """Get the current state of the integrated simulation."""
        current_idx = np.where(self.years == self.current_year)[0][0]
        return {
            'year': self.current_year,
            'resilience_index': self.resilience_index[current_idx],
            'sustainability_index': self.sustainability_index[current_idx],
            'development_index': self.development_index[current_idx],
            'climate_state': self.climate_model.get_current_state(),
            'environment_state': self.env_model.get_current_state(),
            'socioeconomic_state': self.socio_model.get_current_state(),
            'blue_economy_state': self.blue_econ_model.get_current_state(),
            'policy_state': self.policy_model.get_current_state()
        }
    
    def reset(self):
        """Reset all models to initial conditions."""
        self.climate_model.reset()
        self.env_model.reset()
        self.socio_model.reset()
        self.blue_econ_model.reset()
        self.policy_model.reset()
        self._initialize_state() 