import json
import matplotlib.pyplot as plt

with open('properness_probs.json') as data_file:    
    data = json.load(data_file)
    x = []
    y = []
    for point in data['data']:
        x.append(point['givens'])
        y.append(point['prob'])


with open('conflicts.json') as conflicts_file:
    c_y = json.load(conflicts_file)['data']


fig, ax1 = plt.subplots()
blue_line = ax1.plot(x, y, label='fish', color='blueviolet')
ax1.set_ylim([-0.1, 1.10])
ax1.set_ylabel('Average Properness')

ax2 = ax1.twinx()
green_line = ax2.plot(x, c_y, label='chicken', color='black')
ax2.set_ylim([-2, 27])
ax2.set_ylabel('Amount of Conflicts')


plt.xlabel('Amount of Givens')


fig.legend((blue_line), ('Average of Properness',), loc=(0.2, 0.8))
fig.legend((green_line), ('Amount of Conflicts',), loc=(0.2, 0.9))

# axes.set_ylim([-0.1, 1.10])

fig.tight_layout()
plt.savefig('properness_conflicts.png')
plt.show()