import cv2
import numpy as np
import tempfile

def analyze_video(video_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_bytes.read())
        video_path = tmp.name

    cap = cv2.VideoCapture(video_path)
    frame_scores = []

    frame_count = 0
    while cap.isOpened() and frame_count < 20:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F).var()
        frame_scores.append(lap)
        frame_count += 1

    cap.release()

    consistency = np.std(frame_scores)
    avg_noise = np.mean(frame_scores)

    is_ai = consistency < 15 or avg_noise < 50

    reasons = []
    if consistency < 15:
        reasons.append("Low temporal noise variation")
    if avg_noise < 50:
        reasons.append("Over-smooth frames")

    return {
        "ai_generated": is_ai,
        "confidence": min(90, int(100 - consistency)),
        "reasons": reasons or ["Natural temporal variations detected"]
    }

