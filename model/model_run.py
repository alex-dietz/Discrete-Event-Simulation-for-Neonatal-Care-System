import os

import numpy as np
import pandas as pd
import csv
from multiprocessing import Pool
import salabim as sim
from config.run_config import *
from config.constants import *

from patient import *
from hospital import *
from patient_arrival import *
from utils import *
def run_simulation(args):
    '''
    Run the simulation with the given seed and run_id.
    Initiates hospitals and patient arrivals
    '''
    seed, run_id, output_folder = args
    global env, NICU_hospitals, high_care_hospitals, medium_care_hospitals, outside_region, hospital_dict, admission_log

    env = sim.Environment(time_unit='days',trace=True)
    #env.animate(True)
    sim.random_seed(seed)
    #set np random seed
    np.random.seed(seed)

    print(f"RUN ID: {run_id}, SEED: {seed}")

    admission_log = []
    if HOSPITAL_SCENARIO == -1:
        
        hospital_scenario = HOSPITALS_2016
    elif HOSPITAL_SCENARIO == 0:
        hospital_scenario = HOSPITALS_WITHOUT_CLOSURE 
    else:
        hospital_scenario = HOSPITALS_WITH_CLOSURE


    ward_levels = sorted(set(hospital['ward_level'] for hospital in hospital_scenario))
    hospital_dict = {}
    for ward_level in ward_levels:
        hospital_dict[f"{ward_level}_care_hospitals"] = [
            Hospital(hospital_name=hosp['hospital_name'], ward_level=ward_level, beds=hosp['beds'], region=hosp['region'])
            for hosp in hospital_scenario if hosp['ward_level'] == ward_level
        ]

    NICU_hospitals = hospital_dict['NICU_care_hospitals']
    high_care_hospitals = hospital_dict['high_care_hospitals']
    medium_care_hospitals = hospital_dict['medium_care_hospitals']
    outside_region = Hospital(hospital_name='outside_region', ward_level='outside_region', beds=OUTSIDE_REGION_BEDS, region='outside_region')
    
    PatientArrival(type='inside_region', run_id=run_id, hospital_dict=hospital_dict,outside_region_hospital =outside_region, admission_log=admission_log)
    if DEMAND_SCENARIO and DEMAND_SCENARIO_ARRIVAL_RATE != 0:
        PatientArrival(type='outside_region', run_id=run_id, hospital_dict=hospital_dict,outside_region_hospital =outside_region, admission_log=admission_log)
    if NICU_23WEEKS_SCENARIO:
        PatientArrival(type='23_weeks', run_id=run_id, hospital_dict=hospital_dict,outside_region_hospital =outside_region, admission_log=admission_log)
    env.run(till=DAYS + WARM_UP_TIME)

    occupancy_filename = build_file_path(output_folder, 'occupancy_by_hospital', NUMBER_RUNS,
                                            hospitalScenario=HOSPITAL_SCENARIO,
                                            demandScenario=DEMAND_SCENARIO,
                                            
                                            nicu23WeeksScenario=NICU_23WEEKS_SCENARIO,
                                            nicuAssignmentLever=NICU_ASSIGNMENT_LEVER,
                                            nicuAssignmentPercentageChange=NICU_ASSIGNMENT_PERCENTAGE_CHANGE,
                                            highCareAssignmentLever=HIGH_CARE_ASSIGNMENT_LEVER,
                                            highCareAssignmentPercentageChange=HIGH_CARE_ASSIGNMENT_PERCENTAGE_CHANGE,
                                            losLever=LOS_LEVER,
                                            losPercentageChange=LOS_PERCENTAGE_CHANGE,
                                            cpapLever=CPAP_LEVER,
                                            cpapPercentageChange=CPAP_PERCENTAGE_CHANGE,
                                            pathwayLever=PATHWAY_LEVER,
                                            pathwayLeverChange=PATHWAY_LEVER_LOS_CHANGE,
                                            phototherapyIntervention=PHOTOTHERAPY_INTERVENTION,
                                            sepsisIntervention=SEPSIS_INTERVENTION,
                                            nicuThresholdLever=NICU_THRESHOLD_LEVER,
                                            nicuThresholdLeverChange=NICU_THRESHOLD_LEVER_CHANGE,
                                            nicuWaitTimeLever = NICU_WAIT_TIME_LEVER,
                                            nicuWaitTimeLeverChange = NICU_WAIT_TIME_LEVER_CHANGE,
                                            ) 
    save_occupancy_by_hospital(NICU_hospitals + high_care_hospitals + medium_care_hospitals, occupancy_filename, run_id)

    for hospital in NICU_hospitals + high_care_hospitals + medium_care_hospitals:
        occupancy_after_warmup = filter_occupancy(hospital.beds.occupancy.tx(), WARM_UP_TIME)
        print(f'Name: {hospital.hospital_name}, Level: {hospital.ward_level}, Occupancy: {np.mean(occupancy_after_warmup)}')

    # Average occupancy across wards
    for ward_level in ward_levels:
        hospitals = hospital_dict[f"{ward_level}_care_hospitals"]
        occupancies = [filter_occupancy(hospital.beds.occupancy.tx(), WARM_UP_TIME) for hospital in hospitals]
        average_occupancy = np.mean([np.mean(occ) for occ in occupancies])
        print(f'Average occupancy for {ward_level} care: {average_occupancy}')

    return admission_log


