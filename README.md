
# Roach: Smart Car Assistant

Roach is a smart car assistant designed to enhance the driving experience by detecting driver fatigue and engaging in natural conversations. It features advanced capabilities such as function matching for commands like opening music or adjusting the AC.

[Slides](https://docs.google.com/presentation/d/1Bvz7Jjc12NPEY--Cc_XfTcGq5MlKbuA5ew94Y3gOsl8/edit?usp=sharing)
[Demo Video](https://www.youtube.com/watch?v=8EFbl8HcYrE)
## Features

- **Driver Monitoring**: Roach uses advanced algorithms to monitor the driver's state and detects if the driver is snoozing or fatigued.

- **Function Matching**: Recognizes user commands related to car functions, such as opening music, adjusting volume, or controlling the AC.

- **Natural Conversations**: Engages in natural conversations with the driver, making the driving experience more interactive and enjoyable.

- **User Interface**: Provides a user interface that visualizes the internal state of the car, including the camera feed of the driver and the history of previous dialogs.

## Getting Started

To get started with Roach, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/roach.git
   cd roach
2. install requirements with  
    ```bash
   pip install -r requirements
4. Downlaod the face landmark detection model from 
    ```bash
    !wget -O face_landmarker_v2_with_blendshapes.task -q https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
