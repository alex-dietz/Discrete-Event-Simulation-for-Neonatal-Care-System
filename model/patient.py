import salabim as sim
from sklearn.mixture import GaussianMixture
import pandas as pd
import numpy as np
from config.constants import *

from config.run_config import *

gestational_age_gmm = GaussianMixture(n_components=GESTATIONAL_AGE_GMM_N_COMPONENTS)
gestational_age_gmm.weights_ = np.array(GESTATIONAL_AGE_GMM_WEIGHTS)
gestational_age_gmm.means_ = np.array(GESTATIONAL_AGE_GMM_MEANS)
gestational_age_gmm.covariances_ = np.array(GESTATIONAL_AGE_GMM_COVARIANCES)




class Patient(sim.Component):
    def setup(self, admission_log, outside_region, run_id, hospital_dict,is_outside_region=False,age=None):
        subregions = list(SUBREGIONS.keys())
        probabilities = list(SUBREGIONS.values()) 
        
        
        
        if is_outside_region:
            self.subregion = 'Outside Region'
        else:
            
            self.subregion = np.random.choice(subregions, p=probabilities)
            
        if age:
            self.gestational_age = age
        else:
            self.gestational_age = self.get_gestational_age()
        self.weight = self.get_weight()
        self.admission_criteria = get_admission_criteria(sim.IntUniform(1, 2).sample(), self.gestational_age, self.weight)
        self.ward_level = self.determine_ward_level()
        self.c_section = self.get_c_section()
        self.stay_number = 0
        self.next_ward_level = self.ward_level
        self.admission_log = admission_log
        self.outside_region = outside_region
        self.run_id = run_id
        self.hospital_dict = hospital_dict

        # Initialize the admission log index dictionary if not already done
        if not hasattr(self, 'admission_log_index'):
            self.admission_log_index = {}

    def process(self):
        self.setup_admission()

    def reset_treatments(self):
        self.o2_days = 0
        self.cpap_days = 0
        self.hfo_days = 0
        self.phototherapy = 0
        self.thrombocytopenia = 0
        self.antibiotics = 0
        self.anemia = 0
        self.sepsis = 0

    def setup_admission(self):
        self.reset_treatments()
        self.o2_days = self.get_o2_days()
        self.cpap_days = self.get_cpap_days()
        self.phototherapy = self.get_phototherapy()
        if self.ward_level == 'NICU':
            self.hfo_days = self.get_hfo_days()
        self.thrombocytopenia = self.get_thrombocytopenia()
        self.antibiotics = self.get_antibiotics()
        self.anemia = self.get_anemia_treatment()
        self.sepsis = self.get_sepsis_treatment()    

        hospital = self.request_admission(self.ward_level)
        length_of_stay = self.determine_length_of_stay(self.ward_level)
        self.stay_number += 1
        if PHOTOTHERAPY_INTERVENTION:
            if self.gestational_age >= 35*7 and self.admission_criteria == ['icterus']:
                length_of_stay = 1
        if SEPSIS_INTERVENTION:
            if self.gestational_age >= 35*7 and self.sepsis:
                length_of_stay = int(length_of_stay * 0.49)
                
        admission_time = self.env.now()
        admission_id = f"{self.run_id}-{self.name().split('.')[1]}-{self.stay_number}"

        if hospital:                         
            if PHOTOTHERAPY_INTERVENTION or SEPSIS_INTERVENTION:
                if (self.gestational_age >= 35*7 and self.admission_criteria == ['icterus']) or (self.gestational_age >= 35*7 and self.sepsis):
                    pass  # Do nothing in this case
                else:
                    self.re_admission()
            else:
                self.re_admission()
            hospital.admissions.tally(1)
            self.admission_log.append([self.run_id, self.name().split('.')[1], self.subregion, self.c_section, self.gestational_age, self.weight, self.stay_number, hospital.hospital_name, self.ward_level, hospital.region, self.cpap_days, self.o2_days, self.hfo_days, self.antibiotics, self.phototherapy, self.anemia, self.thrombocytopenia, self.sepsis, ','.join(self.admission_criteria), length_of_stay, admission_time, admission_time + length_of_stay])
            self.admission_log_index[admission_id] = len(self.admission_log) - 1

            self.hold(length_of_stay)
            if PATHWAY_LEVER and PATHWAY_LEVER_LOS_CHANGE > 0:
                if self.ward_level == 'NICU' and self.next_ward_level == 'high':
                    # Update admission log
                    idx = self.admission_log_index[admission_id]
                    self.admission_log[idx][19] += PATHWAY_LEVER_LOS_CHANGE  # Update length_of_stay
                    self.admission_log[idx][21] += PATHWAY_LEVER_LOS_CHANGE  # Update end_date
                    self.hold(PATHWAY_LEVER_LOS_CHANGE)
                    self.next_ward_level = 'medium'
            
            if NICU_WAIT_TIME_LEVER and NICU_WAIT_TIME_LEVER_CHANGE > 0 and self.env.now() >= WARM_UP_TIME:
                if self.ward_level == 'NICU' and self.next_ward_level == 'high':
                    wait_days = 0
                    while wait_days < NICU_WAIT_TIME_LEVER_CHANGE:
                        next_hospital = self.find_closest_hospital(self.subregion, self.next_ward_level, self.hospital_dict)
                        if next_hospital:
                            break
                        # Update admission log                        
                        idx = self.admission_log_index[admission_id]
                        self.admission_log[idx][19] += 1  # Update length_of_stay
                        self.admission_log[idx][21] += 1  # Update end_date
                        wait_days += 1
                        self.hold(1)
                        if wait_days >2:
                            print(f'Patient {self.name().split(".")[1]} waiting for high care bed for {wait_days} days')
         
        else:
            self.outside_region.admissions.tally(1)
            if self.subregion != 'Outside Region':
                if PHOTOTHERAPY_INTERVENTION:
                    if self.gestational_age >= 35*7 and self.admission_criteria == ['icterus']:
                        pass  # Do nothing in this case
                    else:
                        self.re_admission()
                else:
                    self.re_admission()
            self.admission_log.append([self.run_id, self.name().split('.')[1], self.subregion, self.c_section, self.gestational_age, self.weight, self.stay_number, 'Outside Hospital', self.ward_level, 'Outside', self.cpap_days, self.o2_days, self.hfo_days, self.antibiotics, self.phototherapy, self.anemia, self.thrombocytopenia, self.sepsis, ','.join(self.admission_criteria), length_of_stay, admission_time, admission_time + length_of_stay])
            self.admission_log_index[admission_id] = len(self.admission_log) - 1
            self.hold(length_of_stay)
            

        
            
        if hospital:
            self.release(hospital.beds)

        if self.ward_level != self.next_ward_level:
            self.ward_level = self.next_ward_level
            self.setup_admission()

    def find_closest_hospital(self, patient_subregion, ward_level, hospital_dict):
        if patient_subregion == 'Outside Region' or PATHWAY_LEVER == 1:
            potential_hospitals = [hospital for hospital in hospital_dict[f"{ward_level}_care_hospitals"] if hospital.beds.available_quantity() > 0]
            if potential_hospitals:             
                return sim.Pdf(potential_hospitals, 1).sample()
        else:
            checked_regions = set()
            regions_to_check = [patient_subregion]
            all_regions = sorted(set(ADJACENT_SUBREGIONS.keys()))
            
            while regions_to_check:
                current_region = regions_to_check.pop(0)
                checked_regions.add(current_region)
                potential_hospitals = [hospital for hospital in hospital_dict[f"{ward_level}_care_hospitals"] if hospital.region == current_region and hospital.beds.available_quantity() > 0]
                if potential_hospitals:
                    return sim.Pdf(potential_hospitals, 1).sample()
                if current_region in ADJACENT_SUBREGIONS:
                    for adjacent_region in ADJACENT_SUBREGIONS[current_region]:
                        if adjacent_region not in checked_regions and adjacent_region not in regions_to_check:
                            regions_to_check.append(adjacent_region)
            for region in all_regions:
                if region not in checked_regions:
                    potential_hospitals = [hospital for hospital in hospital_dict[f"{ward_level}_care_hospitals"] if hospital.region == region and hospital.beds.available_quantity() > 0]
                    if potential_hospitals:
                        return sim.Pdf(potential_hospitals, 1).sample()
        
        return None

    def wait_for_high_care(self):
        wait_days = 0
        while wait_days < 5:
            hospital = self.find_closest_hospital(self.subregion, self.next_ward_level, self.hospital_dict)
            if hospital:                
                self.ward_level = self.next_ward_level
                self.setup_admission()
                return
            self.hold(1)
            wait_days += 1

        # If no high care bed available after 5 days, transfer to outside region        
        self.setup_admission()         

    def request_admission(self, ward_level):
        hospital = self.find_closest_hospital(self.subregion, ward_level, self.hospital_dict)
        if hospital:
            self.request(hospital.beds)           
            return hospital
        else:            
            return None

    def re_admission(self):
        if self.ward_level == 'NICU':
            self.next_ward_level = sim.Pdf(['NICU', 'high', 'medium'], [0.60, 0.33, 0.07]).sample()
            if self.next_ward_level != 'NICU':
                np.append(self.admission_criteria, 'post_ic')                
        elif self.ward_level == 'high':
            self.next_ward_level = sim.Pdf(['NICU', 'high'], [0.02, 0.98]).sample()                        
        elif self.ward_level == 'medium':
            self.next_ward_level = sim.Pdf(['NICU',  'medium'], [0.02, 0.98]).sample()
      
    def get_weight(self):
        prediction = np.exp(WEIGHT_AGE_INTERCEPT + WEIGHT_AGE_COEFFICIENT * self.gestational_age)
        
        while True:
            range_term = sim.Normal(0, 250).sample() 
            adjusted_prediction = prediction + range_term
            
            if 400 <= adjusted_prediction <= 5750:
                break

        return int(adjusted_prediction)
        
    def get_gestational_age(self):
        while True:
            gestational_age = gestational_age_gmm.sample()[0][0][0]
            if gestational_age >= 168 and gestational_age <= 300:
                return int(gestational_age)
            
    def get_o2_days(self):
        if self.ward_level == 'NICU':
            if self.gestational_age <= 224:
                return int(sample_from_custom_distribution(O2_DAYS_NICU_BELOW32_PROBABILITIES, O2_DAYS_NICU_BELOW32_RANGE, mode='inverse', gestational_age=self.gestational_age))
            else:
                return int(sample_from_custom_distribution(O2_DAYS_NICU_ABOVE32_PROBABILITIES, O2_DAYS_NICU_ABOVE32_RANGE, mode='inverse', gestational_age=self.gestational_age))
        elif self.ward_level == 'high':
            if self.gestational_age <= 224:
                return int(sample_from_custom_distribution(O2_DAYS_HIGH_BELOW_224_PROBABILITIES, O2_DAYS_HIGH_BELOW_224_RANGE, mode='inverse', gestational_age=self.gestational_age, factor=0.1))
            else:
                return int(sample_from_custom_distribution(O2_DAYS_HIGH_ABOVE_224_PROBABILITIES, O2_DAYS_HIGH_ABOVE_224_RANGE, mode='inverse', gestational_age=self.gestational_age, factor=0.1))
        else:
            return int(sample_from_custom_distribution(O2_DAYS_MEDIUM_PROBABILITIES, O2_DAYS_MEDIUM_RANGE, mode='inverse', gestational_age=self.gestational_age))
        
    def get_hfo_days(self):
        hfo_days = 0
        if self.ward_level == 'NICU':
            if self.gestational_age <= 190:
                hfo_days = (sample_from_custom_distribution(HFO_NICU_BELOW_200_DAYS_PROBABILITIES, HFO_NICU_DAYS_BELOW200_RANGE, mode='inverse', gestational_age=self.gestational_age))
            else:
                hfo_days = (sample_from_custom_distribution(HFO_NICU_ABOVE_200_DAYS_PROBABILITIES, HFO_NICU_DAYS_ABOVE200_RANGE, mode='inverse', gestational_age=self.gestational_age))
        hfo_days = int(hfo_days)
        if HFO_LEVER:
            hfo_days = int(hfo_days * ((100 + HFO_PERCENTAGE_CHANGE) / 100))
        return int(hfo_days)

    def get_cpap_days(self):
        cpap_days = 0

        if self.ward_level == 'NICU':
            if self.gestational_age <= 200:
                cpap_days = sample_from_custom_distribution(CPAP_DAYS_NICU_BELOW200_PROBABILITIES, CPAP_DAYS_NICU_BELOW200_RANGE, mode='inverse', gestational_age=self.gestational_age)
            elif self.gestational_age <= 224:
                cpap_days = sample_from_custom_distribution(CPAP_DAYS_NICU_200_224_PROBABILITIES, CPAP_DAYS_NICU_200_224_RANGE, mode='inverse', gestational_age=self.gestational_age)
            else:
                cpap_days = sample_from_custom_distribution(CPAP_DAYS_NICU_ABOVE32_PROBABILITIES, CPAP_DAYS_NICU_ABOVE32_RANGE, mode='inverse', gestational_age=self.gestational_age)
        
        elif self.ward_level == 'high':
            if self.gestational_age <= 224:
                cpap_days = sample_from_custom_distribution(CPAP_DAYS_HIGH_BELOW_224_PROBABILITIES, CPAP_DAYS_HIGH_BELOW_224_RANGE, mode='inverse', gestational_age=self.gestational_age, factor=0.1)
            else:
                cpap_days = sample_from_custom_distribution(CPAP_DAYS_HIGH_ABOVE_224_PROBABILITIES, CPAP_DAYS_HIGH_ABOVE_224_RANGE, mode='inverse', gestational_age=self.gestational_age, factor=0.1)
        
        else:
            cpap_days = sample_from_custom_distribution(CPAP_DAYS_MEDIUM_PROBABILITIES, CPAP_DAYS_MEDIUM_RANGE, mode='inverse', gestational_age=self.gestational_age, factor=0.6)
        cpap_days = int(cpap_days)
        if CPAP_LEVER:
            cpap_days = int(cpap_days * ((100 + CPAP_PERCENTAGE_CHANGE) / 100))
        return int(cpap_days)

    def get_c_section(self):        
        return sim.Pdf((0, 1 - CESAREAN_SECTION_PROBABILITY, 1, CESAREAN_SECTION_PROBABILITY)).sample()

    def get_phototherapy(self):
        if self.ward_level == 'NICU':
            if self.gestational_age <= 35*7:
                return sim.Pdf((0, 1 - PHOTOTHERAPY_PROBABILITY_NICU, 1, PHOTOTHERAPY_PROBABILITY_NICU)).sample()
            else:
                return sim.Pdf((0, 1 - PHOTOTHERAPY_PROBABILITY_NICU_ABOVE35, 1, PHOTOTHERAPY_PROBABILITY_NICU_ABOVE35)).sample()
        elif self.ward_level == 'high':
            if self.gestational_age <= 35*7:
                return sim.Pdf((0, 1 - PHOTOTHERAPY_PROBABILITY_HIGH_CARE, 1, PHOTOTHERAPY_PROBABILITY_HIGH_CARE)).sample()
            else:
                return sim.Pdf((0, 1 - PHOTOTHERAPY_PROBABILITY_HIGH_CARE_ABOVE35, 1, PHOTOTHERAPY_PROBABILITY_HIGH_CARE_ABOVE35)).sample()
            
        else:
            if self.gestational_age <= 35*7:
                return sim.Pdf((0, 1 - PHOTOTHERAPY_PROBABILITY_MEDIUM_CARE, 1, PHOTOTHERAPY_PROBABILITY_MEDIUM_CARE)).sample()
            else:
                return sim.Pdf((0, 1 - PHOTOTHERAPY_PROBABILITY_MEDIUM_CARE_ABOVE35, 1, PHOTOTHERAPY_PROBABILITY_MEDIUM_CARE_ABOVE35)).sample()
        


    def get_antibiotics(self):
        if self.ward_level == 'NICU':
            return sim.Pdf((0, 1 - ANTIBIOTICS_PROBABILITY_NICU, 1, ANTIBIOTICS_PROBABILITY_NICU)).sample()
        elif self.ward_level == 'high':
            return sim.Pdf((0, 1 - ANTIBIOTICS_PROBABILITY_HIGH_CARE, 1, ANTIBIOTICS_PROBABILITY_HIGH_CARE)).sample()
        else:
            return sim.Pdf((0, 1 - ANTIBIOTICS_PROBABILITY_MEDIUM_CARE, 1, ANTIBIOTICS_PROBABILITY_MEDIUM_CARE)).sample()

    def get_thrombocytopenia(self):
        if self.ward_level == 'NICU':
            return sim.Pdf((0, 1 - THROMBOCYTOPENIA_PROBABILITY, 1, THROMBOCYTOPENIA_PROBABILITY)).sample()
        else:
            return 0

    def get_anemia_treatment(self):
        if self.ward_level == 'NICU':
            if self.gestational_age <= 32*7:
                return sim.Pdf((0, 1 - ANEMIA_NICU_BELOW224_PROBABILITY, 1, ANEMIA_NICU_BELOW224_PROBABILITY)).sample()
            else:
                return sim.Pdf((0, 1 - ANEMIA_NICU_ABOVE224_PROBABILITY, 1, ANEMIA_NICU_ABOVE224_PROBABILITY)).sample()
        elif self.ward_level == 'high':
            if self.gestational_age <= 32*7:
                return sim.Pdf((0, 1 - ANEMIA_HIGH_CARE_PROBABILITY, 1, ANEMIA_HIGH_CARE_PROBABILITY)).sample()
            else:
                return sim.Pdf((0, 1 - ANEMIA_HIGH_CARE_ABOVE32_PROBABILITY, 1, ANEMIA_HIGH_CARE_ABOVE32_PROBABILITY)).sample()            
        else:
            return 0

    def get_sepsis_treatment(self):
        if self.ward_level == 'NICU':
            if self.gestational_age <= 35*7:
                return sim.Pdf((0, 1 - SEPSIS_PROBABILITY_NICU, 1, SEPSIS_PROBABILITY_NICU)).sample()
            else:
                return sim.Pdf((0, 1 - SEPSIS_PROBABILITY_NICU_ABOVE35, 1, SEPSIS_PROBABILITY_NICU_ABOVE35)).sample()
        elif self.ward_level == 'high':
            return sim.Pdf((0, 1 - SEPSIS_PROBABILITY_HIGH_CARE, 1, SEPSIS_PROBABILITY_HIGH_CARE)).sample()
        else:
            if self.gestational_age <= 35*7:
                return sim.Pdf((0, 1 - SEPSIS_PROBABILITY_MEDIUM_CARE, 1, SEPSIS_PROBABILITY_MEDIUM_CARE)).sample()
            else:
                return sim.Pdf((0, 1 - SEPSIS_PROBABILITY_MEDIUM_CARE_ABOVE35, 1, SEPSIS_PROBABILITY_MEDIUM_CARE_ABOVE35)).sample()
        


    def determine_length_of_stay(self, ward_level):
        if ward_level == 'NICU':
            if self.gestational_age <= 32*7:
                coefficients = COEFFICIENTS_NICU_BELOW32
                data = pd.DataFrame([{
                    'const': 1,
                    'gestational_age': self.gestational_age,
                    'weight': self.weight,
                    'phototherapy': self.phototherapy,
                    'anemia': self.anemia,                    
                    'cpap_days': self.cpap_days,
                    'hfo_days': self.hfo_days,
                    'o2_days': self.o2_days,
                    'thrombocytopenia': self.thrombocytopenia,
                    'antibiotics': self.antibiotics,
                }])
            else:
                coefficients = COEFFICIENTS_NICU
                data = pd.DataFrame([{
                    'const': 1,                
                    'gestational_age': self.gestational_age,
                    'weight': self.weight,
                    'anemia': self.anemia,    
                    'cpap_days': self.cpap_days,
                    'hfo_days': self.hfo_days,
                    'o2_days': self.o2_days,
                }])
        elif ward_level == 'high':
            if self.gestational_age <= 196:
                coefficients = COEFFICIENTS_HIGH_BELOW_28
                data = pd.DataFrame([{
                    'const': 1,
                    'gestational_age': self.gestational_age,
                    'antibiotics': self.antibiotics,
                    'phototherapy': self.phototherapy,
                    'anemia': self.anemia,  
                    'cpap_days': self.cpap_days,
                    'o2_days': self.o2_days,
                }])
            elif self.gestational_age > 259:
                coefficients = COEFFICIENTS_HIGH_ABOVE_37
                data = pd.DataFrame([{
                    'const': 1,
                    'gestational_age': self.gestational_age,
                    'weight': self.weight,
                    'phototherapy': self.phototherapy,
                    'anemia': self.anemia,
                    'cpap_days': self.cpap_days,
                    'o2_days': self.o2_days,
                    'post_ic': 1 if 'post_ic' in self.admission_criteria else 0,
                    'sepsis': self.sepsis,
                    'others': 1 if 'others' in self.admission_criteria else 0,
                }])
            else:
                coefficients = COEFFICIENTS_HIGH
                data = pd.DataFrame([{
                    'const': 1,
                    'gestational_age': self.gestational_age,
                    'weight': self.weight,
                    'phototherapy': self.phototherapy,
                    'anemia': self.anemia,  
                    'cpap_days': self.cpap_days,
                    'o2_days': self.o2_days,
                    'post_ic': 1 if 'post_ic' in self.admission_criteria else 0,
                }])
        else:
            if self.gestational_age <= 31*7:
                coefficients = COEFFICIENTS_MEDIUM_BELOW_31
                data = pd.DataFrame([{
                    'const': 1,
                    'gestational_age': self.gestational_age,
                    'cpap_days': self.cpap_days,
                    'o2_days': self.o2_days,
                    'post_ic': 1 if 'post_ic' in self.admission_criteria else 0,                    
                    'others': 1 if 'others' in self.admission_criteria else 0,
                    'phototherapy': self.phototherapy,
                    'stay_number': self.stay_number,
                }])
            elif self.gestational_age > 266:
                coefficients = COEFFICIENTS_MEDIUM_ABOVE_37
                data = pd.DataFrame([{
                    'const': 1,
                    'o2_days': self.o2_days,
                    'cpap_days': self.cpap_days,
                    'phototherapy': self.phototherapy,
                    'c_section': self.c_section,
                    'sepsis': self.sepsis,
                }])
            else:
                coefficients = COEFFICIENTS_MEDIUM
                data = pd.DataFrame([{
                    'const': 1,
                    'gestational_age': self.gestational_age,                    
                    'o2_days': self.o2_days,
                    'weight': self.weight,
                    'phototherapy': self.phototherapy,
                    'c_section': self.c_section,
                }])
        
        eta = np.dot(data, pd.Series(coefficients))
        df = pd.DataFrame(data)

        
        predicted_los = eta[0]
        #minimal LoS 1 day
        predicted_los = max(1, int((eta[0])))
        #minimal days for extreme premature
        predicted_los = max(predicted_los, 224 - self.gestational_age)
        #minimal days based on respiratory support
        predicted_los = max(predicted_los, self.o2_days, self.cpap_days, self.hfo_days)
        
        #minimal days for sepsis
        if self.sepsis:
            predicted_los = max(predicted_los,7)
        if LOS_LEVER:
            predicted_los = int(predicted_los * ((100 + LOS_PERCENTAGE_CHANGE) / 100))  
        if NICU_THRESHOLD_LEVER and self.ward_level == 'high' and self.gestational_age <= 32*7:
            predicted_los += -NICU_THRESHOLD_LEVER_CHANGE*7
        return predicted_los

    def determine_ward_level(self):
        
        if NICU_THRESHOLD_LEVER:
            nicu_threshold = NICU_THRESHOLD+NICU_THRESHOLD_LEVER_CHANGE
        else:
            nicu_threshold = NICU_THRESHOLD
        p = sim.Uniform(0, 1).sample()
        if self.weight <= 1250 or self.gestational_age <= nicu_threshold*7 or 'congenital abnormalities' in self.admission_criteria:
            if NICU_ASSIGNMENT_LEVER and self.gestational_age > 28 * 7:
                if p < 1 + NICU_ASSIGNMENT_PERCENTAGE_CHANGE / 100:                    
                    return 'NICU'
                else:                    
                    return 'high'
            else:                
                return 'NICU'
        elif NICU_THRESHOLD_LEVER and self.gestational_age <= 32 * 7:
            return 'high'
        else:                        
            if p < HIGH_CARE_PERCENTAGE + (HIGH_CARE_ASSIGNMENT_PERCENTAGE_CHANGE / 100 if HIGH_CARE_ASSIGNMENT_LEVER else 0):
                return 'high'
            else:
                return 'medium'

