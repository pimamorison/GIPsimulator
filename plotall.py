import matplotlib.pyplot as plt
import json
import numpy as np


def only_self_formula(x: float):
    return ((2 ** (x - 1) + 1)**x) / 2**(x**2)


dir = "sp_weak/"
cif = "most_popular"


# with open('data/' + cif + '.json') as json_file:
with open(dir + cif + '.json') as json_file:
    data_dict = json.load(json_file)

# with open('data2/' + cif + '_hamming.json') as json_file:
with open(dir + cif + '_hamming.json') as json_file:
    data_dict2 = json.load(json_file)

with open(dir + cif + '_inter.json') as json_file:
    data_dict3 = json.load(json_file)

with open(dir + cif + '_inver.json') as json_file:
    data_dict4 = json.load(json_file)


x = [int(key) for key in data_dict.keys()]
y = [float(data_dict[key]) for key in data_dict.keys()]

x2 = [int(key) for key in data_dict2.keys()]
y2 = [float(data_dict2[key]) for key in data_dict2.keys()]

x3 = [int(key) for key in data_dict3.keys()]
y3 = [float(data_dict3[key]) for key in data_dict3.keys()]

x4 = [int(key) for key in data_dict4.keys()]
y4 = [float(data_dict4[key]) for key in data_dict4.keys()]


plt.xlabel("Number of agents")
plt.ylabel("Frequency")

plt.plot(x, y, label="Separable preference")
plt.plot(x2, y2, label="Hamming preference")
plt.plot(x3, y3, label="Int+ preference")
plt.plot(x4, y4,
         label="Int- preference")


# plt.plot(x, [1 - only_self_formula(arg)
#              for arg in x], color='r',
#          label=r'$1 -\frac{(2^{n-1}+1)^n}{2^{n^2}}$')


plt.title("Frequency of manipulation for the MPA rule")
# plt.ylim(ymin=0)
plt.legend()
plt.show()
