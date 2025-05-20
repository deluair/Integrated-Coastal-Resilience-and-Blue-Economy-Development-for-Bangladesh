"""
Advanced visualization tools for simulation results analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import pandas as pd
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class AdvancedVisualizer:
    """Advanced visualization tools for in-depth analysis of simulation results."""
    
    def __init__(self, simulation_results: Dict[str, np.ndarray]):
        """Initialize advanced visualizer with simulation results."""
        self.results = simulation_results
        self.years = simulation_results['years']
        
        # Set style
        plt.style.use('seaborn-v0_8')  # Using a specific seaborn style version
        sns.set_theme()  # Set seaborn theme
    
    def plot_radar_chart(self, year: int, figsize: Tuple[int, int] = (10, 10)):
        """Create a radar chart of key indicators for a specific year."""
        # Get data for the specified year
        year_idx = np.where(self.years == year)[0][0]
        
        # Prepare data
        categories = ['Resilience', 'Sustainability', 'Development', 
                     'Climate', 'Environment', 'Socioeconomic']
        values = [
            self.results['resilience_index'][year_idx],
            self.results['sustainability_index'][year_idx],
            self.results['development_index'][year_idx],
            self.results['climate_data']['overall_impact'][year_idx],
            self.results['environment_data']['overall_health'][year_idx],
            self.results['socioeconomic_data']['overall_development'][year_idx]
        ]
        
        # Number of variables
        N = len(categories)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Add the first value to close the loop
        values += values[:1]
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
        
        # Plot data
        ax.plot(angles, values, linewidth=2, linestyle='solid')
        ax.fill(angles, values, alpha=0.4)
        
        # Set category labels
        plt.xticks(angles[:-1], categories)
        
        # Set title
        plt.title(f'Key Indicators - Year {year}')
        
        return fig
    
    def plot_trend_analysis(self, indicator: str, window: int = 5, 
                           figsize: Tuple[int, int] = (12, 6)):
        """Plot trend analysis with moving average for a specific indicator."""
        plt.figure(figsize=figsize)
        
        # Get data
        data = self.results[indicator]
        
        # Calculate moving average
        moving_avg = pd.Series(data).rolling(window=window).mean()
        
        # Plot
        plt.plot(self.years, data, label='Actual', alpha=0.5)
        plt.plot(self.years, moving_avg, label=f'{window}-Year Moving Average', 
                linewidth=2)
        
        plt.title(f'Trend Analysis - {indicator}')
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def perform_pca_analysis(self, n_components: int = 2, 
                           figsize: Tuple[int, int] = (10, 8)):
        """Perform Principal Component Analysis on the data."""
        # Prepare data
        data = pd.DataFrame({
            'Resilience': self.results['resilience_index'],
            'Sustainability': self.results['sustainability_index'],
            'Development': self.results['development_index'],
            'Climate': self.results['climate_data']['overall_impact'],
            'Environment': self.results['environment_data']['overall_health'],
            'Socioeconomic': self.results['socioeconomic_data']['overall_development']
        })
        
        # Standardize data
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        
        # Perform PCA
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(scaled_data)
        
        # Create plot
        plt.figure(figsize=figsize)
        plt.scatter(pca_result[:, 0], pca_result[:, 1], c=self.years, cmap='viridis')
        plt.colorbar(label='Year')
        
        # Add labels for each point
        for i, year in enumerate(self.years):
            plt.annotate(str(year), (pca_result[i, 0], pca_result[i, 1]))
        
        plt.title('PCA Analysis of Key Indicators')
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        
        return plt.gcf()
    
    def plot_sensitivity_analysis(self, base_value: float, 
                                variations: List[float] = [-0.2, -0.1, 0.1, 0.2],
                                figsize: Tuple[int, int] = (12, 8)):
        """Plot sensitivity analysis for key parameters."""
        plt.figure(figsize=figsize)
        
        # Parameters to analyze
        parameters = ['climate_impact', 'environment_health', 'socioeconomic_development']
        
        for param in parameters:
            values = []
            for var in variations:
                modified_value = base_value * (1 + var)
                values.append(modified_value)
            
            plt.plot(variations, values, marker='o', label=param)
        
        plt.title('Sensitivity Analysis of Key Parameters')
        plt.xlabel('Variation from Base Value')
        plt.ylabel('Modified Value')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
    
    def save_all_plots(self, output_dir: str):
        """Save all advanced analysis plots to the specified directory."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save radar chart for the last year
        self.plot_radar_chart(self.years[-1]).savefig(f'{output_dir}/radar_chart.png')
        
        # Save trend analysis for key indicators
        self.plot_trend_analysis('resilience_index').savefig(f'{output_dir}/resilience_trend.png')
        self.plot_trend_analysis('sustainability_index').savefig(f'{output_dir}/sustainability_trend.png')
        self.plot_trend_analysis('development_index').savefig(f'{output_dir}/development_trend.png')
        
        # Save PCA analysis
        self.perform_pca_analysis().savefig(f'{output_dir}/pca_analysis.png')
        
        # Save sensitivity analysis
        self.plot_sensitivity_analysis(1.0).savefig(f'{output_dir}/sensitivity_analysis.png') 