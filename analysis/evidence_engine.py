
import os

from analysis.image_analysis import SynthGuardImageAnalyzer
from detectors.text_detector import SynthGuardTextDetector


class SynthGuardEvidenceEngine:

    def __init__(self):

        print("Initializing SynthGuard Evidence Engine...")
        print()

        self.image_analyzer = SynthGuardImageAnalyzer()

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

        result = self.image_analyzer.analyze(
            image_path
        )

        # ----------------------------------------------------
        # Safety fallback for risk
        # ----------------------------------------------------

        ai_probability = float(
            result["ai_probability"]
        )

        if ai_probability >= 80.0:
            risk = "HIGH"

        elif ai_probability >= 50.0:
            risk = "MEDIUM"

        else:
            risk = "LOW"

        return {

            "media_type": "image",

            "prediction": result["prediction"],

            "confidence": result["confidence"],

            "ai_probability": result["ai_probability"],

            "real_probability": result["real_probability"],

            "risk": risk,

            "explanation": result["explanation"],

            "evidence": result["evidence"],

            "image_info": result["image_info"],

            "metadata": result["metadata"]
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

        # ----------------------------------------------------
        # ModernBERT
        # ----------------------------------------------------

        detector_result = self.text_detector.predict(
            text
        )

        ai_probability = float(
            detector_result["ai_probability"]
        )

        human_probability = float(
            detector_result["human_probability"]
        )

        # ----------------------------------------------------
        # Validate probabilities
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
        # Normalize to exactly 100%
        # ----------------------------------------------------

        total = (
            ai_probability +
            human_probability
        )

        if total > 0:

            ai_probability = (
                ai_probability / total
            ) * 100.0

            human_probability = (
                human_probability / total
            ) * 100.0

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
        # Risk + explanation
        # ----------------------------------------------------

        if ai_probability >= 80.0:

            risk = "HIGH"

            explanation = (
                "The text shows a high probability of being "
                "AI-generated according to the trained detector."
            )

        elif ai_probability >= 50.0:

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
        # FINAL TEXT RESULT
        # ----------------------------------------------------

        return {

            "media_type": "text",

            "prediction": prediction,

            "confidence": confidence,

            "ai_probability": ai_probability,

            "human_probability": human_probability,

            "risk": risk,

            "explanation": explanation
        }
