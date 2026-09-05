
class SynthGuardReportGenerator:

    def generate_report(self, result):

        evidence = result["evidence"]

        ai_probability = result["ai_probability"] * 100
        real_probability = result["real_probability"] * 100

        prediction = result["prediction"]
        risk_level = result["risk_level"]

        print()
        print("=" * 65)
        print("                    SYNTHGUARD REPORT")
        print("=" * 65)

        print()
        print("Prediction :", prediction)

        print()

        print(
            f"AI-generated probability : "
            f"{ai_probability:.2f}%"
        )

        print(
            f"Human/Real probability   : "
            f"{real_probability:.2f}%"
        )

        print()

        print("Risk Level :", risk_level)

        print()
        print("---------------- IMAGE INFORMATION ----------------")

        print(
            "Filename       :",
            evidence.get(
                "filename",
                "Not available"
            )
        )

        print(
            "Format         :",
            evidence.get(
                "format",
                "Not available"
            )
        )

        print(
            "Resolution     :",
            f"{evidence.get('width', 'Unknown')} × "
            f"{evidence.get('height', 'Unknown')}"
        )

        print(
            "Color mode     :",
            evidence.get(
                "color_mode",
                "Not available"
            )
        )

        print()
        print("---------------- METADATA ----------------")

        print(
            "EXIF metadata  :",
            "Detected"
            if evidence.get("has_exif", False)
            else "Not detected"
        )

        print(
            "Camera make    :",
            evidence.get("camera_make")
            or "Not detected"
        )

        print(
            "Camera model   :",
            evidence.get("camera_model")
            or "Not detected"
        )

        print(
            "Software       :",
            evidence.get("software")
            or "Not detected"
        )

        print()
        print("---------------- ANALYSIS ----------------")

        for explanation in result.get(
            "explanation",
            []
        ):

            print("•", explanation)

        print()
        print("=" * 65)
        print("                  END OF IMAGE REPORT")
        print("=" * 65)

    def print_important_note(self):

        print()
        print()
        print("=" * 65)
        print("                  IMPORTANT NOTE")
        print("=" * 65)

        print()

        print(
            "AI detection is probabilistic and should not be "
            "treated as absolute proof."
        )

        print(
            "Metadata is supporting evidence and can be removed "
            "or modified by image-processing software."
        )

        print()
        print("=" * 65)
