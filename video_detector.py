import cv2
from PIL import Image
from model import analyze_image

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    ai_votes = 0
    reasons = set()

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    step = max(1, fps)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % step == 0:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            result = analyze_image(img)

            if result["ai_generated"]:
                ai_votes += 1
                reasons.update(result["reasons"])

        frame_count += 1

    cap.release()

    ai_ratio = ai_votes / max(1, frame_count // step)

    return {
        "ai_generated": ai_ratio > 0.5,
        "confidence": int(ai_ratio * 100),
        "reasons": list(reasons)
    }
