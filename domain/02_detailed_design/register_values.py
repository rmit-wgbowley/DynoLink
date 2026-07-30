"""
Filename: register_values.py

Description:
    Calculates the different ARR values to get 
    fine control over the dyno RPM while limiting 
    RC ripple from the digital to analog conversion
    stage.
"""

from picounits import (
    unit_validator, Q, 
    VOLTAGE, NULLSET, FREQUENCY, RESISTANCE, CAPACITANCE, MEGA, KILO, MICRO, MILLI,
)

# Script Variables
v_supply = 10 * VOLTAGE
v_per_rpm = 5 * MILLI * VOLTAGE
rpm_control_max = 100
f_clock = 1600 * MEGA * FREQUENCY

# THESE ARE THE DYNO SIDE OUTPUT STEP
v_step = 1 * MILLI * VOLTAGE
step_size = 1 * MILLI * VOLTAGE

c = 1.6 * MICRO * CAPACITANCE
r = 2 * KILO * RESISTANCE

# Arbitrary limits (1 step per 10 rpm available)
max_resolution_limit = 200

@unit_validator(NULLSET)
def tim1_ARR(v_source, v_step) -> Q:
    """ Calculates the ARR for that step control"""
    return round(v_source/v_step - 1, 0)


def tim1_frequency(psc, arr, f_tim) -> Q:
    """ Calculates the driving frequency with that ARR value """
    return f_tim / ((psc+1)*(arr+1))


def ripple(v: Q, r: Q, c: Q, f: Q) -> Q:
    """ Calculates the ripple at that frequency """
    return (v/2) / (f*c*r)

# Print table header with values
print("-------------------------------------------------")
print(f"Clock Speed: {f_clock:.3f}, Resistance: {r:.3f}, Capacitance: {c:.3f}")
print("-------------------------------------------------")


resolution = 1e10
while resolution > max_resolution_limit:
    arr = tim1_ARR(v_supply, v_step)
    resolution = arr + 1

    # Assumes PSC=0, ARR is control factor
    frequency = tim1_frequency(0, arr, f_clock)
    v_ripple = ripple(v_supply, r, c, frequency)

    # Prints table
    print(
        f"rpm_step: {v_step*(1/v_per_rpm):.3f}, "
        f"ARR: {arr:.3f}, Frequency: {frequency:.3f}, Output ripple {v_ripple:.3f}"
    )

    # Updates for each
    v_step += step_size