def get_admission_criteria(size, gestational_age, weight):
    criteria = ADMISSION_CRITERIA.copy()    
    if gestational_age >= 37 * 7:
        criteria.pop('premature', None)
    if weight >= 2000:
        criteria.pop('weight', None)         
    pdf = sim.Pdf(criteria)        
    selected_criteria = set()
    while len(selected_criteria) < size:
        selected_criteria.add(pdf.sample())    
    return list(sorted(selected_criteria))


def sample_from_custom_distribution(first_probs, range, mode='linear', gestational_age=None, min_gestational_age=168, factor=1.6):
    """
    Samples a value from a custom probability distribution, which can be a combination of a provided discrete distribution
    and a continuous distribution with optional scaling.

    Parameters:
    - first_probs (list of tuples): A list of (value, probability) pairs specifying a discrete probability distribution.
                                     The sum of the probabilities should not exceed 1. If it's less than 1, the remaining 
                                     probability mass will be allocated to the selected distribution over the specified range.
    - range (tuple): A tuple (min_val, max_val) defining the range [min_val, max_val] over which the selected
                             distribution will be applied if the remaining probability mass is non-zero.
    - mode (str, optional): Specifies the distribution mode for the range part. Options are:
        - 'linear': Linear decreasing probability distribution over the range.
        - 'exponential': Exponential decreasing probability distribution.
        - 'inverse': Inverse power-law distribution, controlled by the 'factor' parameter.
    - gestational_age (int, optional): A value used to scale the probabilities in the range based on 
                                       the current gestational age.
    - min_gestational_age (int, optional): The minimum gestational age used for scaling purposes. Default is 168.
    - factor (float, optional): A scaling factor used in the 'inverse' mode for controlling the power of the 
                                inverse distribution. Default is 1.6.

    Returns:
    - int: A sampled value from either the provided discrete distribution or the generated selected distribution, 
           based on the mode and parameters.

    Raises:
    - ValueError: If the sum of the probabilities in `first_probs` exceeds 1 or if an invalid `mode` is provided.
    """
    if first_probs:
        values, probs = zip(*first_probs)
        prob_sum = np.sum(probs)
        if prob_sum > 1:
            raise ValueError("The sum of probabilities in first_probs cannot exceed 1.")
    else:
        values, probs = [], []

    remaining_prob = 1 - np.sum(probs) if probs else 1
    combined_probs = list(probs) + [remaining_prob]
    combined_values = list(values) + ['outside']
    combined_pdf = sim.Pdf({value: prob for value, prob in zip(combined_values, combined_probs)})

    choice = combined_pdf.sample()

    if choice == 'outside':
        min_val, max_val = range
        range_length = max_val - min_val + 1

        if mode == 'linear':
            linear_values = np.arange(min_val, max_val + 1)
            linear_probs = np.linspace(2 / (range_length + 1), 2 / (range_length * (range_length + 1)), range_length)
            linear_probs /= linear_probs.sum()
            linear_pdf = sim.Pdf({val: prob for val, prob in zip(linear_values, linear_probs)})
            value = linear_pdf.sample()
            if gestational_age:
                scaling_factor = min_gestational_age / gestational_age
                value = int(value * scaling_factor)
            return value

        elif mode == 'exponential':
            exponential_values = np.arange(min_val, max_val + 1)
            exp_probs = np.exp(-np.arange(range_length))
            exp_probs /= exp_probs.sum()
            if gestational_age:
                scaling_factor = gestational_age / min_gestational_age
                exp_probs = np.exp(-scaling_factor * np.arange(range_length))
                exp_probs /= exp_probs.sum()
            exponential_pdf = sim.Pdf({val: prob for val, prob in zip(exponential_values, exp_probs)})
            return exponential_pdf.sample()

        elif mode == 'inverse':
            inverse_values = np.arange(min_val, max_val + 1)
            power = factor
            inv_probs = 1 / (inverse_values ** power)
            inv_probs /= inv_probs.sum()
            if gestational_age:
                scaling_factor = (max_val - gestational_age) / (max_val - min_gestational_age)
                inv_probs = (1 / (inverse_values ** power)) ** scaling_factor
                inv_probs /= inv_probs.sum()
            inverse_pdf = sim.Pdf({val: prob for val, prob in zip(inverse_values, inv_probs)})
            return inverse_pdf.sample()

        else:
            raise ValueError("Invalid mode. Choose either 'linear', 'exponential', or 'inverse'.")
    else:
        return choice
