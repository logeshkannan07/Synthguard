
import os
from transformers import pipeline
from PIL import Image


class SynthGuardImageDetector:

    def __init__(self):

        self.model_name = "Smogy/SMOGY-Ai-images-detector"

        self.detector = pipeline(
            "image-classification",
            model=self.model_name
        )

    def predict(self, image_path):

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = Image.open(image_path).convert("RGB")

        results = self.detector(image)

        ai_probability = 0.0
        real_probability = 0.0

        for result in results:

            label = result["label"].lower()
            score = float(result["score"])

            if label in ["artificial", "ai", "fake"]:
                ai_probability = score

            elif label in ["human", "real"]:
                real_probability = score

        if ai_probability >= real_probability:
            prediction = "AI-generated"
            confidence = ai_probability
        else:
            prediction = "Human/Real"
            confidence = real_probability

        return {
            "prediction": prediction,
            "confidence": confidence,
            "ai_probability": ai_probability,
            "real_probability": real_probability
        }
