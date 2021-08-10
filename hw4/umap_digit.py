# pip3 install umap-learn[plot]
import numpy as np
import pandas as pd

# setup plot
# import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12, 9)

# read data
from sklearn.datasets import load_digits
digits = load_digits()
fig, ax_array = plt.subplots(20, 20)
axes = ax_array.flatten()
for i, ax in enumerate(axes):
    ax.imshow(digits.images[i], cmap='gray_r')
    plt.setp(axes, xticks=[], yticks=[], frame_on=False)
    plt.tight_layout(h_pad=0.5, w_pad=0.01)
plt.show()


def scatterPlot(x, y, label):
    plt.scatter(x, y, c=label, cmap='Spectral', s=5)
    plt.gca().set_aspect('equal', 'datalim')
    plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))


def evaluateCluster(predict, target):
    from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score
    print("  ARI", adjusted_rand_score(target, predict))
    print("  AMI", adjusted_mutual_info_score(target, predict))


# PCA
## PCA transform
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(digits.data)
print("PCA explain variance", pca.explained_variance_ratio_)
pca_embedding = pca.transform(digits.data)

## PCA plot
plt.title("Label on PCA")
scatterPlot(pca_embedding[:, 0], pca_embedding[:, 1], digits.target)
plt.show()

# UMAP
import umap
umap_embedding = umap.UMAP(n_components=2).fit_transform(digits.data)
plt.title("Label on UMAP")
scatterPlot(umap_embedding[:, 0], umap_embedding[:, 1], digits.target)
plt.show()

# Cluster by kmean
import sklearn.cluster as cluster
kmean_labels = cluster.KMeans(n_clusters=10).fit_predict(digits.data)
print("kmeans")
evaluateCluster(kmean_labels, digits.target)

plt.title("kmeans Label on UMAP")
scatterPlot(umap_embedding[:, 0], umap_embedding[:, 1], kmean_labels)
plt.show()

# Cluster by kmean on umap bedding
kmean_umap_data = umap.UMAP(n_components=2).fit_transform(digits.data)
kmean_umap_labels = cluster.KMeans(n_clusters=10).fit_predict(kmean_umap_data)
print(f"K-means on umap")
evaluateCluster(kmean_umap_labels, digits.target)

plt.title("kmeans after UMAP")
scatterPlot(umap_embedding[:, 0], umap_embedding[:, 1], kmean_umap_labels)
plt.show()

## More components for umap
for component in range(1, 4):
    kmean_umap_data = umap.UMAP(n_components=component).fit_transform(digits.data)
    kmean_umap_labels = cluster.KMeans(n_clusters=10).fit_predict(kmean_umap_data)
    print(f"K-means on umap(component={component})")
    evaluateCluster(kmean_umap_labels, digits.target)
