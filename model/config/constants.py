#Hospital Setup
HOSPITALS_2016 = [
    {"hospital_name": "Hospital 1", "region": "Subregion A", "ward_level": "NICU", "beds": 28},        
    {"hospital_name": "Hospital 2", "region": "Subregion A", "ward_level": "high", "beds": 20},
    {"hospital_name": "Hospital 3", "region": "Subregion B", "ward_level": "high", "beds": 24},
    {"hospital_name": "Hospital 4", "region": "Subregion C", "ward_level": "high", "beds": 28},
    {"hospital_name": "Hospital 5", "region": "Subregion D", "ward_level": "high", "beds": 22},
    {"hospital_name": "Hospital 6", "region": "Subregion B", "ward_level": "medium", "beds": 13},
    {"hospital_name": "Hospital 7", "region": "Subregion E", "ward_level": "medium", "beds": 14},
    {"hospital_name": "Hospital 8", "region": "Subregion F", "ward_level": "medium", "beds": 13},
    {"hospital_name": "Hospital 9", "region": "Subregion F", "ward_level": "medium", "beds": 5},
    {"hospital_name": "Hospital 10", "region": "Subregion A", "ward_level": "medium", "beds": 19},
    {"hospital_name": "Hospital 11", "region": "Subregion C", "ward_level": "medium", "beds": 24}
]

HOSPITALS_WITHOUT_CLOSURE = [
    {"hospital_name": "Hospital 1", "region": "Subregion A", "ward_level": "NICU", "beds": 32},        
    {"hospital_name": "Hospital 2", "region": "Subregion A", "ward_level": "high", "beds": 20},
    {"hospital_name": "Hospital 3", "region": "Subregion B", "ward_level": "high", "beds": 22},
    {"hospital_name": "Hospital 4", "region": "Subregion C", "ward_level": "high", "beds": 21},
    {"hospital_name": "Hospital 5", "region": "Subregion D", "ward_level": "high", "beds": 15},
    {"hospital_name": "Hospital 6", "region": "Subregion B", "ward_level": "medium", "beds": 13},
    {"hospital_name": "Hospital 7", "region": "Subregion E", "ward_level": "medium", "beds": 14},
    {"hospital_name": "Hospital 8", "region": "Subregion F", "ward_level": "medium", "beds": 13},
    {"hospital_name": "Hospital 9", "region": "Subregion F", "ward_level": "medium", "beds": 5},
    {"hospital_name": "Hospital 10", "region": "Subregion A", "ward_level": "medium", "beds": 8},
    {"hospital_name": "Hospital 11", "region": "Subregion C", "ward_level": "medium", "beds": 13}
]

HOSPITALS_WITH_CLOSURE = [
    {"hospital_name": "Hospital 1", "region": "Subregion A", "ward_level": "NICU", "beds": 23},        
    {"hospital_name": "Hospital 2", "region": "Subregion A", "ward_level": "high", "beds": 17},
    {"hospital_name": "Hospital 3", "region": "Subregion B", "ward_level": "high", "beds": 15},
    {"hospital_name": "Hospital 4", "region": "Subregion C", "ward_level": "high", "beds": 18},
    {"hospital_name": "Hospital 5", "region": "Subregion D", "ward_level": "high", "beds": 12},
    {"hospital_name": "Hospital 6", "region": "Subregion B", "ward_level": "medium", "beds": 10},
    {"hospital_name": "Hospital 7", "region": "Subregion E", "ward_level": "medium", "beds": 11},
    {"hospital_name": "Hospital 8", "region": "Subregion F", "ward_level": "medium", "beds": 10},
    {"hospital_name": "Hospital 9", "region": "Subregion F", "ward_level": "medium", "beds": 4},
    {"hospital_name": "Hospital 10", "region": "Subregion A", "ward_level": "medium", "beds": 6},
    {"hospital_name": "Hospital 11", "region": "Subregion C", "ward_level": "medium", "beds": 13}
]

#Linked subregions for patient pathway determination
ADJACENT_SUBREGIONS = {
    "Subregion C": ["Subregion D", "Subregion F", "Subregion E"],
    "Subregion A": ["Subregion C", "Subregion B", "Subregion D"],
    "Subregion B": ["Subregion A", "Subregion D"],
    "Subregion D": ["Subregion B", "Subregion A", "Subregion E", "Subregion C"],
    "Subregion E": ["Subregion D", "Subregion F"],
    "Subregion F": ["Subregion C", "Subregion E"]
}

#Distribution of births across subregions
SUBREGIONS = {
    "Subregion C": 0.27,
    "Subregion A": 0.265,
    "Subregion B": 0.1,
    "Subregion D": 0.255,
    "Subregion E": 0.04,
    "Subregion F": 0.02,
    "Outside Region": 0.05,
}

RANDOM_SEED = 42

#Arrival Rates and range
INSIDE_REGION_ARRIVAL_MEAN = 27.94 
INSIDE_REGION_ARRIVAL_STD = 7.16
INSIDE_MIN_ARRIVAL = 9
INSIDE_MAX_ARRIVAL = 49


