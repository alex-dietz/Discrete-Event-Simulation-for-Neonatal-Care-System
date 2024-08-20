import salabim as sim
class Hospital(sim.Component):
    def setup(self, hospital_name, ward_level, beds,region):
        self.hospital_name = hospital_name
        self.ward_level = ward_level
        self.beds = sim.Resource(name=f'{hospital_name}_{ward_level}', capacity=beds)
        self.region = region
        
        
        self.admissions = sim.Monitor(name=f'{hospital_name}_admissions')
        self.occupancy = sim.Monitor(name=f'{hospital_name}_occupancy', level=True,initial_tally=0)
