"""
모델 학습 및 평가를 위한 유틸리티
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
import time


class Trainer:
    """모델 학습 및 평가를 관리하는 클래스"""

    def __init__(self, model, device, criterion=None, optimizer=None):
        self.model = model.to(device)
        self.device = device
        self.criterion = criterion or nn.CrossEntropyLoss()
        self.optimizer = optimizer
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': []
        }

    def train_epoch(self, train_loader):
        """한 에폭 학습"""
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        pbar = tqdm(train_loader, desc='Training')
        for batch_idx, (data, target) in enumerate(pbar):
            data, target = data.to(self.device), target.to(self.device)

            # Forward pass
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)

            # Backward pass
            loss.backward()
            self.optimizer.step()

            # Statistics
            running_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

            # Update progress bar
            pbar.set_postfix({
                'loss': running_loss / (batch_idx + 1),
                'acc': 100. * correct / total
            })

        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100. * correct / total

        return epoch_loss, epoch_acc

    def validate(self, val_loader):
        """검증 데이터로 모델 평가"""
        self.model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for data, target in tqdm(val_loader, desc='Validation'):
                data, target = data.to(self.device), target.to(self.device)

                output = self.model(data)
                loss = self.criterion(output, target)

                running_loss += loss.item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()

        epoch_loss = running_loss / len(val_loader)
        epoch_acc = 100. * correct / total

        return epoch_loss, epoch_acc

    def fit(self, train_loader, val_loader, epochs, save_path=None):
        """모델 학습"""
        print(f"학습 시작 - Device: {self.device}")
        print(f"총 에폭: {epochs}")
        print("-" * 60)

        best_val_acc = 0.0

        for epoch in range(epochs):
            start_time = time.time()

            # Train
            train_loss, train_acc = self.train_epoch(train_loader)

            # Validate
            val_loss, val_acc = self.validate(val_loader)

            # Save history
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)

            epoch_time = time.time() - start_time

            # Print epoch results
            print(f"\nEpoch {epoch + 1}/{epochs} - {epoch_time:.2f}s")
            print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
            print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")

            # Save best model
            if save_path and val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save({
                    'epoch': epoch,
                    'model_state_dict': self.model.state_dict(),
                    'optimizer_state_dict': self.optimizer.state_dict(),
                    'val_acc': val_acc,
                }, save_path)
                print(f"모델 저장됨: {save_path} (Val Acc: {val_acc:.2f}%)")

            print("-" * 60)

        print(f"학습 완료! 최고 검증 정확도: {best_val_acc:.2f}%")

        return self.history
