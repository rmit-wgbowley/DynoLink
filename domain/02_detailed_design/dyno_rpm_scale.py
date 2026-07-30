"""
Filename: dyno_rpm_scale.py

Description:
    Calculates the dyno rpm scale for the A13 input which is
    0-10V analog with a discretization of 5mV per rpm.

    The dyno (AI1 & AI2) inputs have impedances of 200kOhm 
    and sampling of 3.3ms.
    
    NOTE:
    This script does use my custom framework picounits

    NOTE:
    The current test load is a 8 pole fischer PMSM with a
    planetary gearbox of with a 1:12.81. Hence this analytical
    analysis will be using that ratio.

    NOTE:
    The input signal is 10kHz hence with the current RC filter
    before the 2x op-amp. ~1.6uF & 2kOhms with a pre-amplification
    ripple of ~78.5mV & time-constant of 3.183ms
    
    NOTE:
    The AI1 Input is modelled as a RC filter with a time constant of 
    3.3ms hence the total attenuation is first_order (rc filter) *
    second_order (AI1 input). THIS IS AN ASSUMPTION. NOT VALIDATED.
    
    Validate:
    RC filter attenuation (first order)
    Assumed:
    AI1 attenuation (second order)
"""

from math import pi
from picounits import VOLTAGE, TIME, FREQUENCY, KILO, MILLI

# Script control
sampling = 3.3 * MILLI * TIME
frequency = 10 * KILO * FREQUENCY
step_size = 100
ratio = 12.81

# Dyno discretization (10V/5mV)
max_voltage = 10 * VOLTAGE
rpm_step = 5 * MILLI * VOLTAGE

# Output ripple voltage
time_constant = 3.183 * MILLI * TIME
ripple_voltage = 78.5 * MILLI * VOLTAGE
posted_amplification = 2 * ripple_voltage

# Output Attenuation
first_order = 1 / ((1 + (2 * pi * frequency * time_constant) ** 2) ** 0.5)
second_order = 1 / ((1 + (2 * pi * frequency * sampling) ** 2) ** 0.5)
total_attenuation = first_order * second_order

effective_ripple = posted_amplification * total_attenuation
effective_ripple_tolerance = effective_ripple / 2

rpm_dyno_ripple = effective_ripple / rpm_step
rpm_load_ripple = ratio * rpm_dyno_ripple

rpm_dyno_tolerance = rpm_dyno_ripple / 2
rpm_load_tolerance = rpm_load_ripple / 2

# Information Print out
print("-------------------------------------------------")
print(f"SET Driving frequency: {frequency:.3f} | SET RC ripple: {ripple_voltage:.3f} | tau: {time_constant:.3f}")
print(f"Total Attenuation: {total_attenuation:.3f}")
a13_input = 0 * VOLTAGE
while a13_input < max_voltage:
    a13_input += step_size * rpm_step
    dyno_rpm = a13_input / rpm_step
    load_rpm = ratio * dyno_rpm

    # Duty Cycle
    pre_amplification = a13_input / 2
    pre_isolation = 3.3 * pre_amplification / 5 # Isolator (3.3v -> 5v)
    duty_cycle = pre_isolation / (3.3 * VOLTAGE) * 100

    print("-------------------------------------------------")
    print(f"ECU output: {frequency:.3f} @ {duty_cycle:.3f} %")
    print(f"A13 Analog Input: {a13_input:.3f} +/- {effective_ripple:.3f}")
    print(f"Dyno-side RPM: {dyno_rpm:.3f} +/- {rpm_dyno_tolerance:.3f}")
    print(f"Load-side RPM: {load_rpm:.3f} +/- {rpm_load_tolerance:.3f}")
