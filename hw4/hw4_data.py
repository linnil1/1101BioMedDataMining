import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from keras.datasets import cifar10
from PIL import Image


class Data_cifar10(Dataset):
    def __init__(self, x, y, transform=None):
        self.x = x
        self.y = torch.LongTensor(y)
        self.transform = transform

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        image, label = Image.fromarray(self.x[idx]), self.y[idx]
        if self.transform:
            image = self.transform(image)
        return image, label


def get_data(transform_train, transform_test, batch_size=100):
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    # challenge: use 10000 samples for training
    x_train = x_train[:10000]
    y_train = y_train[:10000]

    data_train = Data_cifar10(x_train, y_train, transform=transform_train)
    data_test  = Data_cifar10(x_test,  y_test,  transform=transform_test)
    dataloader_train = DataLoader(data_train, batch_size=batch_size,
                                  shuffle=True, num_workers=12)
    dataloader_test  = DataLoader(data_test,  batch_size=batch_size,
                                  shuffle=True, num_workers=12)
    return dataloader_train, dataloader_test
