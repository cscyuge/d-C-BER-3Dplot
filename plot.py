import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
import config
from functions import calc_ber_with_snr, calc_C_with_snr, calc_d_with_snr, D_SNR, C_SNR, BER_SNR
import time
from matplotlib.widgets import TextBox
from utils import is_key_pressed, is_key_down
# matplotlib.use('QtAgg')
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
cb = fig.colorbar(matplotlib.cm.ScalarMappable(cmap='jet', norm = matplotlib.colors.Normalize(vmin=0, vmax=1)), ax=ax)
azim = -60
elev = 30

arr_d, arr_BER, arr_C, arr_snr, colors = [], [], [], [], []
lines = []


def color_map(data, cmap):    
    dmin, dmax = np.nanmin(data), np.nanmax(data)
    cmo = plt.cm.get_cmap(cmap)
    cs, k = list(), 256/cmo.N
    
    for i in range(cmo.N):
        c = cmo(i)
        for j in range(int(i*k), int((i+1)*k)):
            cs.append(c)
    cs = np.array(cs)
    data = np.uint8(255*(data-dmin)/(dmax-dmin))
    return cs[data]


def get_data():
    global arr_d, arr_BER, arr_C, arr_snr, colors
    if config.sample_base == 'd':
        arr_d = np.linspace(config.d_min, config.d_max, config.num_samples)
        arr_BER = [calc_ber_with_snr(D_SNR(d)) for d in arr_d]
        arr_C = [calc_C_with_snr(D_SNR(d)) for d in arr_d]
        arr_snr = [D_SNR(d) for d in arr_d]
    elif config.sample_base == 'C':
        arr_C = np.linspace(config.C_min, config.C_max, config.num_samples)
        arr_d = [calc_d_with_snr(C_SNR(C)) for C in arr_C]
        arr_BER = [calc_ber_with_snr(C_SNR(C)) for C in arr_C]
        arr_snr = [C_SNR(C) for C in arr_C]
    elif config.sample_base == 'BER':
        arr_BER = np.linspace(config.BER_min, config.BER_max, config.num_samples)
        arr_d = [calc_d_with_snr(BER_SNR(ber)) for ber in arr_BER]
        arr_C = [calc_C_with_snr(BER_SNR(ber)) for ber in arr_BER]
        arr_snr = [BER_SNR(ber) for ber in arr_BER]
    elif config.sample_base == 'SNR':
        arr_snr = np.linspace(config.SNR_min, config.SRN_max, config.num_samples)
        arr_d = [calc_d_with_snr(snr) for snr in arr_snr]
        arr_BER = [calc_ber_with_snr(snr) for snr in arr_snr]
        arr_C = [calc_C_with_snr(snr) for snr in arr_snr]
    
    colors = color_map(arr_snr, 'jet')
    

def update_attr(attr, value):
    if attr == 'num_samples': value = int(value)
    elif attr!='sample_base': value = float(value)
    setattr(config, attr, value)
    print(attr, value, getattr(config, attr))
    get_data()
    ax.set_xlim(np.min(arr_d)-0.1, np.max(arr_d)+0.1)
    ax.set_ylim(np.min(arr_BER)-0.1, np.max(arr_BER)+0.1)
    ax.set_zlim(np.min(arr_C)-0.1, np.max(arr_C)+0.1)
    plot3D()

def plot3D():
    global cb
    for i,l in enumerate(lines):
        l.set_data_3d(([arr_d[i], arr_d[i+1]], [arr_BER[i], arr_BER[i+1]], [arr_C[i], arr_C[i+1]]))
        l.set(color=colors[i])
    cb.update_normal(matplotlib.cm.ScalarMappable(cmap='jet', norm = matplotlib.colors.Normalize(vmin=min(arr_snr), vmax=max(arr_snr))))
    ax.relim()
    ax.autoscale_view()
    plt.draw()

# todo: use lambda will cause duplicate func bug, don't know why
def update_d_min(value): update_attr('d_min', value)
def update_d_max(value): update_attr('d_max', value)
def update_P_r(value): update_attr('P_r', value)
def update_B(value): update_attr('B', value)
def update_k(value): update_attr('k', value)
def update_rho_t(value): update_attr('rho_t', value)
def update_rho_r(value): update_attr('rho_r', value)
def update_theta_1_e(value): update_attr('theta_1_e', value)
def update_theta_i(value): update_attr('theta_i', value)
def update_sigma_i(value): update_attr('sigma_i', value)
def update_sigma_n(value): update_attr('sigma_n', value)
def update_r(value): update_attr('r', value)
def update_v(value): update_attr('v', value)
def update_l(value): update_attr('l', value)
def update_n_i(value): update_attr('n_i', value)
def update_num_samples(value): update_attr('num_samples', value)
def update_sample_base(value): update_attr('sample_base', value)
def update_C_min(value): update_attr('C_min', value)
def update_C_max(value): update_attr('C_max', value)
def update_BER_min(value): update_attr('BER_min', value)
def update_BER_max(value): update_attr('BER_max', value)
def update_SNR_min(value): update_attr('SNR_min', value)
def update_SNR_max(value): update_attr('SRN_max', value)

def main():
    ax.set_xlabel('d')
    ax.set_ylabel('BER')
    ax.set_zlabel('C')
    get_data()
    ax.set_xlim(np.min(arr_d)-0.1, np.max(arr_d)+0.1)
    ax.set_ylim(np.min(arr_BER)-0.1, np.max(arr_BER)+0.1)
    ax.set_zlim(np.min(arr_C)-0.1, np.max(arr_C)+0.1)
    for i in range(len(arr_d)-1):
        l, = ax.plot([arr_d[i], arr_d[i+1]], [arr_BER[i], arr_BER[i+1]], [arr_C[i], arr_C[i+1]], color=colors[i])
        lines.append(l)    
    
    axboxes = []
    text_boxes = []
    param2func = {
        'P_r': update_P_r,
        'B': update_B,
        'k': update_k,
        'rho_t': update_rho_t,
        'rho_r': update_rho_r,
        'theta_1_e': update_theta_1_e,
        'theta_i': update_theta_i,
        'sigma_i': update_sigma_i,
        'sigma_n': update_sigma_n,
        'r': update_r,
        'v': update_v,
        'l': update_l,
        # 'n_i': update_n_i,
        'num_samples': update_num_samples,
        # 'sample_base': update_sample_base,
        # 'C_min': update_C_min,
        # 'C_max': update_C_max,
        # 'BER_min': update_BER_min,
        # 'BER_max': update_BER_max,
        # 'SNR_min': update_SNR_min,
        # 'SRN_max': update_SNR_max,
        # 'd_min': update_d_min,
        # 'd_max': update_d_max,
    }
    if config.sample_base == 'd':
        param2func['d_min'] = update_d_min
        param2func['d_max'] = update_d_max
    elif config.sample_base == 'C':
        param2func['C_min'] = update_C_min
        param2func['C_max'] = update_C_max
    elif config.sample_base == 'BER':
        param2func['BER_min'] = update_BER_min
        param2func['BER_max'] = update_BER_max
    elif config.sample_base == 'SNR':
        param2func['SNR_min'] = update_SNR_min
        param2func['SRN_max'] = update_SNR_max
    
    for i, param in enumerate(param2func.keys()):
        axboxes.append(fig.add_axes([0.1, 0.9-0.03*i, 0.04, 0.02]))
        text_boxes.append(TextBox(axboxes[i], param, textalignment="center"))
        text_boxes[i].on_submit(param2func[param])
        text_boxes[i].set_val(getattr(config, param))
    plt.show()

if __name__ == '__main__':
    main()
