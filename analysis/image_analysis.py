
import os

from detectors.image_detector import SynthGuardImageDetector
from analysis.metadata import ImageMetadataAnalyzer


class SynthGuardImageAnalyzer:

    def __init__(self):

        self.detector = SynthGuardImageDetector()
        self.metadata_analyzer = ImageMetadataAnalyzer()


    # ========================================================
    # RISK CALCULATION
    # ========================================================

    def calculate_risk(self, ai_probability):

        if ai_probability >= 80.0:
            return "HIGH"

        elif ai_probability >= 50.0:
            return "MEDIUM"

        else:
            return "LOW"


    # ========================================================
    # EXPLANATION GENERATION
    # ========================================================

    def generate_explanation(self, ai_probability, metadata):

        explanations = []

        if ai_probability >= 80.0:

            explanations.append(
                "The AI detector gives a high probability "
                "that the image is AI-generated."
            )

        elif ai_probability >= 50.0:

            explanations.append(
                "The AI detector gives a moderate probability "
                "that the image may be AI-generated."
            )

        else:

            explanations.append(
                "The AI detector gives a higher probability "
                "that the image is human/real."
            )

        if metadata["has_exif"]:

            explanations.append(
                "EXIF metadata is present and can provide "
                "supporting information about the image."
            )

        else:

            explanations.append(
                "No EXIF metadata was detected. This can happen "
                "after image editing, compression, screenshots, "
                "or social-media processing."
            )

        if (
            metadata["camera_make"]
            or metadata["camera_model"]
        ):

            explanations.append(
                "Camera information was found in the metadata."
            )

        return explanations


    # ========================================================
    # COMPLETE IMAGE ANALYSIS
    # ========================================================

    def analyze(self, image_path):

        if not os.path.exists(image_path):

            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        # ----------------------------------------------------
        # AI DETECTION
        # ----------------------------------------------------

        detector_result = self.detector.predict(
            image_path
        )

        # ----------------------------------------------------
        # METADATA ANALYSIS
        # ----------------------------------------------------

        metadata = self.metadata_analyzer.analyze(
            image_path
        )

        # ----------------------------------------------------
        # RAW MODEL RESULTS
        # ----------------------------------------------------

        raw_ai_probability = float(
            detector_result["ai_probability"]
        )

        raw_real_probability = float(
            detector_result["real_probability"]
        )

        # ----------------------------------------------------
        # CONVERT 0-1 TO 0-100 PERCENT
        # ----------------------------------------------------

        ai_probability = raw_ai_probability * 100.0
        real_probability = raw_real_probability * 100.0

        # Keep values within valid percentage range

        ai_probability = max(
            0.0,
            min(100.0, ai_probability)
        )

        real_probability = max(
            0.0,
            min(100.0, real_probability)
        )

        # ----------------------------------------------------
        # NORMALIZE TO 100%
        # ----------------------------------------------------

        total = ai_probability + real_probability

        if total > 0:

            ai_probability = (
                ai_probability / total
            ) * 100.0

            real_probability = (
                real_probability / total
            ) * 100.0

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        if ai_probability >= real_probability:

            prediction = "AI-generated"
            confidence = ai_probability

        else:

            prediction = "Human/Real"
            confidence = real_probability

        # ----------------------------------------------------
        # RISK
        # ----------------------------------------------------

        risk_level = self.calculate_risk(
            ai_probability
        )

        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        explanation = self.generate_explanation(
            ai_probability,
            metadata
        )

        # ----------------------------------------------------
        # IMAGE INFORMATION
        # ----------------------------------------------------

        image_info = {
            "filename": metadata.get("filename"),
            "format": metadata.get("format"),
            "width": metadata.get("width"),
            "height": metadata.get("height"),
            "color_mode": metadata.get("color_mode"),
            "file_size_bytes": metadata.get("file_size_bytes")
        }

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return {

            "prediction": prediction,

            "confidence": confidence,

            "ai_probability": ai_probability,

            "real_probability": real_probability,

            "risk": risk_level,

            "explanation": explanation,

            "evidence": metadata,

            "image_info": image_info,

            "metadata": metadata
        }
