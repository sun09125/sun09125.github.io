"""
학습된 모델을 사용한 추론 스크립트
"""

import argparse
import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from models import CNNClassifier, SimpleMLP


def load_model(model_path, model_type='cnn', device='cpu'):
    """학습된 모델 로드"""
    if model_type == 'cnn':
        model = CNNClassifier(num_classes=10)
    else:
        model = SimpleMLP(num_classes=10)

    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()

    print(f"모델 로드 완료: {model_path}")
    print(f"검증 정확도: {checkpoint['val_acc']:.2f}%")

    return model


def predict_image(model, image_path, device='cpu'):
    """이미지 예측"""
    # 이미지 로드 및 전처리
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    image = Image.open(image_path)
    image_tensor = transform(image).unsqueeze(0).to(device)

    # 예측
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = output.argmax(dim=1).item()
        confidence = probabilities[0][predicted_class].item()

    return predicted_class, confidence, probabilities[0].cpu().numpy()


def visualize_prediction(image_path, predicted_class, confidence, probabilities):
    """예측 결과 시각화"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # 이미지 표시
    img = Image.open(image_path).convert('L')
    ax1.imshow(img, cmap='gray')
    ax1.set_title(f'예측: {predicted_class} (신뢰도: {confidence:.2%})')
    ax1.axis('off')

    # 확률 분포 표시
    classes = list(range(10))
    ax2.bar(classes, probabilities)
    ax2.set_xlabel('클래스')
    ax2.set_ylabel('확률')
    ax2.set_title('클래스별 예측 확률')
    ax2.set_xticks(classes)

    plt.tight_layout()
    plt.savefig('prediction_result.png')
    print("예측 결과 저장됨: prediction_result.png")
    plt.show()


def main(args):
    # Device 설정
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"사용 디바이스: {device}")

    # 모델 로드
    model = load_model(args.model_path, args.model_type, device)

    # 이미지 예측
    predicted_class, confidence, probabilities = predict_image(
        model, args.image_path, device
    )

    print(f"\n예측 결과:")
    print(f"클래스: {predicted_class}")
    print(f"신뢰도: {confidence:.2%}")
    print(f"\n클래스별 확률:")
    for i, prob in enumerate(probabilities):
        print(f"  {i}: {prob:.4f}")

    # 시각화
    if args.visualize:
        visualize_prediction(args.image_path, predicted_class, confidence, probabilities)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='학습된 모델로 이미지 분류')
    parser.add_argument('--model-path', type=str, required=True,
                        help='학습된 모델 체크포인트 경로')
    parser.add_argument('--image-path', type=str, required=True,
                        help='분류할 이미지 경로')
    parser.add_argument('--model-type', type=str, default='cnn', choices=['cnn', 'mlp'],
                        help='모델 타입 (cnn 또는 mlp)')
    parser.add_argument('--visualize', action='store_true',
                        help='예측 결과 시각화')

    args = parser.parse_args()
    main(args)
