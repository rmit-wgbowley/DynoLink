### Dyno Side Topology & Components

```
Interface (RJ45) 
ECU Side (5V PMW twisted pairs: +signal, -signal)
                    ↓
Interface (RJ45) 
DYNO Side (5/10 V domain) (receiver / amplification) 
--------------------------------------------
5V Line ← (TPS7A4901, 14 ms start-up, 0.1–0.5 W | R1 = 10 kΩ & R2 = 33 kΩ)
    ↓
RS-422 receiver (Differential input, rejects noise) (AM26LS32AIN)
    ↓
RC low-pass filter (50 Hz) (PWM to DC voltage conversion)
    ↓
Op-amp 2× Gain (Scales to 0–10 V) (TLV272) ← 10 V Line
---------------------------------------------
Interface (JST XH 4-pin 2.5 mm)
                    ↓
Interface (4-pin barrel jack) (Unknown Specifics)
DYNO Controller (Analog 10V Input)
```