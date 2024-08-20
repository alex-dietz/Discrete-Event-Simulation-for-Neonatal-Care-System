# Discrete Event Simulation (DES) Model for Neonatal Care System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Installation](#installation)
4. [How to Run the Model](#how-to-run-the-model)
5. [Configuration](#configuration)
6. [Analyzing Results](#analyzing-results)
7. [Output](#output)
8. [License](#license)

## Project Overview
This project is a Discrete Event Simulation (DES) model designed to simulate the neonatal care system in a region with multiple hospitals and ward levels. It was initially developed for the south-west region of the Netherlands but can easily be adapted to other settings. The model allows to run experiments on scenarios, system levers, and interventions to identify ways of overcoming capacity shortages within staffing limitations.


## Directory Structure

The project directory is organized as follows:

```
├── model_run.py               # Main script to run the simulation
├── model/
│   ├── hospital.py            # Defines the hospital's processes and resources
│   ├── patient_arrival.py     # Handles patient arrival logic
│   ├── patient.py             # Defines patient behavior and characteristics
│   ├── config/
│       ├── run_config.py      # Defines different simulation scenarios and experiments
│       ├── constants.py       # Stores global constants used in the simulation
├── output/                    # Directory where simulation outputs are stored
├── notebooks/                 # Jupyter notebooks for analyzing simulation outputs and initial data exploration of the perinatal birth registry dataset
├── requirements.txt           # List of dependencies required to run the project
└── README.md                  # This README file
```


## Installation
To run this project, you'll need to have Python installed. Follow these steps to install the required packages:

1. Clone the repository to your local machine.
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Model
To run the simulation, execute the `model_run.py` script from the command line:

```bash
python model_run.py

```
This will run the simulation based on the configurations set in the run_config.py file.

## Configuration
The simulation can be configured and customized using the files located in the model/config/ directory:

run_config.py: This file defines various simulation scenarios and experiments. You can set different parameters and configurations to test different scenarios.
constants.py: This file contains global constants such as arrival rates, service times, and other fixed parameters used throughout the model.
Adjust these configurations as needed before running the simulation.


## Analyzing Results
The results of the simulation are saved in the output/ directory. You can analyze these results using the Jupyter notebooks provided in the notebooks/ folder.
To start a Jupyter notebook session, it is recommend to use an IDE like VS Code and run the notebook from there.
There are two main notebooks:
1. Output_comparison.ipynb: This notebook compares the results of different simulation runs and scenarios no matter which settings. It is necessary to provide the file path for each file.
2. Lever_comparison.ipynb: This notebook compares the results of different system levers and their values. One can set the to be analyzed settings directly in the file and the notebook will load all relevant files.

Both notebooks return information on the four performance indicators for the model:
1. Required Beds
2. Weekly Occupancy Rate
3. Capacity Transfer Rate
4. Weekly Capacity Transfers

For more information on those indicators and the model in general, please consult the thesis here:
[https://repository.tudelft.nl/record/uuid:e0e5c46d-ac63-429b-8984-310713cb5e4d](https://repository.tudelft.nl/record/uuid:e0e5c46d-ac63-429b-8984-310713cb5e4d)



## About
This project was developed as part of the Master's thesis in Engineering and Policy Analysis at the Delft University of Technology by Alexander Dietz. 

The repository is also stored on 4TU.ResearchData and can be referenced using: <br>
[![DOI](https://data.4tu.nl/v3/datasets/22215562/doi-badge.svg)](https://doi.org/10.4121/65c49906-dcaf-48fd-b942-e1b42b8c6a18)

## License
This project is licensed under the MIT License. See the LICENSE file for details.
