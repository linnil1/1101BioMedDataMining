# Week4: Clustering and Deep Learning

## Clustering (Lecture)

Using ARI and AMI to Evaluate PCA/UMAP + KMeans Clusering on MNIST 

`umap_digit.py` 

## Deep Learning

Instead of Tensorflow and Keras in the lecture,
I use PyTorch to train a model

### Data

cifar10, first 10000 as training set

### Method

* Darknet-53 
* + Smaller and thinner
* + image argumentation(random crop, color jitter)
* + dropout 0.1
* Cosine annealing SGD lr = 0.1
* batch_size = 16, epoches = 400

Training a new model

``` bash
python3 hw4.py
```

### Result

Download my trainned data https://drive.google.com/file/d/15WD8h9Qm-VL1kYUKlFCL8oNqPNqnuYR-/view?usp=sharing

and Calculate f1 and Confusion Matrix

``` bash
wget "https://drive.google.com/uc?export=download&id=15WD8h9Qm-VL1kYUKlFCL8oNqPNqnuYR-" -O 1627841832.8930326.pth
python3 hw4_log.py 1627841832.8930326.log
python3 hw4_evalute.py 1627841832.8930326
```

Output

``` txt
Acc       0.8555
Precision 0.854274794381158
Recall    0.8554999999999999
F1        0.8546072913161492
[[872   5  39  13  10   3   3   8  30  16]
 [ 11 945   2   2   2   2   1   3  15  41]
 [ 27   2 803  46  45  28  24  11   6   3]
 [  8   2  27 671  28 115  27  20   3   8]
 [ 16   0  37  37 842  23  14  28   1   0]
 [  0   2  35 132  13 780  12  26   2   2]
 [  6   2  37  52  28  20 912   3   3   5]
 [  4   0  14  25  29  25   4 891   2   2]
 [ 43  13   4  10   3   2   2   1 928  12]
 [ 13  29   2  12   0   2   1   9  10 911]]
```

![Confusion Matrix](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw4/1627841832.8930326.confusion_matrix.png)
![Loss and acc](https://raw.githubusercontent.com/linnil1/1101BioMedDataMining/main/hw4/1627841832.8930326.log.png)

### Supplement

I train this model using all training data(50000 images), other parameters remain same.

The accuracy can achieve 0.922
