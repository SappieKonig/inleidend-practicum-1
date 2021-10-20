#Metingen vooraf
import delft_physics_lab as dpl
import numpy as np


d_m_aan = (5.0e-3, .5e-3)
d_m_af = (5.0e-3, .5e-3)
d_m_onder = (5.0e-3, .5e-3)
h_1 = (3.5e-3, .5e-3)
h_2 = (3.8e-3,  .5e-3)

# Measurements: Explain the names of variables provide only raw data in np.arrays!
#Raw measurements

g = 9.812 #m/s^2
p = (3.5e-3, .5e-3) #Distance from bottom of ruler to top of bottom magnet

h_12_af = np.array([19.8, 23.0,  29.2,\
                       36.9,   57.8,  26.0,\
                       41,   48.1,  24,\
                       21,   22.4,  23.2]) / 1000
u_h_12_af = 3e-3

F_af =    g * np.abs(np.array([-0.013,  -0.009,  -0.006,\
                     -0.004,  -0.001,  -0.007,\
                       -0.003,   -0.002,  -0.008,\
                       -0.012,   -0.011,  -0.010]))

h_12_aan = np.array([3.5,   6.1,  4.8,\
                    9.0,   11.5,  14,\
                        16.3,  18,  23,\
                        24.3,   26.9,  39.7]) / 1000
u_h_12_aan = 3e-3

F_aan =     g * np.array([0.244,   0.136,  0.200,\
                         0.074,   0.046,  0.032,\
                        0.020,   0.015,  0.007,\
                        0.005,   0.004,  0.001])

h_12_concat = np.concatenate((h_12_af, h_12_aan))
F_concat = np.concatenate((F_af, F_aan))

u_F = .01

#Data processing and analysis:

def get_r(h_12, p, d_m_boven, d_m_onder, h_1, h_2):
    return h_12 - p + .5*d_m_onder + .5*d_m_boven + h_1 + h_2

u_r_af, r_af = dpl.std_approximation(get_r, [(h_12_af, u_h_12_af), p, d_m_af, d_m_onder, h_1, h_2], approx_type='calculus', evaluate=True)
u_r_aan, r_aan = dpl.std_approximation(get_r, [(h_12_aan, u_h_12_aan), p, d_m_aan, d_m_onder, h_1, h_2], approx_type='calculus', evaluate=True)


