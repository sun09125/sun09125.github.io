# 딥러닝 분류 모델 (Deep Learning Classification Model)

PyTorch를 사용한 MNIST 손글씨 숫자 분류 모델 프로젝트입니다.

## 프로젝트 구조

```
classification_model/
├── models/                 # 모델 정의
│   ├── __init__.py
│   └── cnn_classifier.py  # CNN 및 MLP 모델
├── utils/                  # 유틸리티 함수
│   ├── __init__.py
│   └── trainer.py         # 학습/평가 클래스
├── data/                   # 데이터셋 (자동 다운로드)
├── train.py               # 학습 스크립트
├── inference.py           # 추론 스크립트
├── requirements.txt       # 의존성 패키지
└── README.md             # 프로젝트 문서
```

## 주요 기능

1. **두 가지 모델 아키텍처**
   - CNN (Convolutional Neural Network): 이미지 분류에 최적화된 합성곱 신경망
   - MLP (Multi-Layer Perceptron): 간단한 완전연결 신경망

2. **자동 데이터 처리**
   - MNIST 데이터셋 자동 다운로드
   - 데이터 정규화 및 전처리
   - 학습/검증 데이터 분리

3. **학습 모니터링**
   - 에폭별 손실(Loss) 및 정확도(Accuracy) 추적
   - 학습 진행상황 실시간 표시 (tqdm)
   - 학습 히스토리 시각화

4. **모델 저장 및 추론**
   - 최고 성능 모델 자동 저장
   - 저장된 모델로 새로운 이미지 분류
   - 예측 결과 시각화

## 설치 방법

### 1. 의존성 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 필요한 패키지

- Python 3.8 이상
- PyTorch 2.0 이상
- torchvision
- numpy
- matplotlib
- Pillow
- tqdm

## 사용 방법

### 모델 학습

#### CNN 모델 학습 (기본)

```bash
cd classification_model
python train.py --model cnn --epochs 10 --batch-size 64
```

#### MLP 모델 학습

```bash
python train.py --model mlp --epochs 10 --batch-size 64
```

#### 학습 옵션

- `--model`: 모델 선택 (cnn 또는 mlp, 기본값: cnn)
- `--epochs`: 학습 에폭 수 (기본값: 10)
- `--batch-size`: 배치 크기 (기본값: 64)
- `--lr`: 학습률 (기본값: 0.001)
- `--data-dir`: 데이터 저장 경로 (기본값: ./data)

### 모델 추론

학습된 모델로 새로운 이미지를 분류할 수 있습니다.

```bash
python inference.py \
    --model-path checkpoints/best_cnn_model.pth \
    --image-path test_image.png \
    --model-type cnn \
    --visualize
```

#### 추론 옵션

- `--model-path`: 학습된 모델 체크포인트 경로 (필수)
- `--image-path`: 분류할 이미지 경로 (필수)
- `--model-type`: 모델 타입 (cnn 또는 mlp)
- `--visualize`: 예측 결과 시각화 (선택)

## 모델 아키텍처

### CNN Classifier

```
Conv2d (1 -> 32) -> ReLU -> MaxPool
Conv2d (32 -> 64) -> ReLU -> MaxPool -> Dropout(0.25)
Flatten
Linear (3136 -> 128) -> ReLU -> Dropout(0.5)
Linear (128 -> 10)
```

- 입력: 28x28 그레이스케일 이미지
- 출력: 10개 클래스 (0-9 숫자)
- 파라미터: 약 1.2M

### Simple MLP

```
Flatten
Linear (784 -> 256) -> ReLU -> Dropout(0.2)
Linear (256 -> 128) -> ReLU -> Dropout(0.2)
Linear (128 -> 10)
```

- 입력: 28x28 그레이스케일 이미지 (flatten)
- 출력: 10개 클래스 (0-9 숫자)
- 파라미터: 약 235K

## 학습 결과

일반적으로 다음과 같은 성능을 기대할 수 있습니다:

- **CNN 모델**: 검증 정확도 약 99%+ (10 에폭)
- **MLP 모델**: 검증 정확도 약 97-98% (10 에폭)

학습 완료 후 다음 파일들이 생성됩니다:

- `checkpoints/best_cnn_model.pth`: 최고 성능 모델 체크포인트
- `training_history_cnn.png`: 학습 히스토리 그래프

## 예제 코드

### Python에서 모델 사용하기

```python
import torch
from models import CNNClassifier

# 모델 로드
model = CNNClassifier(num_classes=10)
checkpoint = torch.load('checkpoints/best_cnn_model.pth')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# 예측
with torch.no_grad():
    output = model(input_tensor)
    predicted_class = output.argmax(dim=1)
```

## 데이터셋

**MNIST (Modified National Institute of Standards and Technology)**

- 손글씨 숫자 이미지 데이터셋
- 학습 데이터: 60,000개
- 테스트 데이터: 10,000개
- 이미지 크기: 28x28 픽셀 (그레이스케일)
- 클래스: 0-9 (10개)

데이터는 첫 실행 시 자동으로 다운로드됩니다.

## 커스터마이징

### 새로운 모델 추가

`models/cnn_classifier.py`에 새로운 모델 클래스를 추가할 수 있습니다:

```python
class CustomModel(nn.Module):
    def __init__(self, num_classes=10):
        super(CustomModel, self).__init__()
        # 모델 레이어 정의

    def forward(self, x):
        # Forward pass 정의
        return x
```

### 다른 데이터셋 사용

`train.py`의 `get_data_loaders()` 함수를 수정하여 다른 데이터셋을 사용할 수 있습니다:

```python
# CIFAR-10 예제
train_dataset = datasets.CIFAR10(
    root=data_dir,
    train=True,
    download=True,
    transform=transform
)
```

## 라이선스

MIT License

## 문의

이슈나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.
