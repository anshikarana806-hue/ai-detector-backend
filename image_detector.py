import torch
import timm
import cv2
import numpy as np
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

cnn = timm.create_model("efficientnet_b0", pretrained=True, num_classes=2)
cnn.eval().to(device)

def artifact_analysis(image: Image.Image):
    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    noise = np.var(gray)
    edges = cv2.Canny(gray, 100, 200).mean()

    ai_score = 0
    reasons = []

    if noise < 200:
        ai_score += 1
        reasons.append("Low sensor noise (common in AI images)")

    if edges < 20:
        ai_score += 1
        reasons.append("Unnaturally smooth edge distribution")

    return ai_score, reasons