if __name__ == '__main__':
    output_folder = './model/outputs'
    os.makedirs(output_folder, exist_ok=True)
    
    # Remove old occupancy csv
    occupancy_csv_path = build_file_path(
        output_folder, 'occupancy_by_hospital', NUMBER_RUNS,
        hospitalScenario=HOSPITAL_SCENARIO,
        demandScenario=DEMAND_SCENARIO,        
        nicu23WeeksScenario=NICU_23WEEKS_SCENARIO,
        nicuAssignmentLever=NICU_ASSIGNMENT_LEVER,
        nicuAssignmentPercentageChange=NICU_ASSIGNMENT_PERCENTAGE_CHANGE,
        highCareAssignmentLever=HIGH_CARE_ASSIGNMENT_LEVER,
        highCareAssignmentPercentageChange=HIGH_CARE_ASSIGNMENT_PERCENTAGE_CHANGE,
        losLever=LOS_LEVER,
        losPercentageChange=LOS_PERCENTAGE_CHANGE,
        cpapLever=CPAP_LEVER,
        cpapPercentageChange=CPAP_PERCENTAGE_CHANGE,
        pathwayLever=PATHWAY_LEVER,
        pathwayLeverChange=PATHWAY_LEVER_LOS_CHANGE,
        phototherapyIntervention=PHOTOTHERAPY_INTERVENTION,
        sepsisIntervention=SEPSIS_INTERVENTION,
        nicuThresholdLever=NICU_THRESHOLD_LEVER,
        nicuThresholdLeverChange=NICU_THRESHOLD_LEVER_CHANGE,
        nicuWaitTimeLever = NICU_WAIT_TIME_LEVER,
        nicuWaitTimeLeverChange = NICU_WAIT_TIME_LEVER_CHANGE,
    ) + '.csv'
    print(occupancy_csv_path)
    admission_csv_path = build_file_path(
        output_folder, 'admission_log', NUMBER_RUNS,
        hospitalScenario=HOSPITAL_SCENARIO,
        demandScenario=DEMAND_SCENARIO,        
        nicu23WeeksScenario=NICU_23WEEKS_SCENARIO,
        nicuAssignmentLever=NICU_ASSIGNMENT_LEVER,
        nicuAssignmentPercentageChange=NICU_ASSIGNMENT_PERCENTAGE_CHANGE,
        highCareAssignmentLever=HIGH_CARE_ASSIGNMENT_LEVER,
        highCareAssignmentPercentageChange=HIGH_CARE_ASSIGNMENT_PERCENTAGE_CHANGE,
        losLever=LOS_LEVER,
        losPercentageChange=LOS_PERCENTAGE_CHANGE,
        cpapLever=CPAP_LEVER,
        cpapPercentageChange=CPAP_PERCENTAGE_CHANGE,
        pathwayLever=PATHWAY_LEVER,
        pathwayLeverChange=PATHWAY_LEVER_LOS_CHANGE,
        phototherapyIntervention=PHOTOTHERAPY_INTERVENTION,
        sepsisIntervention=SEPSIS_INTERVENTION,
        nicuThresholdLever=NICU_THRESHOLD_LEVER,
        nicuThresholdLeverChange=NICU_THRESHOLD_LEVER_CHANGE,
        nicuWaitTimeLever = NICU_WAIT_TIME_LEVER,
        nicuWaitTimeLeverChange = NICU_WAIT_TIME_LEVER_CHANGE,
    ) + '.csv'
    if os.path.exists(occupancy_csv_path):
        os.remove(occupancy_csv_path)
        os.remove(admission_csv_path)

    
    RANDOM_SEEDS = [42 + i for i in range(NUMBER_RUNS)]
    all_admission_log = []

    args = [(seed, run_id, output_folder) for run_id, seed in enumerate(RANDOM_SEEDS, start=1)]
    #parallel processing
    with Pool() as pool:
        results = pool.map(run_simulation, args)
        for admission_log in results:
            all_admission_log.extend(admission_log)
    
    
    
    with open(admission_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['run_id', 'id', 'subregion', 'cesarean_section', 'gestational_age', 'weight','stay_number', 'hospital', 'ward', 'hospital_region', 'cpap', 'o2', 'hfo', 'antibiotics', 'photherapy', 'anemia', 'thrombocytopenia', 'sepsis', 'admission_criteria', 'length_of_stay', 'start_date', 'end_date'])
        writer.writerows(all_admission_log)