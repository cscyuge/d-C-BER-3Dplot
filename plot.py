import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
from config import *
from functions import *
import config
import time
from utils import is_key_pressed, is_key_down
# matplotlib.use('QtAgg')
fig = plt.figure(figsize=(10, 8))
plt.ion()
azim = -60
elev = 30


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

def plot3D():
    global elev, azim

    if sample_base == 'd':
        arr_d = np.linspace(d_min, d_max, num_samples)
        arr_BER = [calc_ber_with_snr(D_SNR(d)) for d in arr_d]
        arr_C = [calc_C_with_snr(D_SNR(d)) for d in arr_d]
        arr_snr = [D_SNR(d) for d in arr_d]
    elif sample_base == 'C':
        arr_C = np.linspace(C_min, C_max, num_samples)
        arr_d = [calc_d_with_snr(C_SNR(C)) for C in arr_C]
        arr_BER = [calc_ber_with_snr(C_SNR(C)) for C in arr_C]
        arr_snr = [C_SNR(C) for C in arr_C]
    elif sample_base == 'BER':
        arr_BER = np.linspace(BER_min, BER_max, num_samples)
        arr_d = [calc_d_with_snr(BER_SNR(ber)) for ber in arr_BER]
        arr_C = [calc_C_with_snr(BER_SNR(ber)) for ber in arr_BER]
        arr_snr = [BER_SNR(ber) for ber in arr_BER]
    elif sample_base == 'SNR':
        arr_snr = np.linspace(SNR_min, SRN_max, num_samples)
        arr_d = [calc_d_with_snr(snr) for snr in arr_snr]
        arr_BER = [calc_ber_with_snr(snr) for snr in arr_snr]
        arr_C = [calc_C_with_snr(snr) for snr in arr_snr]
    
    plt.clf()
    ax = fig.gca(projection='3d')
    ax.view_init(elev, azim)
    ax.set_xlabel('d')
    ax.set_ylabel('BER')
    ax.set_zlabel('C')
    colors = color_map(arr_snr, 'jet')
    ax.set_xlim(np.min(arr_d)-0.1, np.max(arr_d)+0.1)
    ax.set_ylim(np.min(arr_BER)-0.1, np.max(arr_BER)+0.1)
    ax.set_zlim(np.min(arr_C)-0.1, np.max(arr_C)+0.1)

    for i in range(len(arr_d)-1):
        ax.plot([arr_d[i], arr_d[i+1]], [arr_BER[i], arr_BER[i+1]], [arr_C[i], arr_C[i+1]], color=colors[i])  
        # plt.pause(0.001) 
    elev, azim = ax.elev, ax.azim
    fig.colorbar(matplotlib.cm.ScalarMappable(cmap='jet', norm = matplotlib.colors.Normalize(vmin=min(arr_snr), vmax=max(arr_snr))), ax=ax)
    plt.ioff()
    # fig.savefig('d-BER-C-SNR.png', dpi=300)
    # plt.show()

def main():
    
    plot3D()
    # while True:
    #     time.sleep(1)
    #     # pressed_key = False
    #     # if is_key_pressed('d'):
    #     #     config.d_min += 0.1
    #     #     pressed_key = True
    #     # if pressed_key:
    #     #     plot3D()
    plt.show()
    

if __name__ == '__main__':
    main()
