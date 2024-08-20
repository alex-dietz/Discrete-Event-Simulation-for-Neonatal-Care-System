import salabim as sim
from config.constants import *
from config.run_config import *
from patient import *
import numpy as np
class PatientArrival(sim.Component):
    def setup(self, type, run_id, hospital_dict,outside_region_hospital, admission_log):
        """
        Setup function is used to initialize the component with necessary attributes.
        
        Parameters:
        - type: The type of PatientArrival Process (e.g., '23_weeks', 'inside_region', or 'outside_region')
        - run_id: Identifier for the simulation run
        - hospital_dict: Dictionary containing the hospitals categorized by care level
        - outside_region_hospital: link to outside region hospital
        - admission_log: Log to record patient admissions
        """
        self.type = type
        self.run_id = run_id
        self.hospital_dict = hospital_dict
        self.admission_log = admission_log
        self.outside_region_hospital = outside_region_hospital
        self.NICU_hospitals = hospital_dict['NICU_care_hospitals']
        self.high_care_hospitals = hospital_dict['high_care_hospitals']
        self.medium_care_hospitals = hospital_dict['medium_care_hospitals']
    
    def process(self):     
        while True:
            if self.type == '23_weeks':                
                inter_arrival_time = round(np.random.exponential(1/(NICU_23WEEKS_SCENARIO_ARRIVALS)))                
                Patient(admission_log=self.admission_log, outside_region=self.outside_region_hospital, run_id=self.run_id, hospital_dict=self.hospital_dict,age=23*7)
                self.hold(inter_arrival_time)
            
            elif self.type == 'inside_region':
                while True:                                        
                    num_patients = round(np.random.normal(INSIDE_REGION_ARRIVAL_MEAN, INSIDE_REGION_ARRIVAL_STD))
                    if INSIDE_MIN_ARRIVAL <= num_patients <= INSIDE_MAX_ARRIVAL:
                        break                                
                for _ in range(num_patients):
                    Patient(admission_log=self.admission_log, outside_region=self.outside_region_hospital, run_id=self.run_id, hospital_dict=self.hospital_dict)
                self.hold(1)
            else:                
                inter_arrival_time = round(np.random.exponential(1/(DEMAND_SCENARIO_ARRIVAL_RATE))) 
                Patient(admission_log=self.admission_log, outside_region=self.outside_region_hospital, run_id=self.run_id, hospital_dict=self.hospital_dict, is_outside_region=True)                
                self.hold(inter_arrival_time)


            if self.env.now() >= WARM_UP_TIME:
                for hospital in self.NICU_hospitals + self.high_care_hospitals + self.medium_care_hospitals:
                    hospital.beds.occupancy.tally(hospital.beds.claimed_quantity() / hospital.beds.capacity())

