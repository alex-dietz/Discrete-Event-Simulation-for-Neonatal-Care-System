import os
import pandas as pd
def filter_occupancy(occupancy_data, warm_up_time):
    """Filter occupancy data to include only values after the warm-up time."""
    times, occupancies = occupancy_data
    filtered_occupancy = [occupancy for time, occupancy in zip(times, occupancies) if time > warm_up_time]
    return filtered_occupancy

def save_occupancy_by_hospital(hospitals, filename, run_id):
    output_folder = os.path.dirname(filename)
    os.makedirs(output_folder, exist_ok=True)
    csv_path = filename + '.csv'
    
    all_data = []
    for hospital in hospitals:
        occupancy_monitor = hospital.beds.occupancy
        times, levels = occupancy_monitor.tx()
        for time, level in zip(times, levels):
            all_data.append([run_id, time, hospital.hospital_name, hospital.ward_level, level])
    
    df = pd.DataFrame(all_data, columns=['run_id', 'start_date', 'hospital', 'ward_level', 'occupancy'])
    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_path, mode='w', header=True, index=False)



def build_file_path(base_path, base_file_name, number_runs, **settings):
    # Initialize the file name with the base
    file_name = base_file_name

    # Append activated settings and their values
    for key, value in settings.items():
        if value:  # Include only activated settings
            if key == 'hospitalScenario' and value < 0:
                # Explicitly handle the hospitalScenario key
                file_name += f'_{key}_{value}'
            elif 'Change' not in key:  # Exclude percentage change keys
                file_name += f'_{key}'
            elif value != 0:  # For percentage change values other than 1
                file_name += f'_{key}_{value}'

    # Append number of runs
    file_name += f'_runs_{number_runs}'
    
 
    
    # Join with base path
    file_path = os.path.join(base_path, file_name)
    
    return file_path
