"""
Policy model for simulating governance and policy interventions in coastal Bangladesh.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime

@dataclass
class PolicyParameters:
    """Parameters for policy model simulation."""
    start_year: int = 2024
    end_year: int = 2039
    time_step: int = 1  # years
    
    # Policy implementation parameters
    policy_effectiveness: float = 0.7  # % of intended impact
    implementation_delay: int = 2  # years
    coordination_efficiency: float = 0.8  # % of maximum possible
    
    # Financial parameters
    initial_budget: float = 1.0  # billion USD
    budget_growth_rate: float = 0.1  # %/year
    resource_utilization: float = 0.85  # % of allocated resources
    
    # Institutional parameters
    institutional_capacity: float = 0.7  # % of required capacity
    capacity_growth_rate: float = 0.05  # %/year
    stakeholder_engagement: float = 0.75  # % of potential engagement
    
    # Monitoring parameters
    monitoring_coverage: float = 0.8  # % of interventions
    data_quality: float = 0.85  # % of maximum quality
    evaluation_frequency: float = 0.9  # % of required evaluations

class PolicyModel:
    """Policy model for simulating governance and policy interventions."""
    
    def __init__(self, parameters: Optional[PolicyParameters] = None):
        """Initialize the policy model with parameters."""
        self.parameters = parameters or PolicyParameters()
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
        self.policy_impact = np.zeros(len(self.years))
        self.budget_utilization = np.zeros(len(self.years))
        self.institutional_performance = np.zeros(len(self.years))
        self.monitoring_effectiveness = np.zeros(len(self.years))
        self.overall_effectiveness = np.zeros(len(self.years))
        
        # Set initial conditions
        self.policy_impact[0] = self.parameters.policy_effectiveness
        self.budget_utilization[0] = self.parameters.resource_utilization
        self.institutional_performance[0] = self.parameters.institutional_capacity
        self.monitoring_effectiveness[0] = (
            self.parameters.monitoring_coverage *
            self.parameters.data_quality *
            self.parameters.evaluation_frequency
        )
        self.overall_effectiveness[0] = (
            self.policy_impact[0] *
            self.budget_utilization[0] *
            self.institutional_performance[0] *
            self.monitoring_effectiveness[0]
        )
    
    def simulate_step(self) -> Dict[str, float]:
        """Simulate one time step of policy change."""
        if self.current_year >= self.parameters.end_year:
            raise ValueError("Simulation has reached end year")
        
        current_idx = np.where(self.years == self.current_year)[0][0]
        next_idx = current_idx + 1
        
        # Update policy impact
        self.policy_impact[next_idx] = (
            self.policy_impact[current_idx] * 
            (1 + self.parameters.coordination_efficiency)
        )
        
        # Update budget utilization
        self.budget_utilization[next_idx] = (
            self.budget_utilization[current_idx] * 
            (1 + self.parameters.budget_growth_rate) *
            self.parameters.resource_utilization
        )
        
        # Update institutional performance
        self.institutional_performance[next_idx] = (
            self.institutional_performance[current_idx] * 
            (1 + self.parameters.capacity_growth_rate) *
            self.parameters.stakeholder_engagement
        )
        
        # Update monitoring effectiveness
        self.monitoring_effectiveness[next_idx] = (
            self.monitoring_effectiveness[current_idx] * 
            (1 + self.parameters.evaluation_frequency)
        )
        
        # Update overall effectiveness
        self.overall_effectiveness[next_idx] = (
            self.policy_impact[next_idx] *
            self.budget_utilization[next_idx] *
            self.institutional_performance[next_idx] *
            self.monitoring_effectiveness[next_idx]
        )
        
        # Update current year
        self.current_year += self.parameters.time_step
        
        return {
            'year': self.current_year,
            'policy_impact': self.policy_impact[next_idx],
            'budget_utilization': self.budget_utilization[next_idx],
            'institutional_performance': self.institutional_performance[next_idx],
            'monitoring_effectiveness': self.monitoring_effectiveness[next_idx],
            'overall_effectiveness': self.overall_effectiveness[next_idx]
        }
    
    def simulate_all(self) -> Dict[str, np.ndarray]:
        """Simulate the entire time period."""
        while self.current_year < self.parameters.end_year:
            self.simulate_step()
        
        return {
            'years': self.years,
            'policy_impact': self.policy_impact,
            'budget_utilization': self.budget_utilization,
            'institutional_performance': self.institutional_performance,
            'monitoring_effectiveness': self.monitoring_effectiveness,
            'overall_effectiveness': self.overall_effectiveness
        }
    
    def get_current_state(self) -> Dict[str, float]:
        """Get the current state of the policy model."""
        current_idx = np.where(self.years == self.current_year)[0][0]
        return {
            'year': self.current_year,
            'policy_impact': self.policy_impact[current_idx],
            'budget_utilization': self.budget_utilization[current_idx],
            'institutional_performance': self.institutional_performance[current_idx],
            'monitoring_effectiveness': self.monitoring_effectiveness[current_idx],
            'overall_effectiveness': self.overall_effectiveness[current_idx]
        }
    
    def reset(self):
        """Reset the model to initial conditions."""
        self._initialize_state() 