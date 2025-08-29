import math
import time

# Physical constants
R_d = 287.05  # Specific gas constant for dry air (J/kg·K)
R_v = 461.5   # Specific gas constant for water vapor (J/kg·K)
mu0 = 1.716e-5  # Reference dynamic viscosity of air at T0 (kg/m·s)
T0 = 273.15  # Reference temperature (K)
p_bar = 1013.25  # Pressure (hPa)
C = 120  # Sutherland's constant for air (K)
alpha0 = 2.24e-5  # Thermal diffusivity at reference temperature (m²/s)
d = 0.065  # Characteristic length (e.g., fruit diameter) (m)
fruit_mass = 31879.49 - 2722.1  # Initial fruit mass (g)

# Variables
previous_time = None
cumulative_wetness_retention_time = 0
cumulative_condensation = 0
cumulative_mass_loss = [0]
new_fruit_masses = [fruit_mass]
cumulative_condensation_list = [0]
predicted_retention_time = 0

def read_sensor_data():
    """Simulate real-time sensor data. Depends on system of IoT that has been used"""
    t_surf = float(input("Enter surface temperature (t_surf) in °C: "))
    t_air = float(input("Enter air temperature (t_air) in °C: "))
    humi = float(input("Enter relative humidity (%) (humi): "))
    current_time = float(input("Enter current time in seconds (current_time): "))
    air_speed = float(input("Enter air speed (m/s) (air_speed): "))
    wetness_sensor_signal = float(input("Enter wetness sensor signal: "))
    return t_surf, t_air, humi, current_time, air_speed, wetness_sensor_signal