HIGH_CARE_PERCENTAGE = 0.58

#Week of gestation for NICU admission
NICU_THRESHOLD = 32



OUTSIDE_REGION_BEDS = float('inf')

# Distribution Parameters
GESTATIONAL_AGE_MEAN = 270
GESTATIONAL_AGE_SD = 15

#GMM Parameters for gestational age
GESTATIONAL_AGE_GMM_N_COMPONENTS = 2
GESTATIONAL_AGE_GMM_WEIGHTS = [0.858, 0.142]
GESTATIONAL_AGE_GMM_MEANS = [[275.037], [237.837]]
GESTATIONAL_AGE_GMM_COVARIANCES = [[[110.36]], [[628.688]]]

#Weight Regression
WEIGHT_AGE_COEFFICIENT = 0.0128
WEIGHT_AGE_INTERCEPT = 4.5792

#Treatment Probabilities
THROMBOCYTOPENIA_PROBABILITY = 0.04
CESAREAN_SECTION_PROBABILITY = 0.329311
ANEMIA_NICU_BELOW224_PROBABILITY = 0.26
ANEMIA_NICU_ABOVE224_PROBABILITY = 0.05
ANEMIA_HIGH_CARE_PROBABILITY = 0.11
ANEMIA_HIGH_CARE_ABOVE32_PROBABILITY = 0.002
ANTIBIOTICS_PROBABILITY_NICU = 0.38
ANTIBIOTICS_PROBABILITY_HIGH_CARE = 0.04
ANTIBIOTICS_PROBABILITY_MEDIUM_CARE = 0.02
PHOTOTHERAPY_PROBABILITY_NICU = 0.61
PHOTOTHERAPY_PROBABILITY_NICU_ABOVE35 = 0.16
PHOTOTHERAPY_PROBABILITY_HIGH_CARE = 0.29
PHOTOTHERAPY_PROBABILITY_HIGH_CARE_ABOVE35 = 0.07
PHOTOTHERAPY_PROBABILITY_MEDIUM_CARE = 0.19
PHOTOTHERAPY_PROBABILITY_MEDIUM_CARE_ABOVE35 = 0.02
SEPSIS_PROBABILITY_NICU = 0.055
SEPSIS_PROBABILITY_NICU_ABOVE35 = 0.07
SEPSIS_PROBABILITY_HIGH_CARE = 0.02
SEPSIS_PROBABILITY_MEDIUM_CARE = 0.02
SEPSIS_PROBABILITY_MEDIUM_CARE_ABOVE35 = 0.044


#Respiratory Treatment Probabilities
O2_DAYS_HIGH_BELOW_224_PROBABILITIES = [
    (0,0.76),
    (1,0.03),
    (2,0.01),
    (3,0.01),
    (4,0.01),
    (5,0.01),       
]
O2_DAYS_HIGH_BELOW_224_RANGE = (6, 74)
O2_DAYS_HIGH_ABOVE_224_PROBABILITIES = [
    (0,0.96),
    (1,0.02),     
]
O2_DAYS_HIGH_ABOVE_224_RANGE = (2, 45)
O2_DAYS_MEDIUM_PROBABILITIES = [
    (0,0.97),
    (1,0.02),       
]
O2_DAYS_MEDIUM_RANGE = (2, 58)

O2_DAYS_NICU_BELOW32_PROBABILITIES = [
    (0,0.33),
    (1,0.15),
    (2,0.06),
    (3,0.04),
    (4,0.04),
    (5,0.03),
    (6,0.02),
    (7,0.02),
    (8,0.02),   
]
O2_DAYS_NICU_BELOW32_RANGE = (9, 125)

O2_DAYS_NICU_ABOVE32_PROBABILITIES = [
    (0,0.61),
    (1,0.14),
    (2,0.08),
    (3,0.05),
    (4,0.03),
    (5,0.02),
    (6,0.02),
    (7,0.01),
    (8,0.01), 
   
]
O2_DAYS_NICU_ABOVE32_RANGE = (9, 62)
CPAP_DAYS_MEDIUM_PROBABILITIES = [
    (0,0.97),
    (1,0.02),
    
]
CPAP_DAYS_MEDIUM_RANGE = (2, 32)

CPAP_DAYS_HIGH_ABOVE_224_PROBABILITIES = [
    (0,0.93),
    (1,0.03),
    (2,0.02),
]
CPAP_DAYS_HIGH_ABOVE_224_RANGE = (3, 35)

