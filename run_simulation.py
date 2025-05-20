"""
Main script to run the integrated coastal resilience simulation.
"""

import numpy as np
from coastal_resilience.simulation import IntegratedSimulation
from coastal_resilience.visualization import SimulationVisualizer
from coastal_resilience.advanced_visualization import AdvancedVisualizer
import os
import json
from datetime import datetime

def run_simulation():
    """Run the integrated simulation and save results."""
    print("Starting simulation...")
    
    # Initialize simulation
    simulation = IntegratedSimulation()
    
    # Run simulation
    results = simulation.simulate_all()
    
    # Add aggregate keys for advanced visualization
    # Climate overall_impact
    climate_data = results['climate_data']
    climate_arrays = [np.array(climate_data[k]) for k in climate_data if k != 'year']
    climate_data['overall_impact'] = np.mean(climate_arrays, axis=0)

    # Environment overall_health
    environment_data = results['environment_data']
    env_arrays = [np.array(environment_data[k]) for k in environment_data if k != 'year']
    environment_data['overall_health'] = np.mean(env_arrays, axis=0)

    # Socioeconomic overall_development
    socioeconomic_data = results['socioeconomic_data']
    socio_arrays = [np.array(socioeconomic_data[k]) for k in socioeconomic_data if k != 'year']
    socioeconomic_data['overall_development'] = np.mean(socio_arrays, axis=0)
    
    # Create output directories
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/simulation_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save raw results
    print("Saving simulation results...")
    np.save(f"{output_dir}/simulation_results.npy", results)
    
    # Convert results to JSON for better readability
    json_results = {
        'years': results['years'].tolist(),
        'resilience_index': results['resilience_index'].tolist(),
        'sustainability_index': results['sustainability_index'].tolist(),
        'development_index': results['development_index'].tolist(),
        'climate_data': {
            k: v.tolist() for k, v in results['climate_data'].items()
        },
        'environment_data': {
            k: v.tolist() for k, v in results['environment_data'].items()
        },
        'blue_economy_data': {
            k: v.tolist() for k, v in results['blue_economy_data'].items()
        },
        'socioeconomic_data': {
            k: v.tolist() for k, v in results['socioeconomic_data'].items()
        },
        'policy_data': {
            k: v.tolist() for k, v in results['policy_data'].items()
        }
    }
    
    with open(f"{output_dir}/simulation_results.json", 'w') as f:
        json.dump(json_results, f, indent=2)
    
    # Generate visualizations
    print("Generating visualizations...")
    basic_visualizer = SimulationVisualizer(results)
    advanced_visualizer = AdvancedVisualizer(results)
    
    # Save basic plots
    basic_visualizer.save_all_plots(f"{output_dir}/visualization/basic")
    
    # Save advanced plots
    advanced_visualizer.save_all_plots(f"{output_dir}/visualization/advanced")
    
    # Save summary table
    summary_table = basic_visualizer.create_summary_table()
    summary_table.to_csv(f"{output_dir}/summary.csv", index=False)
    
    print(f"Simulation completed. Results saved to {output_dir}")
    return output_dir

if __name__ == "__main__":
    output_dir = run_simulation() 