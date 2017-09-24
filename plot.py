import json
import matplotlib.pyplot as plt

with open('properness_probs.json') as data_file:    
    data = json.load(data_file)
    x = []
    y = []
    for point in data['data']:
        x.append(point['givens'])
        y.append(point['prob'])

plt.plot(x, y)
plt.show()