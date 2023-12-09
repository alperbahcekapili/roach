from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

left_eye_landmarks = [
    33,
    246,
    161,
    160,
    159,
    158,
    157,
    173,
    133,
    155,
    154,
    153,
    145,
    144,
    163,
    7,
]
right_eye_landmarks = [
    362,
    398,
    384,
    385,
    386,
    387,
    388,
    263,
    249,
    390,
    373,
    374,
    380,
    381,
    382,
]


def draw_landmarks_on_image(rgb_image, detection_result):
    if (
        type(detection_result.face_landmarks) != list
        or len(detection_result.face_landmarks) < 1
    ):
        return None

    face_landmarks_list = detection_result.face_landmarks[0]
    annotated_image = np.copy(rgb_image).astype(np.uint8)

    # Loop through the detected faces to visualize.
    for idx in range(len(face_landmarks_list)):
        if idx not in left_eye_landmarks and idx not in right_eye_landmarks:
            continue
        landmark = face_landmarks_list[idx]

        x = int(landmark.x * rgb_image.shape[1])
        y = int(landmark.y * rgb_image.shape[0])

        cv2.circle(annotated_image, (x, y), radius=1, color=(255, 0, 0))
        # cv2.putText(
        #     annotated_image,
        #     str(idx),
        #     (x, y),
        #     fontFace=1,
        #     fontScale=0.5,
        #     color=(255, 0, 0),
        # )
    return annotated_image


import cv2

base_options = python.BaseOptions(model_asset_path="face_model.task")
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1,
)
detector = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    # STEP 4: Detect face landmarks from the input image.
    detection_result = detector.detect(image)

    # STEP 5: Process the detection result. In this case, visualize ict.
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    if annotated_image is not None:
        cv2.imshow("face", annotated_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
