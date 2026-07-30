"""
Filename: Low_bypass_filter.py

Description:
    Calculates the size of the capacitor and resistor to 
    ensure the cutoff frequency is meant and the rise time
    isn't too slow.
    
    Time constant -> R & C proportionally
    Cutoff frequency -> 1/R & 1/C
    Hence fixed R (reduces voltage drop), dynamic Cap
    
    NOTE:
    This script does use my custom framework picounits.
"""

from math import pi
from picounits import KILO, NANO, VOLTAGE, FREQUENCY, RESISTANCE, CAPACITANCE

v_supply = 5 * VOLTAGE
amplification_gain = 2

pwm_frequency = 10 * KILO * FREQUENCY
cutoff = 50 * FREQUENCY
r1 = 2 * KILO * RESISTANCE
c1 = 100 * NANO * CAPACITANCE

# If c_total > c1, you need to add an extra capacitor (c_extra)
c_total = 1 / (2 * pi * cutoff * r1)
c_extra = c_total - c1

# total capacitance for ripple and timing calculations
time_constant_total = c_total * r1
settling_time = 5 * time_constant_total
ripple = (v_supply * 0.5) / (pwm_frequency * r1 * c_total)

print(f"c_total: {c_total:.3f}, c_extra: {c_extra:.3f}")
print(f"time constant: {time_constant_total:.3f}")
print(f"settling_time: {settling_time:.3f}")
print(f"ripple_in: {ripple:.3f}, ripple_out: {ripple*amplification_gain:.3f}")
print(f"Ripple ratio of range: {ripple/v_supply*100:.3f} %")
