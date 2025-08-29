**Apple Condensation and Mass Loss Model**

This repository contains an Internet of Things (IoT)-driven predictive model for analyzing and predicting condensation and mass loss in apples during storage. The model integrates real-time sensor data to provide insights into post-harvest fruit quality.

**Background**

This project is based on the research paper "Investigating apple surface condensation and mass loss with IoT and predictive modelling" by Sonawane et al. (2025). The study addresses the significant challenge of condensation and mass loss in cold storage, which can lead to microbial growth, spoilage, and a reduction in fruit quality. The developed model aims to optimize storage conditions by accurately predicting these phenomena in real time.

**Features**

Predictive Modeling: The model forecasts cumulative condensation, condensation retention time, and cumulative mass loss in apples.

Real-time Data Integration: It uses an IoT system to collect and process real-time sensor data, including:

Air and apple surface temperature 

Relative humidity 

Air speed 

Surface wetness 


Biophysical Equations: The model is built on established biophysical principles, including the Sherwood number for mass transfer and a model for mass loss that incorporates both transpiration and respiration.


Validation: The model has been validated through experiments with both individual and bulk apples under varying temperature conditions.

**Files**

Apple condensation and mass loss model.py: This is the Python script that implements the predictive model. It requires real-time sensor data as input to calculate condensation, mass loss, and updated fruit mass over time.

Sonawane et al 2025 PBT Investigating apple surface condensation and mass loss with IoT and predictive modelling.pdf: The complete academic paper that details the methodology, experimental setup, and results of the study. It provides the theoretical foundation for the Python model.

**Installation and Usage**

To use the Python model, you will need to set up an IoT system capable of collecting the required sensor data and streaming it to the application. The original study used a system with:

Sensors (e.g., Adafruit SHT45) 

Microcontrollers (e.g., STM32L031K Nucleo board) 

A Raspberry Pi to serve as a bridge 

A Kafka streaming platform to handle the data 

InfluxDB for real-time data visualization 

The Python script Apple condensation and mass loss model.py simulates real-time sensor data through user input, making it a good starting point for understanding the model's logic. To run the script, simply execute it in a Python environment.

**Bash**

python "Apple condensation and mass loss model.py"
Dependencies
The Python script requires the 

math and time libraries, which are standard with Python. For a complete implementation as described in the paper, additional libraries like 


pandas, numpy, matplotlib, confluent kafka, Adafruit SHT45, and influxdb client would be necessary.

**Citation**

If you use this model or the associated research in your work, please cite the following paper:

Sonawane, A. D., Hoffmann, T. G., Jedermann, R., Linke, M., & Mahajan, P. V. (2025). Investigating apple surface condensation and mass loss with IoT and predictive modelling. Postharvest Biology and Technology, 225, 113520. https://doi.org/10.1016/j.postharvbio.2024.113520
