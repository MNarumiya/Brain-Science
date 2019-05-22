import numpy as np
from scipy.io import wavfile

import matplotlib.pyplot as plt


def continuous_listening_effect(seconds=1.0, rate = 44100, noize_index=None, seconds_noize = 1/50, noize=None):
    frequency = 440  # 生成するサイン波の周波数

    if noize_index == None:
        noize_index = np.random.randint(rate)

    if noize == None:
        noize = create_white_noize(seconds)

    rate_number_noize = int(rate * seconds_noize) # ノイズを入れるレート数(リストでの幅)

    surplus_rate = rate_number_noize + noize_index - rate

    if surplus_rate <= 0:
        index_np_list = np.array([])
        for i in range(int(seconds)):
            index_np_list = np.concatenate([index_np_list, np.ones(noize_index)], 0)
            index_np_list = np.concatenate([index_np_list, np.zeros(rate_number_noize)], 0)
            index_np_list = np.concatenate([index_np_list, np.ones(-surplus_rate)], 0)
    else:
        index_np_list = np.ones(noize_index)
        index_np_list = np.concatenate([index_np_list, np.zeros(rate - noize_index)], 0)
        for i in range(int(seconds)-1):
            index_np_list = np.concatenate([index_np_list, np.zeros(surplus_rate)], 0)
            index_np_list = np.concatenate([index_np_list, np.ones(rate - noize_index - surplus_rate) ], 0)
            index_np_list = np.concatenate([index_np_list, np.zeros(rate - noize_index)], 0)

    phases = np.cumsum(2.0 * np.pi * frequency / rate * index_np_list)

    wave = np.sin(phases)

    # 16bit の wav ファイルに書き出す
    wave_16bit = (wave * float(2 ** 15 - 1)).astype(np.int16)  # 値域を 16bit にする
    wavfile.write("sin_and_none.wav", rate, wave_16bit)

    wave += noize * ( 1 - index_np_list) # 無音のとこをノイズで差し替え

    # 16bit の wav ファイルに書き出す
    wave_16bit = (wave * float(2 ** 15 - 1)).astype(np.int16)  # 値域を 16bit にする
    wavfile.write("sin_and_noize.wav", rate, wave_16bit)

def create_white_noize(seconds = 1.0): # seconds : 生成する音の秒数
    frequency = 440  # 生成するサイン波の周波数
    rate = 44100     # 出力する wav ファイルのサンプリング周波数

    # x1 = np.linspace(0, seconds, rate*seconds)
    # A = 1.0
    #
    # wave = np.random.rand(int(rate * seconds))-A
    #
    # # 16bit の wav ファイルに書き出す
    # wave = (wave * float(2 ** 15 - 1)).astype(np.int16)  # 値域を 16bit にする
    # wavfile.write("whitenoize1.wav", rate, wave)

    return np.array([np.random.random()*2.0 - 1.0 for i in range(int(rate * seconds))])


if __name__ == '__main__':
    rate = 44100
    continuous_listening_effect(seconds=5.0, rate = 44100, noize_index=np.random.randint(44100), seconds_noize = 1/50, noize=None)
