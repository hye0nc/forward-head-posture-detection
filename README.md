# 거북목 감지 시스템 (MediaPipe 사용)

## 개요

이 프로젝트는 **MediaPipe Pose**를 활용하여 웹캠을 통해 실시간으로 거북목(앞으로 기울어진 머리 자세)을 감지하는 시스템입니다. 사용자의 자세를 분석하여 **크라니오버테브랄 각도(CVA)**와 **코와 어깨 간 z 좌표 차이**를 계산하고, 거북목이 감지되면 콘솔에 경고 메시지를 출력합니다.

이 프로젝트는 Python으로 작성되었으며, MediaPipe 라이브러리를 사용해 포즈 랜드마크를 감지하고, OpenCV를 통해 웹캠 영상을 캡처하며, NumPy를 활용해 수치 연산을 수행합니다.

## 기능

- 웹캠을 통한 실시간 자세 감지.
- 두 가지 감지 방법:
  - **z 좌표 차이**: 3D 공간에서 머리의 앞으로 기울어짐을 측정 (정면 뷰).
  - **크라니오버테브랄 각도(CVA)**: 어깨와 귀 사이의 각도를 추정 (측면 뷰).
- MediaPipe의 그리기 유틸리티를 사용해 영상에 포즈 랜드마크를 시각화.
- 거북목이 감지되면 콘솔에 경고 메시지 출력.

## 준비물

- Python 3.7 이상
- 웹캠 (장치에 연결된 상태)
- Python 및 컴퓨터 비전 개념에 대한 기본 이해

## 설치 방법

1. **저장소 복제** (해당되는 경우):

   ```bash
   git clone <저장소-URL>
   cd forward-head-posture-detection
   ```

2. **가상 환경 설정** (선택 사항, 권장):

   ```bash
   python -m venv env
   source env/bin/activate  # Windows에서는 env\Scripts\activate
   ```

3. **의존성 설치**:
   프로젝트에 필요한 Python 패키지는 `requirements.txt` 파일에 명시되어 있습니다. 다음 명령어로 설치하세요:

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` 파일 내용:

   ```
   opencv-python
   mediapipe
   numpy
   ```

## 사용 방법

1. **스크립트 실행**:
   메인 스크립트를 실행하여 자세 감지 시스템을 시작합니다:

   ```bash
   python posture_detection.py
   ```

2. **웹캠 앞에서 자세 잡기**:

   - **정면 뷰 감지** (z 좌표 방법): 카메라를 정면으로 바라보세요.
   - **측면 뷰 감지** (CVA 방법): 카메라를 측면에 두고 옆모습을 보여주세요 (예: 왼쪽 옆모습).

3. **콘솔 출력 확인**:

   - 스크립트는 각 프레임마다 z 좌표 차이(미터 단위)와 CVA 각도(도 단위)를 출력합니다.
   - 거북목이 감지되면 콘솔에 다음 메시지가 표시됩니다:
     ```
     z 차이: <값> 미터
     거북목 감지 (z 좌표 기준)
     ```
     또는
     ```
     CVA 각도: <값> 도
     거북목 감지 (CVA 기준)
     ```

4. **프로그램 종료**:
   `Esc` 키를 눌러 스크립트를 종료하고 웹캠 창을 닫습니다.

## 코드 설명

- **사용된 라이브러리**:

  - `cv2` (OpenCV): 웹캠 영상을 캡처하고 처리된 프레임을 표시합니다.
  - `mediapipe`: BlazePose 기반의 Pose Landmarker 모델을 사용해 33개의 포즈 랜드마크를 감지합니다.
  - `numpy`: 자세 분석을 위한 수치 연산을 수행합니다.
  - `math`: CVA 각도 계산을 위해 사용됩니다.

- **모델**:
  이 스크립트는 MediaPipe의 Pose Landmarker 모델(`pose_landmarker_full.tflite`)을 사용하며, 기본 설정인 `model_complexity=1`로 동작합니다. 이 모델은 2D 및 3D 포즈 랜드마크를 제공합니다.

- **감지 방법**:
  - **z 좌표 차이**: 코와 어깨 중간점의 z 좌표 차이를 계산합니다. 임계값 0.013미터를 기준으로 거북목을 감지합니다 (정면 뷰).
  - **크라니오버테브랄 각도(CVA)**: 왼쪽 어깨와 왼쪽 귀 사이의 각도를 측정합니다. 임계값 110도를 기준으로 거북목을 감지합니다 (측면 뷰, MediaPipe 좌표계에 맞게 조정됨).

## 커스터마이징

- **임계값 조정**:

  - 정면 뷰 감지를 위한 z 좌표 임계값(`0.013`)을 조정하세요:
    ```python
    if z_diff > 0.013:
        print("거북목이 감지되었습니다! (z 좌표 기준)")
    ```
  - 측면 뷰 감지를 위한 CVA 임계값(`110`)을 조정하세요:
    ```python
    if cva > 110:
        print("거북목이 감지되었습니다! (CVA 기준)")
    ```

- **모델 복잡도**:
  더 높은 정확도를 위해 성능을 희생하고 싶다면 `model_complexity=2`로 설정하세요:

  ```python
  with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=2) as pose:
  ```

- **가시성 임계값**:
  랜드마크 감지의 신뢰도를 높이기 위해 가시성 임계값(`visibility > 0.3`)을 조정할 수 있습니다:
  ```python
  if nose.visibility > 0.3 and left_shoulder.visibility > 0.3 and right_shoulder.visibility > 0.3:
  ```

## 한계

- **카메라 각도**: z 좌표 방법은 정면 뷰에서, CVA 방법은 측면 뷰에서 가장 효과적입니다. 적절한 위치를 잡아야 정확한 감지가 가능합니다.
- **조명 및 환경**: 어두운 조명이나 복잡한 배경은 랜드마크 감지 정확도에 영향을 줄 수 있습니다.
- **모델 정확도**: 기본 설정(`model_complexity=1`)은 균형 잡힌 성능을 제공합니다. 더 높은 정확도를 원한다면 `model_complexity=2`를 사용하세요. 단, 처리 속도가 느려질 수 있습니다.
- **임계값 민감도**: z 좌표와 CVA 임계값은 사용자 및 카메라 설정에 따라 조정해야 할 수 있습니다.

## 참고 자료

- [MediaPipe 포즈 랜드마크 감지 가이드](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
- [MediaPipe를 활용한 자세 분석 시스템 구축](https://learnopencv.com/building-a-body-posture-analysis-system-using-mediapipe/)
- [컴퓨터 비전을 활용한 머리 자세 평가](https://www.mdpi.com/2076-3417/13/6/3910)

<!-- ## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자유롭게 수정 및 배포가 가능합니다.

---

**작성자**: [사용자 이름]
**작성일**: 2025년 4월 -->
