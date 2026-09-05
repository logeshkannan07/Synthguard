
import os

from analysis.image_analysis import SynthGuardImageAnalyzer
from detectors.text_detector import SynthGuardTextDetector


class SynthGuardEvidenceEngine:

    def __init__(self):

        print("Initializing SynthGuard Evidence Engine...")
        print()

        # Image pipeline
        self.image_analyzer = SynthGuardImageAnalyzer()

        # Text pipeline
        self.text_detector = SynthGuardTextDetector()

        print()
        print("Evidence Engine initialized successfully.")

    # ========================================================
    # IMAGE ANALYSIS
    # ========================================================

    def analyze_image(self, image_path):

        if not isinstance(image_path, str):
            raise TypeError(
                "Image path must be a string."
            )

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        result = self.image_analyzer.analyze(image_path)

        return {
            "media_type": "image",
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "ai_probability": result["ai_probability"],
            "real_probability": result["real_probability"],
            "risk": result.get("risk"),
            "explanation": result.get("explanation"),
            "evidence": result.get("evidence"),
            "image_info": result.get("image_info"),
            "metadata": result.get("metadata")
        }

    # ========================================================
    # TEXT ANALYSIS
    # ========================================================

    def analyze_text(self, text):

        if not isinstance(text, str):
            raise TypeError(
                "Text must be a string."
            )

        if not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        # Send text to ModernBERT
        result = self.text_detector.predict(text)

        ai_probability = float(
            result["ai_probability"]
        )

        human_probability = float(
            result["human_probability"]
        )

        # ----------------------------------------------------
        # Keep probabilities valid
        # ----------------------------------------------------

        ai_probability = max(
            0.0,
            min(100.0, ai_probability)
        )

        human_probability = max(
            0.0,
            min(100.0, human_probability)
        )

        # ----------------------------------------------------
        # Normalize so probabilities total exactly 100%
        # ----------------------------------------------------

        total = ai_probability + human_probability

        if total > 0:

            ai_probability = (
                ai_probability / total
            ) * 100

            human_probability = (
                human_probability / total
            ) * 100

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        if ai_probability >= human_probability:

            prediction = "AI-generated"
            confidence = ai_probability

        else:

            prediction = "Human/Real"
            confidence = human_probability

        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        if ai_probability >= 80:

            risk = "HIGH"

            explanation = (
                "The text shows a high probability of being "
                "AI-generated according to the trained detector."
            )

        elif ai_probability >= 50:

            risk = "MEDIUM"

            explanation = (
                "The text shows mixed evidence. The detector "
                "cannot confidently classify it as human or "
                "AI-generated."
            )

        else:

            risk = "LOW"

            explanation = (
                "The text shows a higher probability of being "
                "human-written according to the trained detector."
            )

        # ----------------------------------------------------
        # Final standardized result
        # ----------------------------------------------------
        return {
             "media_type": "image",
             "prediction": result["prediction"],
             "confidence": result["confidence"],
             "ai_probability": result["ai_probability"],
             "real_probability": result["real_probability"],
             "risk": result["risk"],
             "explanation": result["explanation"],
             "evidence": result["evidence"]
        }
     
