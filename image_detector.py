import cv2
import numpy as np
from PIL import Image

def analyze_image(image_bytes):
    image = Image.open(image_bytes).convert("RGB")
    img = np.array(image)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 1️⃣ Noise analysis
    noise = cv2.Laplacian(gray, cv2.CV_64F).var()

    # 2️⃣ Frequency artifacts (FFT)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude = 20 * np.log(np.abs(fshift) + 1)
    freq_score = np.mean(magnitude)

    # 3️⃣ Edge sharpness
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges > 0)

    # 4️⃣ Color entropy
    hist = cv2.calcHist([img], [0,1,2], None, [8,8,8], [0,256]*3)
    hist = hist / np.sum(hist)
    color_entropy = -np.sum(hist * np.log2(hist + 1e-9))

    score = (
        (freq_score * 0.4) +
        (edge_density * 100 * 0.3) +
        (color_entropy * 0.3)
    )

    is_ai = score > 85

    reasons = []
    if freq_score > 60:
        reasons.append("Unnatural frequency artifacts")
    if edge_density < 0.05:
        reasons.append("Over-smooth edges")
    if color_entropy < 4:
        reasons.append("Low color randomness")

    return {
        "ai_generated": is_ai,
        "confidence": min(95, int(abs(score))),
        "reasons": reasons or ["Natural photographic patterns detected"]
    }
