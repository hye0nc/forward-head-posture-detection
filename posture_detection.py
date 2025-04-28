import cv2
import mediapipe as mp
import numpy as np
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def calculate_angle(x1, y1, x2, y2):
    """어깨와 귀 사이 선과 수평선 사이의 각도를 계산 (CVA 근사)"""
    dx = x2 - x1
    dy = y2 - y1
    angle = math.degrees(math.atan2(abs(dy), dx))
    return angle


cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    # heavy 모델: model_complexity=2
    # full 모델: model_complexity=1
    # light 모델: model_complexity=0
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as pose:
    while cap.isOpened():
        # 0번째 카메라 사용
        success, image = cap.read()
        if not success:
            print("카메라를 찾을 수 없습니다.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            )

            if results.pose_world_landmarks:
                landmarks = results.pose_world_landmarks.landmark
                nose = landmarks[mp_pose.PoseLandmark.NOSE]
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR]

                # z 좌표 기반 감지 (정면 뷰)
                if (
                    nose.visibility > 0.3
                    and left_shoulder.visibility > 0.3
                    and right_shoulder.visibility > 0.3
                ):
                    shoulder_mid_z = (left_shoulder.z + right_shoulder.z) / 2
                    z_diff = nose.z - shoulder_mid_z
                    print(f"z 차이: {z_diff:.4f} 미터")
                    if z_diff > -0.04:  # 임계값 조정 필요
                        print("거북목이 감지 (z 좌표 기준)")

                # CVA 기반 감지 (측면 뷰)
                if left_shoulder.visibility > 0.3 and left_ear.visibility > 0.3:
                    shoulder_x = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_SHOULDER
                    ].x
                    shoulder_y = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_SHOULDER
                    ].y
                    ear_x = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_EAR
                    ].x
                    ear_y = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_EAR
                    ].y
                    cva = calculate_angle(shoulder_x, shoulder_y, ear_x, ear_y)
                    print(f"CVA: {cva:.2f}도")
                    if cva > 110:  # 임계값 조정 필요
                        print("거북목 감지 (CVA 기준)")

        cv2.imshow("MediaPipe Pose", cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
