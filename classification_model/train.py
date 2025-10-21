"""
MNIST 데이터셋을 사용한 분류 모델 학습 스크립트
"""

import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os
import matplotlib.pyplot as plt

from models import CNNClassifier, SimpleMLP
from utils import Trainer


def get_data_loaders(batch_size=64, data_dir='./data'):
    """MNIST 데이터셋 로드"""

    # 데이터 전처리
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # MNIST 평균, 표준편차
    ])

    # 학습 데이터
    train_dataset = datasets.MNIST(
        root=data_dir,
        train=True,
        download=True,
        transform=transform
    )

    # 테스트 데이터
    test_dataset = datasets.MNIST(
        root=data_dir,
        train=False,
        download=True,
        transform=transform
    )

    # 데이터 로더
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2
    )

    return train_loader, test_loader


def plot_history(history, save_path='training_history.png'):
    """학습 히스토리 시각화"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Loss plot
    ax1.plot(history['train_loss'], label='Train Loss')
    ax1.plot(history['val_loss'], label='Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.legend()
    ax1.grid(True)

    # Accuracy plot
    ax2.plot(history['train_acc'], label='Train Accuracy')
    ax2.plot(history['val_acc'], label='Validation Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Training and Validation Accuracy')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(save_path)
    print(f"학습 히스토리 그래프 저장됨: {save_path}")


def main(args):
    # Device 설정
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"사용 디바이스: {device}")

    # 데이터 로더
    print("데이터셋 로딩 중...")
    train_loader, test_loader = get_data_loaders(
        batch_size=args.batch_size,
        data_dir=args.data_dir
    )
    print(f"학습 데이터: {len(train_loader.dataset)}개")
    print(f"테스트 데이터: {len(test_loader.dataset)}개")

    # 모델 생성
    if args.model == 'cnn':
        model = CNNClassifier(num_classes=10)
        print("모델: CNN Classifier")
    else:
        model = SimpleMLP(num_classes=10)
        print("모델: Simple MLP")

    # 옵티마이저 및 손실 함수
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    # 트레이너 생성
    trainer = Trainer(model, device, criterion, optimizer)

    # 모델 저장 경로
    os.makedirs('checkpoints', exist_ok=True)
    save_path = f'checkpoints/best_{args.model}_model.pth'

    # 학습
    history = trainer.fit(
        train_loader=train_loader,
        val_loader=test_loader,
        epochs=args.epochs,
        save_path=save_path
    )

    # 히스토리 시각화
    plot_history(history, save_path=f'training_history_{args.model}.png')

    print("\n학습 완료!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MNIST 분류 모델 학습')
    parser.add_argument('--model', type=str, default='cnn', choices=['cnn', 'mlp'],
                        help='모델 선택 (cnn 또는 mlp)')
    parser.add_argument('--epochs', type=int, default=10,
                        help='학습 에폭 수 (기본값: 10)')
    parser.add_argument('--batch-size', type=int, default=64,
                        help='배치 크기 (기본값: 64)')
    parser.add_argument('--lr', type=float, default=0.001,
                        help='학습률 (기본값: 0.001)')
    parser.add_argument('--data-dir', type=str, default='./data',
                        help='데이터 저장 경로')

    args = parser.parse_args()
    main(args)
