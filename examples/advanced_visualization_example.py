"""
Example script demonstrating the usage of advanced visualization features.
"""

import numpy as np
from coastal_resilience.visualization import SimulationVisualizer
from coastal_resilience.advanced_visualization import AdvancedVisualizer

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
    
    # Create visualizer instances
    basic_visualizer = SimulationVisualizer(sample_data)
    advanced_visualizer = AdvancedVisualizer(sample_data)
    
    # Generate and display basic plots
    print("Generating basic plots...")
    basic_visualizer.plot_indices()
    basic_visualizer.plot_climate_indicators()
    basic_visualizer.plot_environmental_indicators()
    basic_visualizer.plot_blue_economy_indicators()
    basic_visualizer.plot_socioeconomic_indicators()
    basic_visualizer.plot_policy_indicators()
    basic_visualizer.plot_correlation_matrix()
    
    # Generate and display advanced plots
    print("Generating advanced plots...")
    advanced_visualizer.plot_radar_chart(2024)  # Initial year
    advanced_visualizer.plot_radar_chart(2038)  # Final year
    advanced_visualizer.plot_trend_analysis('resilience_index')
    advanced_visualizer.plot_trend_analysis('sustainability_index')
    advanced_visualizer.plot_trend_analysis('development_index')
    advanced_visualizer.plot_pca_analysis()
    advanced_visualizer.plot_sensitivity_analysis('resilience_index')
    advanced_visualizer.plot_sensitivity_analysis('sustainability_index')
    advanced_visualizer.plot_sensitivity_analysis('development_index')
    
    # Save all plots
    print("Saving plots...")
    basic_visualizer.save_all_plots('output/visualization/basic')
    advanced_visualizer.save_all_plots('output/visualization/advanced')
    
    # Display summary table
    print("\nSummary Table:")
    print(basic_visualizer.create_summary_table())

if __name__ == "__main__":
    main() 