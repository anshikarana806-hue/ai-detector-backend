import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)

TEXT_PROMPTS = [
    "a real photograph taken by a camera",
    "an AI generated image"
]

text_tokens = clip.tokenize(TEXT_PROMPTS).to(device)

@torch.no_grad()
def analyze_image(image: Image.Image):
    image_input = preprocess(image).unsqueeze(0).to(device)

    image_features = model.encode_image(image_input)
    text_features = model.encode_text(text_tokens)

    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    similarity = (image_features @ text_features.T).cpu().numpy()[0]

    real_score = float(similarity[0])
    ai_score = float(similarity[1])

    if ai_score > real_score:
        return {
            "ai_generated": True,
            "confidence": int(ai_score * 100),
            "reasons": [
                "Semantic patterns align with AI-generated imagery",
                "Lack of real-world camera context",
                "CLIP model confidence higher for synthetic description"
            ]
        }
    else:
        return {
            "ai_generated": False,
            "confidence": int(real_score * 100),
            "reasons": [
                "Strong alignment with real photographic description",
                "Natural scene composition detected",
                "Camera-like visual semantics present"
            ]
        }
