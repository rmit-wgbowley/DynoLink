<!--
Colors:
FFFFFF - Pure white
e01e37 - Bold crimson-red 
-->


<div align="center">
  <table>
    <tr>
      <td><img src="./media/ecu_side_on_table.jpg" alt="ECU-Side Board" style="max-width:300px;"></td>
      <td><img src="./media/dyno_side_on_box.jpg" alt="Dyno-Side Board" style="max-width:300px;"></td>
    </tr>
    <tr>
      <td><em>ECU-Side Board on table</em></td>
      <td><em>Dyno-Side Board on DCS800</em></td>
    </tr>
  </table>
</div>


### Overview

![MIT License](https://img.shields.io/badge/License-MIT-FFFFFF?style=flat-square&logoColor=black)
![Electrics](https://img.shields.io/badge/Domain-Electrics-e01e37?style=flat-square&logoColor=black)
![Dyno System](https://img.shields.io/badge/System-Dyno-FFFFFF?style=flat-square&logo=speedtest)

The RMIT dyno setup consists of two systems: the dyno controller panel (DCS800) and the r19e ECU. This allows the vehicle's powertrain system to be validated before implementation. 
The ECU controls the load motor and HV system. 
However, for this test setup, it is also meant to transmit a `0-3.3 V` PWM signal to control the dyno motor RPM. 
This allows a lookup table to be used to ramp up the dyno motor (a former elevator motor) RPM in an arbitrary function.

#### Objectives

```
- [x] Safely interface a 3.3 V STM32 PWM output with a 0–10 V dyno controller input.
- [x] Provide galvanic isolation between the ECU and dyno controller.
- [/] Maintain signal integrity over 2–4 m cable runs.
```

> *(Note). `[ ]` Not started. `[/]` In progress. `[x]` Complete.*

---

### Control Strategy

The 2026 dyno setup uses speed control on the dyno side and torque control on the load motor. 
This allows a lookup table to be used to ramp up the dyno RPM to model RPM vs torque. 
For example, the dyno-side RPM over time could be modelled as this arbitrary function:

$$ RPM(t) = \frac{A}{2B}(1-\cos(\frac{\pi t}{t_{total}})), \quad RPM(t) \in [0, dyno_{max}] $$

Where `A` is the target RPM at the load side, `B` is the gearing ratio between the dyno motor and load motor, and `t_total` is the total time to reach that requested RPM. 
The requested RPM then needs to be converted to duty cycle:

$$ DC(t) = (\frac{C \times RPM(t)}{2})(\frac{3.3}{5})(\frac{100}{3.3})$$
$$ DC(t) = 10C \times RPM(t), \quad DC(t) \in [0, 100]$$

And then it would simply be transformed into a simple lookup table, assuming `C` is the dyno controller input scaling factor `(V/RPM)` after the 2× amplification stage.

<br>

The dyno has a `200 kΩ` input impedance (AI1), an analog range of `0–10 V` with a linear factor of `5 mV/RPM`, and a maximum safe RPM of `1800` at the dyno-side motor. 
The r26 powertrain has a gearing of `1:12.81`. Driving frequency table (ARR), output ripple at the dyno, and duty-cycle resolution trade-offs can be found [here](./domain/readme.md).

| Step | Time (s) | ECU Duty Cycle (%) | Dyno Controller Input (V) | Target Dyno (RPM) | Target Load (RPM) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 0 | 0.00 | 0.00 | 0.0  | 0  | 0 |
| 1 | 0.25 | 0.26 | 0.03 | 5  | 64 |
| 2 | 0.50 | 0.98 | 0.10 | 20 | 256 |
| 3 | 0.75 | 1.95 | 0.20 | 39 | 500 |
| 4 | 1.00 | 2.93 | 0.29 | 59 | 755 |
| 5 | 1.25 | 3.64 | 0.36 | 73 | 935 |
| 6 | 1.50 | 3.90 | 0.39 | 78 | 999 |

*Figure 1: Example profile parameters configured for a real-time `1.5-second` window with time steps of `250 ms` using `A = 1000`, `B = 12.81`, and `c = 0.005`.*

> The program used to generate that table can be found [here](./domain/example_profiles.py)

However, for the real system, race day data is used to model the dynamic torque loading on the load motor.

---

### High-level Topology

The dyno controller and r19e ECU are approximately `2-4 meters` apart and operate at different voltage levels (`0-3.3V` vs `0-10V`). An ECU conditioning and isolation board is used on one end, and a dyno receiver and amplification board on the other. Due to the electrical noise produced by the dyno motors, an `RS-422` differential link was used.

```
Interface (2.54mm Pitch Male Header)
ECU PWM Source (Digital 3.3 V - PB13, TIM1_CHN1, STM32F405RGT6)
                    ↓

Interface (JST XH 4-pin 2.5mm)
ECU Side (3.3 V logic / 5 V domain) (Conditioning / Isolation)
--------------------------------------------
Schmitt Trigger (Edge Conditioning)
    ↓
Digital Isolator (Isolates the PWM Signal) ← (Isolated 5 V Domain)
    ↓
RS-422 Driver (A/B Differential Pair)
-------------------------------------------- 
Interface Socket (RJ45)
                    ↓

CAT 5/6 Cable
--------------------------------------------
Twisted Pairs: (+Signal, -Signal)
--------------------------------------------
                    ↓

Interface Socket (RJ45)
DYNO Side (5 / 10 V domain) (Receiver / Amplification) 
--------------------------------------------
RS-422 Receiver (Differential Input, Rejects Noise) ← (5 V LDO)
    ↓
RC Low-Pass Filter (50 Hz) (PWM to DC Voltage Conversion)
NOTE:
Ripple magnitude depends on PWM frequency,
filter capacitance, and filter resistance.
    ↓
Op-Amp 2× Gain (Non-Inverting) (Scales to 0–10V ADC Input Range) ← 10 V Line
--------------------------------------------- 
Interface (JST XH 4-pin 2.5mm)
                    ↓
Interface (4-pin Barrel Jack) (Unknown Specifics)
DYNO Controller (Analog 10V Input)
```

---

### Case Design

<p align="center">
  <img src="media/dyno_side_case.png" alt="Dyno-side case render" style="max-width:600px;">
</p>
<p align="center">
  <em>Housing design (identical for both ECU-side and Dyno-side boards)</em>
</p>

Case design files: [Available here (Fusion source files)](domain/03_cad/)

```
- Same case size and external design for both boards — only internal PCBs differ
- IGES format included for users without Fusion
- 4× M3 inserts for mounting PCB and top housing
- Velcro recommended to secure the housing to the test bench
```

---

### Documentation

Design notes, validation results, design iterations, and implementation 
decisions are documented in the repository [issues](https://github.com/rmit-wgbowley/dyno-boards/issues).

#### Tags

```
Project Progress:
----------------------------------------------------
LX → Documentation and project structure
L0 → Review and analysis of reference designs
L1 → System level design, topology and interfaces
L2 → Detailed design & prototyping
L3 → Testing & Validation of prototype
----------------------------------------------------
```

<br>

```
Miscellaneous:
----------------------------------------------------
DS → De-scoped Feature, De-scoped Analysis
AC → Architectural Change
----------------------------------------------------
```

---