import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import tempfile
import cv2
import os


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


max_distance_left = 0
max_distance_right = 0
min_distance_left = 99999
min_distance_right = 99999

image_width = 0
image_height = 0

from enum import Enum


class DRIVER_STATE(Enum):
    SLEEPING = "sleeping"
    AWAKE = "awake"


driver_state = DRIVER_STATE.AWAKE
driver_state_count = 0

base_options = python.BaseOptions(model_asset_path="face_model.task")
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1,
)
detector = vision.FaceLandmarker.create_from_options(options)
cap = cv2.VideoCapture(0)
latest_file = ""


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

        cv2.circle(
            annotated_image,
            (x, y),
            radius=1,
            color=(255, 0, 0) if idx in left_eye_landmarks else (0, 255, 255),
        )
        # cv2.putText(
        #     annotated_image,
        #     str(idx),
        #     (x, y),
        #     fontFace=1,
        #     fontScale=0.5,
        #     color=(255, 0, 0),
        # )
    return annotated_image


def calculate_center(landmarks):
    centerx = 0
    centery = 0
    for l in landmarks:
        centerx += int(l.x * image_width)
        centery += int(l.y * image_height)
    centerx = int(centerx / len(landmarks))
    centery = int(centery / len(landmarks))
    return centerx, centery


def calculate_distance(landmarks):
    centerx, centery = calculate_center(landmarks)
    distancex = 0
    distancey = 0
    for l in landmarks:
        distancex += int(abs(int(l.x * image_width) - centerx))
        distancey += int(abs(int(l.y * image_height) - centery))

    return distancex, distancey, distancey + distancex


def driver_sleeping(
    eye_landmarks,
):
    global driver_state, driver_state_count
    global max_distance_left
    global max_distance_right
    global min_distance_left
    global min_distance_right

    left_landmarks = [
        eye_landmarks[i] for i in range(len(eye_landmarks)) if i in left_eye_landmarks
    ]
    right_landmarks = [
        eye_landmarks[i] for i in range(len(eye_landmarks)) if i in right_eye_landmarks
    ]

    _, _, left_distance = calculate_distance(left_landmarks)
    _, _, right_distance = calculate_distance(right_landmarks)

    if left_distance > max_distance_left:
        max_distance_left = left_distance
    if left_distance < min_distance_left:
        min_distance_left = left_distance
    if right_distance > max_distance_right:
        max_distance_right = right_distance
    if right_distance < min_distance_right:
        min_distance_right = right_distance

    cur_state = True if left_distance < 190 or right_distance < 190 else False
    if cur_state:
        cur_state = DRIVER_STATE.SLEEPING
    else:
        cur_state = DRIVER_STATE.AWAKE

    # if old state and new state is same then incerement the count
    if cur_state == driver_state:
        driver_state_count += 1
    # if state is changed then reset the state count
    else:
        driver_state = cur_state
        driver_state_count = 0

    # if driver state is sleeping and state_count is bigger than 5(last 5 frame sleeping state)
    if driver_state == DRIVER_STATE.SLEEPING and driver_state_count > 5:
        return (True,)
    return False


def read_frame_and_annotatte():
    global max_distance_left
    global max_distance_right
    global min_distance_left
    global min_distance_right
    global image_height, image_width

    ret, frame = cap.read()
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    image_height = image.height
    image_width = image.width

    detection_result = detector.detect(image)

    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    is_sleeping = driver_sleeping(detection_result.face_landmarks[0])
    print(max_distance_left, max_distance_right, min_distance_left, min_distance_right)

    cv2.putText(
        annotated_image,
        "SLEEPING" if is_sleeping else "AWAKE",
        org=(50, 50),
        fontFace=2,
        fontScale=2,
        color=(0, 0, 255),
    )

    # save image to a file

    temp_file_path = tempfile.mkstemp(suffix=".png", dir="static")
    cv2.imwrite(temp_file_path[1], annotated_image)
    global latest_file
    if os.path.exists(latest_file):
        os.remove(latest_file)
    latest_file = temp_file_path[1]

    return temp_file_path[1].split("/")[-1], is_sleeping
    # is_sleeping
    # if annotated_image is not None:
    #     cv2.imshow("face", annotated_image)
    #     cv2.waitKey(0)
