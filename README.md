# Nev_health: Assessing the Contribution of New Energy Vehicles to Air Pollution Reduction and Health Impacts in Chinese Cities

This repository contains the code and analysis scripts for the study on **the role of New Energy Vehicles (NEVs) in reducing urban air pollution and the associated health impacts**. The project includes three main components: trends in air pollution, pollution modeling using NEVs and fossil vehicles (FV), and health impact analysis.  

This repository is structured to reproduce figures and analyses presented in the corresponding Nature Health submission. All code has been organized for clarity and reproducibility.

---

## Project Structure

### 1. `trend_of_air_pollution/`
This folder contains scripts to analyze **annual trends of air pollutants** in Chinese cities and visualize city-level changes.

- `Annual_variation_trends_allcity_general.py`  
  Computes and visualizes annual variation trends for multiple pollutants across all cities.

- `Scatter_plot_for_change_rate_cities.py`  
  Generates scatter plots of pollutant change rates between years for different cities.

- `Draw_city_change_rate_difference_distribution.py`  
  Plots the spatial distribution and difference of pollutant change rates for each city.

---

### 2. `pollution_NEV_FV_RF_regression_model/`
This folder implements **Random Forest regression models** to quantify the contribution of NEVs and fossil vehicles to urban air pollution and evaluate model accuracy using bootstrapping.

- `RF_regression_pollution_vehicles_Bootstrap.py`  
  Main RF regression script with bootstrap resampling for uncertainty quantification. Computes feature importance (SHAP values) and predicted pollutant reductions contributed by NEVs.

- `Draw_Bootstrap_models_accuracy.py`  
  Generates publication-quality figures showing model accuracy metrics (R², RMSE, MAE, MAPE) for different pollutants.

- `Draw_NEV_contributed_air_pollution_change_distribution.py`  
  Produces city-level spatial maps showing the NEV contribution to the observed change in pollutant concentrations.

---

### 3. `health_impact_analysis/`
This folder contains scripts to evaluate health impacts associated with changes in air pollution due to NEV adoption.  
Current scripts include:

- `Calculate_health_impact_CO_2023.py` — Estimates health impacts attributable to CO exposure in 2023.  
- `Calculate_health_impact_NO2_2023.py` — Estimates health impacts attributable to NO₂ exposure in 2023.  
- `Calculate_health_impact_PM10_2023.py` — Estimates health impacts attributable to PM₁₀ exposure in 2023.  
- `Calculate_health_impact_PM25_GEMM_2023.py` — Estimates health impacts attributable to PM₂.₅ exposure in 2023 using GEMM methodology.  
- `Kruskal–Wallis test.py` — Performs non-parametric Kruskal–Wallis statistical tests to assess differences between groups.  

---

## Dependencies

The code requires the following Python packages:

- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `shap`
- `mpl_toolkits.basemap` (for city-level maps)
- `openpyxl` (for reading/writing Excel files)


##  Notes

The code is research-oriented and may require modification of file paths to match your local environment.

Figures generated are designed to meet Nature journal style requirements (font: Arial, high-resolution, publication-ready).

The health_impact_analysis/ module is under active development and will be updated with reproducible health impact calculations.

The current release (v1.0) contains the main framework of the analysis. Subsequent versions will include full datasets and completed health impact scripts.


## License

This repository uses an Open Source Initiative-approved license (MIT by default). Users are free to use and modify the code with proper citation.

## Citation

If you use this code in your research, please cite:

Qianqian Yang et al., Nev_health: Initial release of Nev_health code, Zenodo, DOI: 10.5281/zenodo.19065317



You can install them using:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn shap basemap openpyxl

## Usage

1. **Clone the repository:**

```bash
git clone https://github.com/Qianqian-Yang/Nev_health.git
cd Nev_health

2. **Navigate to the folder corresponding to the analysis you want to reproduce, e.g.:**

```bash
cd pollution_NEV_FV_RF_regression_model
python RF_regression_pollution_vehicles_Bootstrap.py
