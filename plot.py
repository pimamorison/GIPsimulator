import matplotlib.pyplot as plt
import json


def only_self_formula(x: float):
    return ((2 ** (x - 1) + 1)**x) / 2**(x**2)


with open('data/inductive_consensus.json') as json_file:
    data_dict = json.load(json_file)

with open('data/most_popular.json') as json_file:
    data_dict2 = json.load(json_file)


x = [int(key) for key in data_dict.keys()]
y = [float(data_dict[key]) for key in data_dict.keys()]

x2 = [int(key) for key in data_dict2.keys()]
y2 = [float(data_dict2[key]) for key in data_dict2.keys()]

plt.title("Frequency of strategic manipulation")
plt.xlabel("Number of agents")
plt.ylabel("Frequency")

# plt.plot(x, [1 - only_self_formula(arg)
#              for arg in x], linestyle='--', dashes=(5, 5), color='r')
#plt.plot(x2, y2, label="Frequency max-secondmax < 2")
plt.plot(x, y, label="Frequency of strategic manipulation")
plt.ylim(ymin=0)
plt.legend()
plt.show()
