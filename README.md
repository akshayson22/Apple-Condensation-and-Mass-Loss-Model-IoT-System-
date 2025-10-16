**Apple Condensation and Mass Loss Model**

This repository contains an Internet of Things (IoT)-driven predictive model for analyzing and predicting condensation and mass loss in apples during storage. The model integrates real-time sensor data to provide insights into post-harvest fruit quality.

---

**Background**

This project is based on the research paper "Investigating apple surface condensation and mass loss with IoT and predictive modelling" by Sonawane et al. (2025). The study addresses the significant challenge of condensation and mass loss in cold storage, which can lead to microbial growth, spoilage, and a reduction in fruit quality. The developed model aims to optimize storage conditions by accurately predicting these phenomena in real time.

---

**Features**

* **Predictive Modeling:** Forecasts cumulative condensation, condensation retention time, and cumulative mass loss in apples.
* **Real-time Data Integration:** Collects and processes sensor data, including:

  * Air and apple surface temperature
  * Relative humidity
  * Air speed
  * Surface wetness
* **Biophysical Equations:** Utilizes principles such as the Sherwood number for mass transfer and models mass loss via transpiration and respiration.
* **Validation:** Tested with experiments using both individual and bulk apples under varying temperature conditions.

---

**Files**

* `Apple_condensation_and_mass_loss_model.py`: Python script implementing the predictive model. Accepts real-time sensor data as input to compute condensation, mass loss, and updated fruit mass over time.
* `Sonawane_et_al_2025_PBT.pdf`: Academic paper detailing methodology, experimental setup, and results, providing the theoretical foundation for the Python model.

---

**Installation and Usage**

1. Ensure you have Python 3.x installed.

2. Set up your IoT system capable of collecting and streaming sensor data (for full implementation):

   * Sensors (e.g., Adafruit SHT45)
   * Microcontrollers (e.g., STM32L031K Nucleo board)
   * Raspberry Pi as a bridge
   * Kafka streaming platform
   * InfluxDB for real-time visualization

3. To run the Python simulation locally:

```bash
python "Apple_condensation_and_mass_loss_model.py"
```

**Dependencies:**

* Standard Python libraries: `math`, `time`
* For full IoT integration: `pandas`, `numpy`, `matplotlib`, `confluent-kafka`, `Adafruit-SHT45`, `influxdb-client`

---

**Citation**

If you use this model or the associated research in your work, please cite:

Sonawane, A. D., Hoffmann, T. G., Jedermann, R., Linke, M., & Mahajan, P. V. (2025). Investigating apple surface condensation and mass loss with IoT and predictive modelling. *Postharvest Biology and Technology, 225*, 113520. [https://doi.org/10.1016/j.postharvbio.2024.113520](https://doi.org/10.1016/j.postharvbio.2024.113520)
