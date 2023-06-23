import matplotlib.pyplot as plt
import json


def only_self_formula(x: float):
    return ((2 ** (x - 1) + 1)**x) / 2**(x**2)


with open('sp_strong/testodds.json') as json_file:
    data_dict = json.load(json_file)


x = [int(key) for key in data_dict.keys()]
y = [float(data_dict[key]) for key in data_dict.keys()]


plt.xlabel("Number of agents")
plt.ylabel("Frequency")
plt.title(r'Frequency that $|N_1(p, j)| - |N_1(p, q)| \leq 2$')


plt.plot(x, y)
plt.ylim(ymin=0)
plt.show()
