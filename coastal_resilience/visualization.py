"""
Visualization module for analyzing and presenting simulation results.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import pandas as pd

class SimulationVisualizer:
    """Visualization tools for simulation results."""
    
    def __init__(self, simulation_results: Dict[str, np.ndarray]):
        """Initialize visualizer with simulation results."""
        self.results = simulation_results
        self.years = simulation_results['years']
        
        # Set style
        plt.style.use('seaborn-v0_8')  # Using a specific seaborn style version
        sns.set_theme()  # Set seaborn theme
    
    def plot_indices(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot the main indices over time."""
        plt.figure(figsize=figsize)
        
        plt.plot(self.years, self.results['resilience_index'], 
                label='Resilience Index', linewidth=2)
        plt.plot(self.years, self.results['sustainability_index'], 
                label='Sustainability Index', linewidth=2)
        plt.plot(self.years, self.results['development_index'], 
                label='Development Index', linewidth=2)
        
        plt.title('Integrated Coastal Development Indices Over Time')
        plt.xlabel('Year')
        plt.ylabel('Index Value')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def plot_climate_indicators(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot climate change indicators."""
        plt.figure(figsize=figsize)
        
        climate_data = self.results['climate_data']
        plt.plot(self.years, climate_data['sea_level'], 
                label='Sea Level Rise', linewidth=2)
        plt.plot(self.years, climate_data['temperature'], 
                label='Temperature', linewidth=2)
        plt.plot(self.years, climate_data['rainfall'], 
                label='Rainfall', linewidth=2)
        
        plt.title('Climate Change Indicators')
        plt.xlabel('Year')
        plt.ylabel('Change from Baseline (%)')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def plot_environmental_indicators(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot environmental indicators."""
        plt.figure(figsize=figsize)
        
        env_data = self.results['environment_data']
        plt.plot(self.years, env_data['mangrove_coverage'], 
                label='Mangrove Coverage', linewidth=2)
        plt.plot(self.years, env_data['biodiversity_index'], 
                label='Biodiversity Index', linewidth=2)
        plt.plot(self.years, env_data['water_quality_index'], 
                label='Water Quality Index', linewidth=2)
        
        plt.title('Environmental Indicators')
        plt.xlabel('Year')
        plt.ylabel('Index Value')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def plot_blue_economy_indicators(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot blue economy indicators."""
        plt.figure(figsize=figsize)
        
        blue_econ_data = self.results['blue_economy_data']
        plt.plot(self.years, blue_econ_data['fisheries_value'], 
                label='Fisheries Value', linewidth=2)
        plt.plot(self.years, blue_econ_data['aquaculture_value'], 
                label='Aquaculture Value', linewidth=2)
        plt.plot(self.years, blue_econ_data['tourism_value'], 
                label='Tourism Value', linewidth=2)
        plt.plot(self.years, blue_econ_data['biotech_value'], 
                label='Biotech Value', linewidth=2)
        
        plt.title('Blue Economy Indicators')
        plt.xlabel('Year')
        plt.ylabel('Value (Billion USD)')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def plot_socioeconomic_indicators(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot socioeconomic indicators."""
        plt.figure(figsize=figsize)
        
        socio_data = self.results['socioeconomic_data']
        plt.plot(self.years, socio_data['population'], 
                label='Population', linewidth=2)
        plt.plot(self.years, socio_data['gdp'], 
                label='GDP', linewidth=2)
        plt.plot(self.years, socio_data['employment_rate'], 
                label='Employment Rate', linewidth=2)
        plt.plot(self.years, socio_data['poverty_rate'], 
                label='Poverty Rate', linewidth=2)
        
        plt.title('Socioeconomic Indicators')
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def plot_policy_indicators(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot policy implementation indicators."""
        plt.figure(figsize=figsize)
        
        policy_data = self.results['policy_data']
        plt.plot(self.years, policy_data['policy_impact'], 
                label='Policy Impact', linewidth=2)
        plt.plot(self.years, policy_data['budget_utilization'], 
                label='Budget Utilization', linewidth=2)
        plt.plot(self.years, policy_data['institutional_performance'], 
                label='Institutional Performance', linewidth=2)
        plt.plot(self.years, policy_data['monitoring_effectiveness'], 
                label='Monitoring Effectiveness', linewidth=2)
        
        plt.title('Policy Implementation Indicators')
        plt.xlabel('Year')
        plt.ylabel('Effectiveness (%)')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def create_summary_table(self) -> pd.DataFrame:
        """Create a summary table of key indicators."""
        summary_data = {
            'Year': self.years,
            'Resilience Index': self.results['resilience_index'],
            'Sustainability Index': self.results['sustainability_index'],
            'Development Index': self.results['development_index'],
            'Sea Level Rise': self.results['climate_data']['sea_level'],
            'Mangrove Coverage': self.results['environment_data']['mangrove_coverage'],
            'GDP': self.results['socioeconomic_data']['gdp'],
            'Blue Economy Value': self.results['blue_economy_data']['total_value'],
            'Policy Effectiveness': self.results['policy_data']['overall_effectiveness']
        }
        
        return pd.DataFrame(summary_data)
    
    def plot_correlation_matrix(self, figsize: Tuple[int, int] = (12, 8)):
        """Plot correlation matrix of key indicators."""
        summary_df = self.create_summary_table()
        correlation_matrix = summary_df.corr()
        
        plt.figure(figsize=figsize)
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix of Key Indicators')
        
        return plt.gcf()
    
    def save_all_plots(self, output_dir: str):
        """Save all plots to the specified directory."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate and save all plots
        self.plot_indices().savefig(f'{output_dir}/indices.png')
        self.plot_climate_indicators().savefig(f'{output_dir}/climate.png')
        self.plot_environmental_indicators().savefig(f'{output_dir}/environment.png')
        self.plot_blue_economy_indicators().savefig(f'{output_dir}/blue_economy.png')
        self.plot_socioeconomic_indicators().savefig(f'{output_dir}/socioeconomic.png')
        self.plot_policy_indicators().savefig(f'{output_dir}/policy.png')
        self.plot_correlation_matrix().savefig(f'{output_dir}/correlation.png')
        
        # Save summary table
        self.create_summary_table().to_csv(f'{output_dir}/summary.csv', index=False) 