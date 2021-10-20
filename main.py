from data import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import delft_physics_lab as dpl

def func(z, a):
    return a / z**4

# to calculate the deviation of F, we use a dummy value of a (through later division, it shows that this will not impact the outcome)

F_prime, F = dpl.std_approximation(func, [(r_aan, u_r_aan), (1, 0)], approx_type='functional', evaluate=True)

# since a is directly proportional to F, the relative deviation of the two is equal
dev = ((F_prime/F)**2+(u_F/F_aan)**2)**.5

popt, pcov = curve_fit(func, r_aan, F_aan, sigma=dev)

def get_B(a, d, h):
    V = (d/2)**2 * np.pi * h
    mu = 1.25663753e-6
    m = (a * 2 * np.pi/(3 * mu))**(1/2)
    B = mu * m/V
    return B

c_u_a, c_a = dpl.std_approximation(get_B, [(popt[0], popt[0]*np.mean(dev)), (10e-3, .1e-3), (5e-3, .1e-3)], approx_type='calculus', evaluate=True)

print(c_a, c_u_a)

