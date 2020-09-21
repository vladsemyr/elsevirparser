import matplotlib.pyplot as plt
import sys
import io


input_filename = sys.argv[1]

with io.open(input_filename, mode="r", encoding="utf-8") as f:
    plots_data = {}
    lines = f.readlines()
    lines = map(lambda x: x.split(";"), lines)
    for l in lines:
        #пример: PLD;1994;384
        if l[0] not in plots_data:
            # [x...] [y...]
            plots_data[l[0]] = ([], [])
        
        plots_data[l[0]][0].append(int(l[1]))
        plots_data[l[0]][1].append(int(l[2]))

for name, data in plots_data.items():
    plt.close()
    plt.bar(plots_data[name][0], plots_data[name][1])
    plt.title(name)
    plt.savefig(f"images/{name}.png")