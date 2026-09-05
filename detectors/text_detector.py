import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class SynthGuardTextDetector:

    MODEL_NAME = "rasbt/ai-text-detector-modernbert"

    def __init__(self):

        print("Loading ModernBERT AI Text Detector...")
        print("Model:", self.MODEL_NAME)
        print()

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.MODEL_NAME
        )

        self.model.eval()

        # Show the model's actual label mapping
        print("Model label mapping:", self.model.config.id2label)

        print("ModernBERT loaded successfully.")

    def predict(self, text):

        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        if not text.strip():
            raise ValueError("Text cannot be empty.")

        inputs = self.tokenizer(
            text,
            truncation=True,
            max_length=8192,
            return_tensors="pt"
        )

        with torch.inference_mode():

            outputs = self.model(**inputs)

            probabilities = torch.softmax(
                outputs.logits,
                dim=-1
            )[0]

        # Get the model's actual label IDs
        human_probability = probabilities[0].item() * 100
        ai_probability = probabilities[1].item() * 100

        if ai_probability >= human_probability:

            prediction = "AI-generated"
            confidence = ai_probability

        else:

            prediction = "Human/Real"
            confidence = human_probability

        return {
            "prediction": prediction,
            "confidence": confidence,
            "ai_probability": ai_probability,
            "human_probability": human_probability
        }