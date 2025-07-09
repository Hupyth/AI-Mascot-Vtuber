import os
from dotenv import load_dotenv

load_dotenv()

# ====== Paths ======
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "C:\\ffmpeg\\bin")
BASE_MODEL_PATH = "whisper/base.pt"

# ====== Device ======
MIC_DEVICE_INDEX = 1

# ====== Assistant Info ======
ASSISTANT_NAME = "ScraPy"
ASSISTANT_NICKNAME = "CrashAppeared"
VOICE_RATE = 125

# ====== API Keys ======
GEMINI_KEYS = os.getenv("GEMINI_KEYS").split(",")
OPENAI_KEYS = os.getenv("OPENAI_KEYS").split(",")
