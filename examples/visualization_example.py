"""
Example script demonstrating the usage of the visualization module.
"""

import numpy as np
from coastal_resilience.visualization import SimulationVisualizer

def generate_sample_data(years: np.ndarray) -> dict:
    """Generate sample simulation data for demonstration."""
    n_years = len(years)
    
    # Generate sample data with realistic trends
    return {
        'years': years,
        'resilience_index': np.linspace(0.5, 0.8, n_years) + np.random.normal(0, 0.02, n_years),
        'sustainability_index': np.linspace(0.4, 0.75, n_years) + np.random.normal(0, 0.02, n_years),
        'development_index': np.linspace(0.3, 0.7, n_years) + np.random.normal(0, 0.02, n_years),
        
        'climate_data': {
            'sea_level': np.linspace(0, 0.3, n_years) + np.random.normal(0, 0.01, n_years),
            'temperature': np.linspace(0, 1.5, n_years) + np.random.normal(0, 0.1, n_years),
            'rainfall': np.linspace(0, 0.2, n_years) + np.random.normal(0, 0.05, n_years)
        },
        
        'environment_data': {
            'mangrove_coverage': np.linspace(0.4, 0.7, n_years) + np.random.normal(0, 0.02, n_years),
            'biodiversity_index': np.linspace(0.5, 0.8, n_years) + np.random.normal(0, 0.02, n_years),
            'water_quality_index': np.linspace(0.3, 0.6, n_years) + np.random.normal(0, 0.02, n_years)
        },
        
        'blue_economy_data': {
            'fisheries_value': np.linspace(1, 2, n_years) + np.random.normal(0, 0.1, n_years),
            'aquaculture_value': np.linspace(0.5, 1.5, n_years) + np.random.normal(0, 0.1, n_years),
            'tourism_value': np.linspace(0.3, 1.2, n_years) + np.random.normal(0, 0.1, n_years),
            'biotech_value': np.linspace(0.2, 0.8, n_years) + np.random.normal(0, 0.1, n_years),
            'total_value': np.linspace(2, 5.5, n_years) + np.random.normal(0, 0.2, n_years)
        },
        
        'socioeconomic_data': {
            'population': np.linspace(1, 1.3, n_years) + np.random.normal(0, 0.01, n_years),
            'gdp': np.linspace(1, 2, n_years) + np.random.normal(0, 0.05, n_years),
            'employment_rate': np.linspace(0.4, 0.6, n_years) + np.random.normal(0, 0.01, n_years),
            'poverty_rate': np.linspace(0.3, 0.1, n_years) + np.random.normal(0, 0.01, n_years)
        },
        
        'policy_data': {
            'policy_impact': np.linspace(0.3, 0.8, n_years) + np.random.normal(0, 0.02, n_years),
            'budget_utilization': np.linspace(0.4, 0.9, n_years) + np.random.normal(0, 0.02, n_years),
            'institutional_performance': np.linspace(0.3, 0.7, n_years) + np.random.normal(0, 0.02, n_years),
            'monitoring_effectiveness': np.linspace(0.4, 0.8, n_years) + np.random.normal(0, 0.02, n_years),
            'overall_effectiveness': np.linspace(0.35, 0.8, n_years) + np.random.normal(0, 0.02, n_years)
        }
    }

def main():
    # Generate sample data for 15 years
    years = np.arange(2024, 2039)
    sample_data = generate_sample_data(years)
    
    # Create visualizer instance
    visualizer = SimulationVisualizer(sample_data)
    
    # Generate and display all plots
    visualizer.plot_indices()
    visualizer.plot_climate_indicators()
    visualizer.plot_environmental_indicators()
    visualizer.plot_blue_economy_indicators()
    visualizer.plot_socioeconomic_indicators()
    visualizer.plot_policy_indicators()
    visualizer.plot_correlation_matrix()
    
    # Save all plots and summary data
    visualizer.save_all_plots('output/visualization')
    
    # Display summary table
    print("\nSummary Table:")
    print(visualizer.create_summary_table())

if __name__ == "__main__":
    main() 