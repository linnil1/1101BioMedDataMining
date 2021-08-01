# pip3 install keras tensorflow torch torchvision tqdm matplotlib scikit-learn
import os
import time
import torch
from torch import nn, optim
from torchvision import transforms
from tqdm import tqdm
from hw4_data import get_data
from hw4_model import DarkNet53


epoches = 200
batch_size = 50

# change this to resume
name = str(time.time())
# name = "1627714346.7687738"
# name = "1627797842.914972"

# from torchvision.models import *
# from hw4_other import LabelSmoothingLoss, DenseNet121, densenet_cifar
# 32, (6, 12, 24, 16), 64,
# model = densenet121(pretrained=False, num_classes=10, drop_rate=0.1)
# 32, (6, 12, 48, 32), 64
# model = densenet201(pretrained=False, num_classes=10, drop_rate=0.1)
# model = DenseNet121()
# model = densenet_cifar()
model = DarkNet53()


transform_my = transforms.Compose([
    transforms.ColorJitter(0.4, 0.4, 0.4),
    # transforms.RandomRotation(10),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.5),
    #  transforms.RandomCrop(30),
    transforms.ToTensor(),
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

transform_train = transforms.Compose([
    transforms.ColorJitter(0.32, 0.32, 0.32),
    # transforms.RandomAffine(16, (0.16, 0.16), (0.84, 1.16), 0.2),
    # transforms.RandomAffine(0, translate=(0.16, 0.16)),
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transform_test,
])

transform_train_my = transforms.Compose([
    transforms.AutoAugment(transforms.AutoAugmentPolicy.CIFAR10),
    transform_test,
])

dataloader_train, dataloader_test = \
        get_data(transform_train, transform_test, batch_size=batch_size)


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# loss_func = LabelSmoothingLoss(10, 0.1)
loss_func = nn.CrossEntropyLoss()
# opt = optim.Adam(model.parameters(), lr=0.001)
model = model.to(device)

# init training parameters
if os.path.exists(f"{name}.pth"):
    checkpoint = torch.load(f'{name}.pth')
    model.load_state_dict(checkpoint['net'])
    best_acc = checkpoint['acc']
    start_epoch = checkpoint['epoch']
    opt = optim.SGD(model.parameters(), lr=0.01)
else:
    start_epoch = 0
    best_acc = 0
    opt = optim.SGD(model.parameters(), lr=0.1)

scheduler = optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epoches)


if __name__ == "__main__":
    print(f"Start training {name}")
    for epoch in range(start_epoch, start_epoch + epoches):
        running_loss = 0.0
        acc = 0
        tot = 0
        bar_train = tqdm(dataloader_train, leave=False)
        model.train()
        for step, (img, label) in enumerate(bar_train):
            img = img.to(device)
            label = label.to(device)
            opt.zero_grad()
            label_pred = model(img)
            loss = loss_func(label_pred, label.flatten())
            loss.backward()
            opt.step()

            with torch.no_grad():
                tot += len(img)
                acc += (torch.argmax(label_pred, axis=1)
                        == label.flatten()).sum()
                running_loss += loss.item()
                if (step + 1) % 1 == 0:
                    bar_train.set_description(
                            f"train_loss: {running_loss * 1000 / tot:.3f} "
                            f"train_acc:  {acc/tot:.3f}")
        scheduler.step()
        print(f"[{epoch:2d}] train_loss: {running_loss * 1000 / tot:6.3f} "
              f"train_acc: {acc/tot:.3f}", end="\t")

        # evaluation
        model.eval()
        with torch.no_grad():
            tot = 0
            acc = 0
            running_loss = 0.0

            for step, (img, label) in enumerate(dataloader_test):
                img = img.to(device)
                label = label.to(device)
                label_pred = model(img)
                running_loss += loss_func(label_pred, label.flatten())
                tot += len(img)
                acc += (torch.argmax(label_pred, axis=1)
                        == label.flatten()).sum()

            save = " Save!" if acc > best_acc else ""
            print(f"[{epoch:2d}] valid_loss: {running_loss * 1000 /tot:6.3f} "
                  f"valid_acc: {acc/tot:.3f} \t {save}")

            if acc > best_acc:
                best_acc = acc
                state = {
                    'net': model.state_dict(),
                    'acc': acc,
                    'epoch': epoch,
                }
                torch.save(state, f'./{name}.pth')

    print('Finished')
