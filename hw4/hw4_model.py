import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class LabelSmoothingLoss(nn.Module):
    """ https://github.com/pytorch/pytorch/issues/7455 """

    def __init__(self, classes, smoothing=0.0, dim=-1):
        super(LabelSmoothingLoss, self).__init__()
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.cls = classes
        self.dim = dim

    def forward(self, pred, target):
        pred = pred.log_softmax(dim=self.dim)
        with torch.no_grad():
            true_dist = torch.zeros_like(pred)
            true_dist.fill_(self.smoothing / (self.cls - 1))
            true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        return torch.mean(torch.sum(-true_dist * pred, dim=self.dim))


class Residue(nn.Module):
    def __init__(self, channel1, channel2, s):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(channel1, channel2, 1, padding=0, stride=1),
            nn.BatchNorm2d(channel2),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.2),
            nn.Conv2d(channel2,  channel1, 3, padding=1, stride=1),
            nn.BatchNorm2d(channel1),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.2),
        )

    def forward(self, x):
        x = self.cnn(x) + x
        return x


class DarkNet53(nn.Module):
    """
    This model is similiar to darnet53 from YOLO.
    But has less blocks and less channels,
    output classes = 10
    """
    def __init__(self):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1, stride=1),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.1),
            nn.Conv2d(32,  64, 3, padding=1, stride=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.1),

            Residue(64, 32, s=16),
            nn.Conv2d(64,  128, 3, padding=1, stride=2),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.1),
            nn.Dropout(0),

            Residue(128, 64, s=8),
            Residue(128, 64, s=8),
            nn.Conv2d(128,  256, 3, padding=1, stride=2),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.1),

            Residue(256, 128, s=4),
            Residue(256, 128, s=4),
            Residue(256, 128, s=4),
            Residue(256, 128, s=4),
            nn.Conv2d(256,  512, 3, padding=1, stride=2),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.1),

            Residue(512, 256, s=2),
            Residue(512, 256, s=2),
            nn.AvgPool2d(2),
            nn.Dropout(0),

            nn.Flatten(),
            nn.Linear(512 * 1 * 1,  10),
        )

    def forward(self, x):
        x = self.cnn(x)
        return x
