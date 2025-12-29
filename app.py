from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from image_detector import analyze_image
from video_detector import analyze_video

app = FastAPI(title="AI Generated Media Detector")

# ✅ CORS FIX (THIS IS THE KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "AI Detector API running"}

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    return analyze_image(file.file)

@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...)):
    return analyze_video(file.file)
