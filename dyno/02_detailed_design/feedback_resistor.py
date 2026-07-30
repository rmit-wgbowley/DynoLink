"""
Filename: feedback_resistor.py

Description:
    Calculates the size of the feedback resistors for the TPS7A30xx 
    to get a 5V output from 10 V input voltage with 100mA output.
    
    Also calculates the approximate power loss through the different
    components.
    
    NOTE:
    This script does use my custom framework picounits.
    
    NOTE:
    Reference the ido_tps7a49 document -> for application specifics
"""

from picounits import VOLTAGE, TIME, CURRENT, RESISTANCE, CAPACITANCE, MICRO, KILO, MILLI, NANO

# Parameters
v_in = 10 * VOLTAGE
v_out = 5 * VOLTAGE
i_out = 100 * MILLI * CURRENT
i_q = 55 * MICRO * CURRENT

v_feedback = 1.185 * VOLTAGE
r2 = 10 * KILO * RESISTANCE
c_ss = 10 * NANO * CAPACITANCE
start_up_ratio = 1.4 * ((1*MILLI*TIME)/(1*NANO*CAPACITANCE))

# Equations for the ido_tps7a49
r1 = r2 * (v_out/v_feedback - 1)
t_ss = start_up_ratio * c_ss
power_loss = (v_in - v_out) * i_out + i_q * v_in

# ~ Power loss through resistors
total_r = r1 + r2
current = v_out/total_r

r_1_losses = current ** 2 * r1
r_2_losses = current ** 2 * r2

print(f"v_in: {v_in:.3f}, v_out: {v_out:.3f}")
print(f"r_1: {r1:.3f}, r_2: {r2:.3f}")
print(f"LDO Power loss: {power_loss:.3f} @ {i_out:.3f}, Start_up time: {t_ss:.3f}")
print(f"R1_loss: {r_1_losses:.3f}, R2_loss: {r_2_losses:.3f}")