CPAP_DAYS_HIGH_BELOW_224_PROBABILITIES = [
    (0,0.60),
    (1,0.04),
    (2,0.01),
    (3,0.01),
    (4,0.01),
    (5,0.01),
    (6,0.01),
    (7,0.01),
   
]
CPAP_DAYS_HIGH_BELOW_224_RANGE = (8, 80)
CPAP_DAYS_NICU_BELOW200_PROBABILITIES = [
    (0,0.14),
    (1,0.04),
    (2,0.03),
    (3,0.03),
    (4,0.02),
    (5,0.01),
    (6,0.03),
    (7,0.03),
    (8,0.02),
    (9,0.02),
    (10,0.02),
    (11,0.02),
    (12,0.02),
    (13,0.02),
    (14,0.02),
]
CPAP_DAYS_NICU_BELOW200_RANGE = (15, 101)
CPAP_DAYS_NICU_200_224_PROBABILITIES = [
    (0,0.33),
    (1,0.08),
    (2,0.08),
    (3,0.06),
    (4,0.06),
    (5,0.06),
    (6,0.04),
    (7,0.04),
    (8,0.03),
    (9,0.03),
    (10,0.02),
    (11,0.02),
    (12,0.02),
    (13,0.01),
    (14,0.02),
]
CPAP_DAYS_NICU_200_224_RANGE = (15, 86)
CPAP_DAYS_NICU_ABOVE32_PROBABILITIES = [
     (0,0.58),
    (1,0.16),
    (2,0.08),
    (3,0.05),
    (4,0.03),
    (5,0.03),
    (6,0.016),
    (7,0.011),
    (8,0.005),
    (9,0.005),
]
CPAP_DAYS_NICU_ABOVE32_RANGE = (10,22)

HFO_NICU_BELOW_200_DAYS_PROBABILITIES = [
    (0,0.48),
    (1,0.06),
    (2,0.05),
    (3,0.03),
    (4,0.03),
    (5,0.03),
    (6,0.02),
    (7,0.02),
    (8,0.02),
    (9,0.02),
]
HFO_NICU_DAYS_BELOW200_RANGE = (10, 101)

HFO_NICU_ABOVE_200_DAYS_PROBABILITIES = [
    (0,0.81),
    (1,0.05),
    (2,0.04),
    (3,0.02),
    (4,0.02),
    (5,0.02),
    (6,0.01),
    (7,0.01),
    
]
HFO_NICU_DAYS_ABOVE200_RANGE = (8, 65)

#Admission Criteria Probabilities
ADMISSION_CRITERIA = {
    'others': 0.29,
    'premature': 0.155,
    'weight': 0.145,
    'maternal medication': 0.14,
    'infection': 0.07,
    'icterus': 0.03,
    'feeding': 0.02,
    'congenital abnormalities': 0.005,
    'cardiovascular': 0.00,
    'asphyxia': 0.00,    
    'hypoglycemia': 0.00,
    'seizure': 0.00,
    'withdrawal symptoms': 0.00,
    'psycho': 0.00,
}

#LOS Coefficients

COEFFICIENTS_NICU = {
    'const': 21.60,
    'gestational_age': -0.0623,
    'weight': -0.0013,
    'anemia': 3.45,
    'cpap_days': 0.51,
    'hfo_days': 0.10,
    'o2_days': 0.66,
}


COEFFICIENTS_NICU_BELOW32 = {
    'const': 5.20,
    'gestational_age': -0.0023,
    'weight': -0.0010,
    'phototherapy': 0.43,
    'anemia': 1.55,
    'cpap_days': 0.75,
    'hfo_days': 0.63,
    'o2_days': 0.39,
    'thrombocytopenia': 0.03,
    'antibiotics': -1.13,
}

COEFFICIENTS_HIGH = {
    'const': 158.35,    
    'gestational_age': -0.563098,    
    'weight': -0.003614,    
    'phototherapy': 2.99,    
    'anemia': 2.13,
    'cpap_days': 0.49,    
    'o2_days': 0.39,
    'post_ic': 2.19, 
}
COEFFICIENTS_HIGH_BELOW_28 = {
    'const': -62.93,    
    'gestational_age': 0.54,    
    'antibiotics': -22.80,
    'phototherapy': 19.28,
    'anemia': 3.30,
    'cpap_days': 0.40,    
    'o2_days': 0.47, 
}
COEFFICIENTS_HIGH_ABOVE_37 = {
    'const': 7.94,    
    'gestational_age': -0.0157, 
    'weight': -0.0004,    
    'phototherapy': 1.52,    
    'anemia': 2.54,
    'cpap_days': 0.93,    
    'o2_days': 0.86,
    'post_ic': 4.73,
    'sepsis': 2.25,
    'others': -0.14
}
COEFFICIENTS_MEDIUM_BELOW_31 = {
    'const': -34.33,   
    'gestational_age': 0.1613,
    'cpap_days': 0.53,
    'o2_days': 0.08,
    'post_ic': 11.11,    
    'others': -1.22,
    'phototherapy': 13.93,
    'stay_number': 12.03,
}

COEFFICIENTS_MEDIUM = {
    'const': 120.12,   
    'gestational_age': -0.4312,
    'o2_days': 0.85,    
    'weight': -0.0017,
    'phototherapy': 2.12,
    'c_section': 1.57,
    
}
COEFFICIENTS_MEDIUM_ABOVE_37 = {
    'const': 1.59661,           
    'o2_days': 0.91, 
    'cpap_days': 0.36,
    'phototherapy': 2.64,
    'c_section': 0.90,
    'sepsis': 2.95, 
}




