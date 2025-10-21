"""
CNN 분류 모델 정의
MNIST 데이터셋을 위한 간단한 Convolutional Neural Network
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class CNNClassifier(nn.Module):
    """
    간단한 CNN 분류 모델

    구조:
    - Conv Layer 1: 1 -> 32 channels, 3x3 kernel
    - Conv Layer 2: 32 -> 64 channels, 3x3 kernel
    - Fully Connected Layer 1: 9216 -> 128
    - Fully Connected Layer 2: 128 -> 10 (출력 클래스 수)
    """

    def __init__(self, num_classes=10):
        super(CNNClassifier, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)

        # Pooling layer
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Dropout for regularization
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)

        # Fully connected layers
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        # Conv layer 1
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool(x)

        # Conv layer 2
        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool(x)
        x = self.dropout1(x)

        # Flatten
        x = x.view(-1, 64 * 7 * 7)

        # Fully connected layers
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)

        return x


class SimpleMLP(nn.Module):
    """
    간단한 Multi-Layer Perceptron 분류 모델
    """

    def __init__(self, input_size=784, hidden_size=256, num_classes=10):
        super(SimpleMLP, self).__init__()

        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 128)
        self.fc3 = nn.Linear(128, num_classes)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        # Flatten input
        x = x.view(x.size(0), -1)

        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc2(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc3(x)

        return x
