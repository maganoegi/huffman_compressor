# ------------------------------------------------------------------ #
# ------------ Huffman Compressor Application ---------------------- #
# ------------ HEPIA 2018-2019 ITI 1 ------------------------------- #
# ------------------------------------------------------------------ #
# ---- File Module ----- Sergey PLATONOV & Dylan MPACKO ------------ #
# ------------------------------------------------------------------ #

# ------------------------------ Assets ---------------------------- #
import sys
import json
import time
import hashlib
import argparse
import os
from prettytable import PrettyTable

# ----------------------- Function Definitions --------------------- #
def read_user_input():
    filenames = []
    args = sys.argv
    if len(args) == 4:
        filenames.append(args[1])
        filenames.append(args[2])
        filenames.append(args[3])
        return filenames
    else:
        raise Exception('Please provide the name of the Input and Output files! (2 arguments)')

def bytes_2_array(filename): # -> bytearray()
    output_array = []
    with open(filename, "rb") as f:
        byte = f.read(1).hex()
        output_array.append(byte)
        while byte:
            byte = f.read(1)
            if not byte:
                break
            i = byte.hex()
            output_array.append(i)
    f.close()
    return output_array


def translate(vals, dict):
    byte_string = ""
    for i in range(len(vals)):
        byte_string += dict[vals[i]]

    return byte_string

def finalize(byte_string):
    zeros_added = 0
    while len(byte_string) % 8 != 0:
        byte_string += "0"
        zeros_added += 1
    header_str = format(zeros_added, '08b')
    byte_string = header_str + byte_string

    start = 0
    stop = 8
    val_array = []
    while start < len(byte_string):
        sl = slice(start, stop, 1)
        val = int(byte_string[sl], 2)
        start += 8
        stop += 8
        val_array.append(hex(val))

    return val_array

def write_2_json(dictionary, filename):
    data = {v: k for k, v in dictionary.items()}
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()

def write_2_binary(byte_array, filename):
    x = bytes([int(x, 0) for x in byte_array])
    #x += b''
    f = open(filename, "wb")
    f.write(x)
    f.close()

def update_bar(pbar, processname):
    time.sleep(0.1)
    pbar.update(1)
    pbar.set_description(processname, refresh=True)


def hashOriginal(filename):
    with open(filename, "rb") as f:
        byte = f.read()
        m = hashlib.sha256(byte).hexdigest()
    f.close()
    return m

def compressor_display(freq_dict, compressed_list, file_2_read, file_2_write, byte_array, HashVal):
    print("\n")
    _green_bold = "\033[92m\033[1m"
    _yellow_bold = "\033[93m"
    _red_bold = "\033[91m\033[1m"
    _blue_bold = "\033[94m\033[1m"
    _end = "\033[0m"
    _color = ""
    j = 0
    k = 0
    tmp0 = ""
    tmp1 = ""
    tmp2 = ""
    tmp3 = ""
    tmp4 = ""

    for i in compressed_list.keys():
        if k < (len(compressed_list) - 4):
            if j == 0:
                tmp0 = i
                j += 1
            elif j == 1:
                tmp1 = i
                j += 1
            elif j == 2:
                tmp2 = i
                j += 1
            elif j == 3:
                tmp3 = i
                j += 1
            elif j == 4:
                tmp4 = i
                j += 1
            else:
                print((_green_bold + "{0:3}" + _red_bold + "{1:20}" +
                 _green_bold + "{2:3}" + _red_bold + "{3:20}" +
                 _green_bold + "{4:3}" + _red_bold + "{5:20}" +
                 _green_bold + "{6:3}" + _red_bold + "{7:20}" +
                 _green_bold + "{8:3}" + _red_bold + "{9:20}" + _end).format(tmp0, compressed_list[tmp0],
                                                                           tmp1, compressed_list[tmp1],
                                                                           tmp2, compressed_list[tmp2],
                                                                           tmp3, compressed_list[tmp3],
                                                                           tmp4, compressed_list[tmp4]))

                j = 0
            k += 1
        else:
            print(_green_bold + i, _red_bold + compressed_list[i] + _end)

    file_path_original = './' + file_2_read
    size_before = os.path.getsize(file_path_original)
    size_after = os.path.getsize(file_2_write) + os.path.getsize('./dict.json')
    rate = 100.0 - ((float(size_after) / float(size_before)) * 100.0)

    if rate <= 0.0:
        _color = _red_bold
    elif (rate > 0.0) & (rate < 20.0):
        _color = _yellow_bold
    else:
        _color = _green_bold
    arrow = '\u2192'

    avg = 0.0
    for x in freq_dict.keys():
        avg += (freq_dict[x] / len(byte_array)) * len(compressed_list[x])

    print('\nCompressed: ', file_2_read, arrow, file_2_write + ' dict.json')
    print('Compression Stats: ', size_before, 'bytes', arrow, size_after, 'bytes, ', "%.3f" % avg, "bits / symbol")
    print('Compression Rate:  ', _color + "%.3f" % rate, '%\n' + _end)
    print('\nFile Hash:  ', _blue_bold + HashVal + _end)
    print("\n")
    print("PS: please specify the file extension in the code of the decompressor when decompressing!\n")

