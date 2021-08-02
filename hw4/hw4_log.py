import sys
import re
import numpy as np
import matplotlib.pyplot as plt

# read data
data = []
name = sys.argv[1]
for i in open(f"{name}"):
    d = re.findall(r"(\d+).*?([0-9.]+).*?([0-9.]+)", i)
    if len(d) > 1:
        data.append([float(i) for i in d[0] + d[1]])
data = np.array(data).T

# plot
plt.subplot(1, 2, 1)
plt.title("loss")
plt.plot(data[0], data[1], label="train")
plt.plot(data[0], data[4], label="valid")
plt.legend()
plt.xlabel("epoch")
plt.ylabel("loss")

plt.subplot(1, 2, 2)
plt.title("Accuracy")
plt.plot(data[0], data[2], label="train")
plt.plot(data[0], data[5], label="valid")
plt.xlabel("epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.savefig(f"{name}.png")
plt.show()
