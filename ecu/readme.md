### ECU-side Topology & Components

```
Interface (2.54mm Pitch Male Header)
ECU PWM Source (Digital 3.3 V @ 10 kHz - PB13, tim1_CHN1, STM32F405RGT6)
                    ↓
Interface (JST XH 4-pin 2.5mm)
ECU Side (3.3 V logic / 5 V domain) (conditioning / isolation)
--------------------------------------------
Schmitt trigger (Cleans up the signal edge) (SN74LVC1G17)
    ↓
Digital Isolator (Isolates the PWM signal) (ISO7720) <- RFM-0505S (isolated 5 V)
    ↓
RS-422 Driver (A/B differential pair) (AM26LS31)
--------------------------------------------
Interface Socket (RJ45) (twisted pairs: +signal, -signal)
                    ↓
Interface (RJ45) 
DYNO Side (5/10 V domain) (receiver / amplification) 
```

