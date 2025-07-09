import pyttsx3
import os
import sys
import time
import warnings
from os import system, environ

import pyautogui
import speech_recognition as sr
import whisper
import webbrowser
import google.generativeai as genai

# Configure environment paths
os.environ["PATH"] += os.pathsep + "C:\\ffmpeg\\bin"
os.environ["FFMPEG_BINARY"] = "C:\\ffmpeg\\bin\\ffmpeg.exe"

engine = pyttsx3.init()
engine.setProperty("rate", 125)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Constants and configurations
ASSISTANT_NAME = "ScraPy"
ASSISTANT_NICKNAME = "CrashAppeared"
LISTEN_FOR_TRIGGER_WORD = True
SHOULD_RUN = True
GOOGLE_API_KEY = "AIzaSyAjvN0bGVEBFuGaUjlHsLIUH1W647FM0yI"

# Initialize Gemini
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")  # Đã đổi tên model


def respond(text: str) -> str:
    """Convert text to speech and return the response."""
    try:
        print(f"{ASSISTANT_NAME}: {text}")

        if sys.platform == "darwin":
            ALLOWED_CHARS = set(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ "
            )
            clean_text = "".join(c for c in text if c in ALLOWED_CHARS)
            system(f"say '{clean_text}'")
        else:
            engine.say(text)
            engine.runAndWait()
        return text
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def listen_for_command() -> str:
    """Listen for and transcribe voice commands."""
    try:
        with source as s:
            print("Listening to command...")
            recognizer.adjust_for_ambient_noise(s)
            audio = recognizer.listen(s)

            with open(COMMAND_FILE_PATH, "wb") as f:
                f.write(audio.get_wav_data())

            command = base_model.transcribe(COMMAND_FILE_PATH, fp16=False)
            return command["text"].lower() if command and command["text"] else None

    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
    except sr.RequestError:
        print("Unable to access the Google Speech Recognition API.")
        return None
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        return None


def perform_command(command: str) -> None:
    """Process and execute the given command."""
    global SHOULD_RUN
    global LISTEN_FOR_TRIGGER_WORD

    if command:
        print(f"You: {command}")
        if "exit" in command.lower():
            SHOULD_RUN = False
        else:
            response = gemini_model.generate_content(command)
            output = response.text
            respond(output)
    LISTEN_FOR_TRIGGER_WORD = True


def main() -> None:
    """Main function to run the assistant."""
    global LISTEN_FOR_TRIGGER_WORD

    while SHOULD_RUN:
        # command = listen_for_command()

        if LISTEN_FOR_TRIGGER_WORD:
            LISTEN_FOR_TRIGGER_WORD = False
        else:
            # _____________________________________
            command = "Who's Bill Gates?"
            perform_command(command)
            command = "ExIt"
            # _____________________________________
            perform_command(command)
    respond("Goodbye!")


if __name__ == "__main__":
    main()
