# Output Dynamics Based on Frequency Changes (FOR STM32F405RGT6)

> [!important]
> Assumed Configuration:
> - PSC = 0
> - RC Characteristics: 2 kΩ, 1.6 µF
> - Clock Speed: 160 MHz on TIM1_CH1N (APB2)
> - APB2 (Scale of 2x) → PCLK2 (80 MHz) → 160 MHz
> - These values will be different if R7 and C9 are populated with (47 Ω | 100 nf, etc.)

## Initial Calibration Row (10 kHz)

| RPM Step (at Dyno) | ARR | Frequency | Output Ripple (After 2x @ DYNO) |
|--------------------|-----|-----------|--------------------------|
| 0.625 rpm | 15999 | 10.000 kHz | 156.080 mV |

## Main Table (0.2 rpm Resolution)

| RPM Step (at Dyno) | ARR | Frequency | Output Ripple (After 2x @ DYNO) |
|--------------------|-----|-----------|--------------------------|
| 0.200 rpm | 9999 | 16.000 kHz | 97.656 mV |
| 0.400 rpm | 4999 | 32.000 kHz | 48.828 mV |
| 0.600 rpm | 3332 | 48.005 kHz | 32.549 mV |
| 0.800 rpm | 2499 | 64.000 kHz | 24.414 mV |
| 1.000 rpm | 1999 | 80.000 kHz | 19.531 mV |
| 1.200 rpm | 1666 | 95.981 kHz | 16.279 mV |
| 1.400 rpm | 1428 | 111.966 kHz | 13.955 mV |
| 1.600 rpm | 1249 | 128.000 kHz | 12.207 mV |
| 1.800 rpm | 1110 | 144.014 kHz | 10.850 mV |
| 2.000 rpm | 999 | 160.000 kHz | 9.766 mV |
| 2.200 rpm | 908 | 176.018 kHz | 8.877 mV |
| 2.400 rpm | 832 | 192.077 kHz | 8.135 mV |
| 2.600 rpm | 768 | 208.062 kHz | 7.510 mV |
| 2.800 rpm | 713 | 224.090 kHz | 6.973 mV |
| 3.000 rpm | 666 | 239.880 kHz | 6.514 mV |
| 3.200 rpm | 624 | 256.000 kHz | 6.104 mV |
| 3.400 rpm | 587 | 272.109 kHz | 5.742 mV |
| 3.600 rpm | 555 | 287.770 kHz | 5.430 mV |
| 3.800 rpm | 525 | 304.183 kHz | 5.137 mV |
| 4.000 rpm | 499 | 320.000 kHz | 4.883 mV |
| 4.200 rpm | 475 | 336.134 kHz | 4.648 mV |
| 4.400 rpm | 454 | 351.648 kHz | 4.443 mV |
| 4.600 rpm | 434 | 367.816 kHz | 4.248 mV |
| 4.800 rpm | 416 | 383.693 kHz | 4.072 mV |
| 5.000 rpm | 399 | 400.000 kHz | 3.906 mV |
| 5.200 rpm | 384 | 415.584 kHz | 3.760 mV |
| 5.400 rpm | 369 | 432.432 kHz | 3.613 mV |
| 5.600 rpm | 356 | 448.179 kHz | 3.486 mV |
| 5.800 rpm | 344 | 463.768 kHz | 3.369 mV |
| 6.000 rpm | 332 | 480.480 kHz | 3.252 mV |
| 6.200 rpm | 322 | 495.356 kHz | 3.154 mV |
| 6.400 rpm | 311 | 512.821 kHz | 3.047 mV |
| 6.600 rpm | 302 | 528.053 kHz | 2.959 mV |
| 6.800 rpm | 293 | 544.218 kHz | 2.871 mV |
| 7.000 rpm | 285 | 559.441 kHz | 2.793 mV |
| 7.200 rpm | 277 | 575.540 kHz | 2.715 mV |
| 7.400 rpm | 269 | 592.593 kHz | 2.637 mV |
| 7.600 rpm | 262 | 608.365 kHz | 2.568 mV |
| 7.800 rpm | 255 | 625.000 kHz | 2.500 mV |
| 8.000 rpm | 249 | 640.000 kHz | 2.441 mV |
| 8.200 rpm | 243 | 655.738 kHz | 2.383 mV |
| 8.400 rpm | 237 | 672.269 kHz | 2.324 mV |
| 8.600 rpm | 232 | 686.695 kHz | 2.275 mV |
| 8.800 rpm | 226 | 704.846 kHz | 2.217 mV |
| 9.000 rpm | 221 | 720.721 kHz | 2.168 mV |
| 9.200 rpm | 216 | 737.327 kHz | 2.119 mV |
| 9.400 rpm | 212 | 751.174 kHz | 2.080 mV |
| 9.600 rpm | 207 | 769.231 kHz | 2.031 mV |
| 9.800 rpm | 203 | 784.314 kHz | 1.992 mV |
| 10.000 rpm | 199 | 800.000 kHz | 1.953 mV |
