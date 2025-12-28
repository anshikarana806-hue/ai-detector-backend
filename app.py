from fastapi import FastAPI, UploadFile, File
from image_detector import analyze_image
from video_detector import analyze_video

app = FastAPI(title="AI Generated Media Detector")

@app.get("/")
def root():
    return {"status": "AI Detector API running"}

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    result = analyze_image(file.file)
    return result

@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...)):
    result = analyze_video(file.file)
    return result
