
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

        if ai_probability >= 0.80:

            return "HIGH"

        elif ai_probability >= 0.50:

            return "MEDIUM"

        else:

            return "LOW"


    # ========================================================
    # EXPLANATION GENERATION
    # ========================================================

    def generate_explanation(
        self,
        ai_probability,
        metadata
    ):

        explanations = []


        if ai_probability >= 0.80:

            explanations.append(
                "The AI detector gives a high probability "
                "that the image is AI-generated."
            )

        elif ai_probability >= 0.50:

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
        # DETECTOR RESULTS
        # ----------------------------------------------------

        ai_probability = detector_result[
            "ai_probability"
        ]

        real_probability = detector_result[
            "real_probability"
        ]

        prediction = detector_result[
            "prediction"
        ]

        confidence = detector_result[
            "confidence"
        ]


        # ----------------------------------------------------
        # RISK LEVEL
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
        # FINAL RESULT
        # ----------------------------------------------------

        return {

            "prediction": prediction,

            "confidence": confidence,

            "ai_probability": ai_probability,

            "real_probability": real_probability,

            "risk_level": risk_level,

            "evidence": metadata,

            "explanation": explanation

        }
