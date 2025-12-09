# High Voltage Transmission Line Positioning Analysis
### Task for VEV in STUBA
______
## Tasks
 * Analyze inserted data via .cvs file of landscape
 * Calculate and measure best positions for line
 * Optimize line parameters for best usage 
 * Add automatisation 
______
Task status due 09/12/2025 - **_Finished_**

---

## Code Structure

```
HV_Transmission_Line_Analysis/
├── main.py                  # Main execution script
├── constants.py            # Task basis 
├── cable_parameters.py     # Cable resistance calculations
├── ampacity.py             # Ampacity calculations  
├── montage_tables.py       # Montage state equations and tables
├── vibration_control.py    # Vibration and minimal height checks
└── data/
    ├── data.csv            # Terrain elevation data
    └── *.xlsx             # Output tables
```

### Module Descriptions

**cable_parameters.py**  
Calculates AC resistance at 80°C considering skin effect and temperature coefficients.

**ampacity.py**  
Determines maximum current capacity based on:
- Solar radiation heating
- Convective cooling
- Radiative heat transfer

**montage_tables.py**  
Generates sag-tension tables for:
- Different temperature conditions (-30°C to +80°C)
- Ice loading conditions
- Wind loading conditions
- Combined loading scenarios

**vibration_control.py**  
Analyzes:
- Aeolian vibration risk zones
- Minimum ground clearance (12m requirement)
- Vibration damper requirements

---
