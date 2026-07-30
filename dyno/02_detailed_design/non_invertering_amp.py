""""
Filename: non_inverting_amp.py

Description:
    Calculates the feedback resistor & the r2 resistor 
    for the opa4277 to ensure a 2x gain from 5v out of the 
    rc filter.
    
    NOTE:
    This script does use my custom framework picounits.
"""


from picounits import Q as q, unit_validator
from picounits import KILO, RESISTANCE

gain = 2
res_2 = 1 * KILO * RESISTANCE

@unit_validator(RESISTANCE)
def calculates_feedback(gain: q) -> q:
    """ Calculates the feedback resistor required for gain"""
    return (gain - 1) * res_2

feedback = calculates_feedback(gain)

print(f"resistor 2: {res_2:.3f}")
print(f"Feedback resistor: {feedback:.3f} @ {gain:.2f} Gain")
