from PIL import Image
from transformers import pipeline

# Initialize Hugging Face pipelines
caption_pipeline = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
plant_disease_pipeline = pipeline("image-classification", model="microsoft/beit-base-patch16-224-pt22k-ft22k")

def generate_caption_and_detect_disease(image):
    try:
        # Get disease results
        disease_result = plant_disease_pipeline(image)
        print("Disease Result: ", disease_result)  # Debug print
        
        # Extract labels and scores
        diseases = [
            {"label": plant_disease_pipeline.model.config.id2label[i], "score": score.item()}
            for i, score in enumerate(disease_result[0]["scores"])
        ]
        
        caption = "Detected diseases from the image."
        
        return caption, diseases
    except KeyError as e:
        print(f"KeyError: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise