import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import itertools
from hw4 import model, dataloader_test, device
from sklearn.metrics import (
        f1_score, accuracy_score, recall_score, precision_score)


def plot_confusion_matrix(cm):
    # cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.title("Confusion matrix")
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.colorbar()
    classes = list(range(len(cm)))
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    # fmt = '.2f'
    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 verticalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def runModel(name):
    checkpoint = torch.load(f'{name}.pth')
    model.load_state_dict(checkpoint['net'])

    labels = []
    predit = []
    with torch.no_grad():
        model.eval()
        for step, (img, label) in enumerate(dataloader_test):
            img = img.to(device)
            label_pred = model(img)
            labels.extend(label.flatten().numpy())
            predit.extend(torch.argmax(label_pred, axis=1).cpu().numpy())
    return predit, labels


def createMatrix(predit, labels):
    classes = 10
    cm = np.zeros([classes, classes], dtype=np.int)
    for a, b in zip(predit, labels):
        cm[a, b] += 1
    return cm


if __name__ == "__main__":
    name = sys.argv[1]

    predit, labels = runModel(name)
    print("Acc      ", accuracy_score(labels, predit))
    print("Precision", precision_score(labels, predit, average='macro'))
    print("Recall   ", recall_score(labels, predit, average='macro'))
    print("F1       ", f1_score(labels, predit, average='macro'))

    cm = createMatrix(predit, labels)
    print(cm)
    plot_confusion_matrix(cm)
    plt.savefig(f"{name}.confusion_matrix.png")
