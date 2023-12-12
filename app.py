import json
from pathlib import Path
import random
import time
import numpy as np
from shiny import App, render, ui, reactive
from shiny.types import ImgData
import threading


from sleep_detection import read_frame_and_annotatte

app_ui = ui.page_fluid(
    ui.tags.style(
        """
        .app-col {
            border: 1px solid black;
            border-radius: 5px;
            background-color: #eee;
            padding: 8px;
            margin-top: 5px;
            margin-bottom: 5px;
        }
        """
    ),
    ui.row(
        ui.column(6, ui.output_image("driver_video")),
        ui.column(
            6,
            {"id": "chat-history"},
            ui.h1("Interaction History"),
            ui.output_text("chat_history"),
        ),
    ),
)

# diyalogu baslat -> 1
# diyalog gecmisi
from chat import OPENAIController

openai_controller = OPENAIController()

# IDLE, STARTED

sleepy_conv_starter = "I feel sleepy. Warn me politely"


def server(input, output, session):
    image_container = reactive.Value(random.randint(0, 1000))
    dialog_history = reactive.Value(
        [
            {
                "role": "system",
                "content": "You are a in-car voice assistant. Plase provide answers that are short and to the point. Your responses should now exceed 20 words. Try to make them as shot as possible",
            }
        ]
    )

    driver_state = reactive.Value("SLEEPING")
    dialog_state = reactive.Value("IDLE")

    def update_driver_state():
        print("Triggered")
        tmpbuf = dialog_history.get()
        dialog_history.unset()
        tmpbuf.append({"role": "user", "content": sleepy_conv_starter})
        setting_successful = dialog_history.set(tmpbuf)
        print(setting_successful)

        ai_answer = openai_controller.assistant_chat(
            history=dialog_history.get(), new_message=sleepy_conv_starter
        )
        tmpbuf = dialog_history.get()
        dialog_history.unset()
        tmpbuf.append({"role": "assistant", "content": ai_answer})
        dialog_history.set(tmpbuf)

    @reactive.Effect
    async def _():
        reactive.invalidate_later(0.1)
        if driver_state.get() == "SLEEPING" and dialog_state.get() == "IDLE":
            # prevent unnecessary re-execution
            print("Triggered")
            dialog_state.set("STARTED")
            t = threading.Thread(target=update_driver_state)
            t.start()

    @reactive.Effect
    async def __():
        reactive.invalidate_later(0.1)
        image, is_sleeping = read_frame_and_annotatte()
        # if is_sleeping:
        #     driver_state.set("SLEEPING")
        image_container.set(image)

    @output
    @render.text
    async def chat_history():
        return f"\n".join([str(d["content"]) for d in dialog_history.get()])

    @output
    @render.image
    async def driver_video():
        dir = Path(__file__).resolve().parent
        img: ImgData = {"src": str(dir / image_container.get()), "width": "600px"}
        return img


app = App(app_ui, server)