while True:
    # Fetch real-time sensor data
    t_surf, t_air, humi, current_time, air_speed, wetness_sensor_signal = read_sensor_data()

    # Calculate the time difference
    if previous_time is None:
        time_difference = 0
    else:
        time_difference = current_time - previous_time
    previous_time = current_time

    # Wetness sensor signal condition
    if wetness_sensor_signal < 3000:
        cumulative_wetness_retention_time += time_difference / 60

    # Convert air temperature to Kelvin
    T_K = t_air + 273.15  # Air temperature (K)
    ptotal = 101325  # Total atmospheric pressure (Pa)

    # Saturation vapor pressure calculation for air and surface
    psl_cuv_air = 610.94 * math.exp(17.625 * t_air / (t_air + 243.04))  # Saturation vapor pressure of air (Pa)
    psl_cuv_surf = 610.94 * math.exp(17.625 * t_surf / (t_surf + 243.04))  # Saturation vapor pressure of surface (Pa)
    pair = psl_cuv_air * humi / 100  # Partial pressure of water vapor in air (Pa)
    p_d = ptotal - pair  # Partial pressure of dry air (Pa)

    # Humid air density calculation
    rho_humid = (p_d / (R_d * T_K)) + (pair / (R_v * T_K))  # Humid air density (kg/m³)

    # Dynamic viscosity calculations
    mu_dry = mu0 * (T_K / T0) ** 1.5 * (T0 + C) / (T_K + C)  # Dynamic viscosity of dry air (kg/m·s)
    mu_vapor = 9.8e-6  # Dynamic viscosity of water vapor (kg/m·s)
    Y = pair / ptotal
    mu_humid = mu_dry * (1 - Y) + mu_vapor * Y  # Dynamic viscosity of humid air (kg/m·s)

    # Thermal conductivity of air
    k_moist_air = (
        ((0.002646 + 0.0000737 * (T_K)) * (1 - (0.622 * pair / (ptotal - pair)))) +
        ((0.01468 + 0.0001536 * (T_K)) * (0.622 * pair / (ptotal - pair)))
    )  # Thermal conductivity of moist air (W/m·K)

    # Specific heat capacity of moist air
    cp_moist_air = 1005 + 1.82 * t_air + (0.61 * (0.622 * pair / (ptotal - pair)) * 1860)  # (J/kg·K)

    # Kinematic viscosity and thermal diffusivity calculations
    nu_humid = mu_humid / rho_humid  # Kinematic viscosity (m²/s)
    alpha_humid = alpha0 * (T_K / T0) ** 1.5  # Thermal diffusivity (m²/s)

    # Diffusivity of water vapor in air
    D_m = 2.26e-5 * (T_K / 273.15) ** 1.81  # Diffusivity of water vapor (m²/s)

    # Dimensionless numbers calculations
    Re = (rho_humid * air_speed * d) / mu_humid  # Reynolds number
    Sc = mu_humid / (rho_humid * D_m)  # Schmidt number
    Pr = (cp_moist_air * mu_humid) / k_moist_air  # Prandtl number

    # Sherwood number
    Sh = 2 + 1.3 * (Sc ** 0.15) + 0.66 * (Sc ** 0.31) * (Re ** 0.5)  # Sherwood number

    # Mass transfer coefficient
    h_m = (Sh * D_m) / d  # Mass transfer coefficient (m/s)

    # Nusselt number and surface heat transfer coefficient
    Nu = 2 + (0.6 * Re ** 0.5 * Pr ** (1 / 3))  # Nusselt number
    h_T = (Nu * k_moist_air) / 3.14e-5  # Heat transfer coefficient (W/m²·K)

    # Lewis number and mass transfer coefficient
    Lewis = k_moist_air / (rho_humid * cp_moist_air * 7.50e-14)  # Lewis number
    h_mass = h_T / (rho_humid * cp_moist_air * (Lewis ** (2 / 3)))  # Mass transfer coefficient (m/s)

    # Surface area of apple
    surface_area_apple = (0.0581 * (new_fruit_masses[-1] / 1000) ** 0.685)  # Surface area (m²)

    # Volume of condensation per unit time
    v1 = surface_area_apple * h_m  # Volume rate (m³/s)

    # Water content of air and surface
    xL_cuv_air = 1000 * 0.622 * pair / (100 * p_bar - pair)  # Specific humidity of air (g/kg)
    xL_cuv_surf = 1000 * 0.622 * psl_cuv_surf / (100 * p_bar - psl_cuv_surf)  # Specific humidity of surface (g/kg)
    rhoL_cuv = ((1 + xL_cuv_air / 1000) * 100) / ((0.622 + xL_cuv_air / 1000) * 0.46152 * (T_K))  # Air density (kg/m³)
    rhoL_cuv_surf = ((1 + xL_cuv_surf / 1000) * 100) / ((0.622 + xL_cuv_surf / 1000) * 0.46152 * (T_K))  # Surface density (kg/m³)
    xL_cuvv_air = xL_cuv_air * rhoL_cuv  # Water vapor density of air (g/m³)
    xL_cuvv_surf = xL_cuv_surf * rhoL_cuv_surf  # Water vapor density of surface (g/m³)

    # Dew point temperature
    Tdp = (243.04 * (math.log(humi / 100) + (17.625 * t_air) / (243.04 + t_air))) / \
          (17.625 - (math.log(humi / 100) + (17.625 * t_air) / (243.04 + t_air)))  # Dew point (°C)

    # Condensation or evaporation
    if (xL_cuvv_air > xL_cuvv_surf) or (t_surf < Tdp):
        condensation = "Yes"
        condensed_capacity = (xL_cuvv_air - xL_cuvv_surf) * v1 * time_difference  # (g)
        if condensed_capacity < 0:
            condensed_capacity = 0
    else:
        condensation = "No"
        condensed_capacity = (xL_cuvv_air - xL_cuvv_surf) * v1 * time_difference  # (g)
        if condensed_capacity > 0:
            condensed_capacity = 0

    cumulative_condensation += condensed_capacity  # (g)
    if cumulative_condensation < 0:
        cumulative_condensation = 0

    if cumulative_condensation > 0:
        predicted_retention_time += time_difference / 60  # (minutes)

    # Mass loss due to transpiration
    if cumulative_condensation == 0:
        mass_loss_due_to_transpiration = surface_area_apple * 1000 * (pair - psl_cuv_surf) * time_difference / \
                                         ((1 / 2.03e-9) + (1 / h_m))  # (g)
    else:
        mass_loss_due_to_transpiration = 0

    # Oxidative mass loss
    rco2 = 1172783.97 * math.exp(-63111.14 / (8.314 * T_K))  # Respiration rate constant (kg/s·mol)
    oxidative_mass_loss = float((new_fruit_masses[-1] / 1000) * rco2 * time_difference * (180 - 108) / 264)  # (g)

    # Update cumulative mass loss
    new_cumulative_mass_loss = cumulative_mass_loss[-1] + mass_loss_due_to_transpiration - oxidative_mass_loss  # (g)
    cumulative_mass_loss.append(new_cumulative_mass_loss)

    # New fruit mass with condensation
    new_fruit_mass_with_condensation = (new_fruit_masses[-1]) - oxidative_mass_loss + mass_loss_due_to_transpiration + \
                                        (cumulative_condensation - cumulative_condensation_list[-1])  # (g)
    new_fruit_masses.append(new_fruit_mass_with_condensation)

    # Output results in printed form or real-time graphs
    print(f"Condensation: {condensation}")
    print(f"Cumulative Condensation: {cumulative_condensation:.2f} g")
    print(f"Mass Loss Due to Transpiration: {mass_loss_due_to_transpiration:.2f} g")
    print(f"Oxidative Mass Loss: {oxidative_mass_loss:.2f} g")
    print(f"New Fruit Mass: {new_fruit_mass_with_condensation:.2f} g")

    # Simulate real-time loop
    time.sleep(60)