def hepia_print():
    line = [""] * 14
    line[0] = "MMMMMMMMMMMMMMMMMMMMMMWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWWWMMMMMMMMMMMMMMMMMMMMMMMMMMM"
    line[1] = "MMMMMMMMMMMMMMMMMMMMMO:;OMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWx,;OMMMMMMMMMMMMMMMMMMMMMMMMMM"
    line[2] = "MMMMMMMMMMMMMMMMMMMMMd  oX00XWMMMMMMMMMMMMMWK0O0NMMMMMMMMMMMMMNKXNKO0NMMMMMMMMMMMMWkcl0MMMMMMMMMMMWN0OOKNMMMMMMMM"
    line[3] = "MMMMMMMMMMMMMMMMMMMMMd  ';...xWMMMMMMMMMMM0:.',.'xNMMMMMMMMMMWd..,;..,OWMMMMMMMMMMWo.'kMMMMMMMMMMNd'.,'.,kWMMMMMM"
    line[4] = "MMMMMMMMMMMMMMMMMMMMMd  cKd. ;XMMMMMMMMMMX; .xO; .OMMMMMMMMMMWl  cKx. :XMMMMMMMMMMWl .xMMMMMMMMMMXd:d0o. :NMMMMMM"
    line[5] = "MMMMMMMMMMMMMMMMMMMMMd  oMO. ;XMMMMMMMMMM0' .;c;':0MMMMMMMMMMWl  dM0' ,KMMMMMMMMMMWl .xMMMMMMMMMMNkc;:,  :NMMMMMM"
    line[6] = "MMMMMMMMMMMMMMMMMMMMMd  oMO. ;XMMMMMMMMMMK, 'OXxcoXMMMMMMMMMMWl  oWO. ;XMMMMMMMMMMWl .xMMMMMMMMMMk. :Kk. :NMMMMMM"
    line[7] = "MMMMMMMMMMMMMMMMMMMMMd. dMO. :XMMMMMMMMMMWx. ,;..lNMMMMMMMMMMWl  .;. .xWMMMMMMMMMMWl .xMMMMMMMMMMO' .c;. :XMMMMMM"
    line[8] = "MMMMMMMMMMMMMMMMMMMMMXkkXMNOx0WMMMMMMMMMMMWKkddx0WMMMMMMMMMMMWl .lkdxKWMMMMMMMMMMMWKxkXMMMMMMMMMMWKxdx0OxONMMMMMM"
    line[9] = "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWd.'kMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
    line[10] ="MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN..WMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
    line[11] ="MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNXXWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
    line[12] ="\033[91mMMMMMMMMMMMMMMMMMMMMMMMMMMMMM\033[0mMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
    line[13] ="\033[91mMMMMMMMMMMMMMMMMMMMMMMMMMMMMM\033[0mMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n"

    for i in range(len(line)):
        for j in range(len(line[i])):
            if j < (len(line[i])-1):
                print(line[i][0:j], end = "\r")
            else:
                print(line[i][0:j], end = "\n")
        time.sleep(0.01)


