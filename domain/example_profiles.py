"""
Filename: example_profiles.py

Description:
    Generates an example input curve with duty cycle and 
    example rpm ramp up based on the dyno's 5mv per 1 RPM
    and the 3.3v to 10v amplification.

    NOTE:
    DIRECTION -> True = RPM ramp up, False = RPM ramp down
"""

from math import cos, pi

# Controls
DIRECTION = True
TABLE = True

# Parameters
time_step = 0.250
total_time = 1.5

target_rpm = 1000
gearing = 12.81
conversion = 0.005
analog_max = 10

def rpm_ramp(t, a, b, t_total):
    """ Dyno side rpm function """
    if DIRECTION:
        return a/(2*b) * (1-cos(pi*t/t_total))

    return a - a/(2*b) * (1-cos(pi*t/t_total))


def duty_cycle(rpm, c):
    """ Rpm to duty cycle with duty cycle clamp """
    dc = 10 * c * rpm
    return min(max(dc, 0), 100)

t = 0
lookup_table = []
while t < total_time + 1*time_step:
    rpm = rpm_ramp(t, target_rpm, gearing, total_time)
    dc = duty_cycle(rpm, conversion)

    ai1 = (dc/100) * analog_max
    print(f"Time: {t:.3f}s, ECU Duty Cycle: {dc:.2f}%, Dyno target rpm: {rpm:.0f}, AI1: {ai1:.2f}v")

    lookup_table.append({'time (s)': t, 'duty_cycle (0-100)': dc})
    t += time_step
