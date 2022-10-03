import numpy as np

import collections
import math

# input_DNA_sequence = input('Input Urutan DNA : ')
# #contoh input : ATCGTAGTGAC
# #fixed hasil : 1.9808259362290785
# m = len(input_DNA_sequence)
# bases = collections.Counter([tmp_base for tmp_base in input_DNA_sequence])
#
# shannon_entropy_value = 0
# for base in bases:
#         # number of residues
#         n_i = bases[base]
#         # n_i (# residues type i) / M (# residues in column)
#         p_i = n_i / float(m)
#         entropy_i = p_i * (math.log(p_i, 2))
#         shannon_entropy_value += entropy_i
#
#
#
# print('Estimasi Shanon Entrophy :', shannon_entropy_value * -1)
# s = ['A','B','B','B','B','C','D','D',]
# temp = []
# for i in s :
#     if i == 'A':
#         temp.append('00')
#     elif i == 'B':
#         temp.append('01')
#     elif i == 'C':
#         temp.append('10')
#     elif i == 'D':
#         temp.append('11')
# print('S = ',s)
# s = temp
# print('S = ',s)


# x = [10,10,10,10,10,50,50,50,50,50]
# y = [13,18,16,15,20,86,90,88,88,92]
#
#
# rata_x = np.average(x)
# print(rata_x)
#
# rata_y = np.average(y)
# print(rata_y)
# hasil_b1 = 0
# hasil_x = 0
# hasil_y = 0
# hasil_x2 = 0
# hasill = 0
#
# for i in x:
#     for j in y:
#         hasill = hasill+((i-rata_x)*(j - rata_y))
#
# for k in x:
#     hasil_x2 = hasil_x2 + ((k - rata_x)**2)
#
# print("atas = ", hasill)
# print("bawah = ",hasil_x2)
# hasil_b1 = hasill/hasil_x2
# print("b1 = ", hasil_b1)
#
# print("b0 = ", rata_y-(hasil_b1*rata_x))
#
# print("RSS = ", rata_y-(hasil_b1*rata_x))

def average_len(Soal):
        Sy=[]
        s = ['A', 'B', 'B', 'B', 'B', 'C', 'D', 'D', ]
        for x in s:
                if x == 'A':
                        Sy.append(len(Soal[0]))
                elif x == 'B':
                        Sy.append(len(Soal[1]))
                elif x == 'C':
                        Sy.append(len(Soal[2]))
                elif x == 'D':
                        Sy.append(len(Soal[3]))
                L1 = sum(Sy) / len(Sy)
        return  L1

import numpy as np
Soal1 = ['10','0','1','0']
Soal2 = ['11','0','00','0']
Soal3 = ['00','01','10','11']
Soal4 = ['111','0','110','10']
Soal5 = ['0111','0','110','10']
s = ['A','B','B','B','B','C','D','D',]


print("Average length Soal1: ", average_len(Soal1))
print("Average length Soal2: ", average_len(Soal2))
print("Average length Soal3: ", average_len(Soal3))
print("Average length Soal4: ", average_len(Soal4))
print("Average length Soal5: ", average_len(Soal5))