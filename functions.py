import numpy as np
from scipy.special import lambertw, erfc, erfcinv
import config

def invW(x):
    return x*np.exp(x)


def invQ(x):
    return np.sqrt(2) * erfcinv(2 * x)

def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))

def BER_SNR(BER):
    return 2*(invQ(BER)**2)

def C_SNR(C):
    return np.exp2(C/config.B)-1

def D_SNR(d):
    return (config.P_r * 2 * np.pi * (1 - np.cos(config.theta_1_e)) * (config.rho_t * config.rho_r) * (config.v**2)*(config.l**2) * (2/config.k * invW(config.k/2*d-config.n_i))**2) / (config.sigma_i**2 * config.r * np.cos(config.theta_i))


def calc_d_with_snr(snr):
    return 2/config.k*np.real(lambertw(config.k/2*np.sqrt(snr*(config.sigma_i**2)*config.r*np.cos(config.theta_i)/(config.P_r*2*np.pi*(1-np.cos(config.theta_1_e))*(config.rho_t*config.rho_r)*(config.v**2)*(config.l**2))))) + config.n_i

def calc_ber_with_snr(snr):
    return Q(np.sqrt(snr / 2))

def calc_C_with_snr(snr):
    return config.B * np.log2(1 + snr)