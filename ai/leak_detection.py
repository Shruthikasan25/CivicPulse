import os
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from PIL import Image

print("Loading AI Models (this will take a minute on the first run)...")

# 1. Lightweight text embeddings model (~80MB)
text_model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Zero-shot vision model (~600MB)
vision_classifier = pipeline(
    "zero-shot-image-classification", 
    model="openai/clip-vit-base-patch32"
)

def get_text_score(description):
    """Scores how closely the text describes a physical pipe leak vs rain."""
    query_emb = text_model.encode(description)
    
    # Define our anchors
    leak_anchor = text_model.encode("urgent pressurized water main pipe burst leaking flowing from ground")
    rain_anchor = text_model.encode("stagnant puddles waterlogged flooded street after heavy rainfall")
    
    leak_sim = util.cos_sim(query_emb, leak_anchor).item()
    rain_sim = util.cos_sim(query_emb, rain_anchor).item()
    
    # Normalize score: Closer to 1.0 means it's definitely a leak
    score = max(0.0, min(1.0, (leak_sim - rain_sim) + 0.5))
    return round(score, 2)

def get_vision_score(image_path):
    """Uses zero-shot classification to detect leaks in photos."""
    # Fallback gracefully if the image hasn't been downloaded yet
    if not os.path.exists(image_path):
        return 0.5 
        
    try:
        image = Image.open(image_path)
        labels = [
            "a bursting water pipe", 
            "a flooded street from rain", 
            "normal dry road", 
            "trash on street"
        ]
        results = vision_classifier(image, candidate_labels=labels)
        
        # Extract the confidence score for the pipe leak label
        for res in results:
            if res['label'] == "a bursting water pipe":
                return round(res['score'], 2)
        return 0.0
    except Exception as e:
        print(f"Warning: Could not process {image_path}")
        return 0.5

def verify_report(description, image_path):
    """Combines text and vision scores into a final leak probability."""
    text_score = get_text_score(description)
    vision_score = get_vision_score(image_path)
    
    # Weight vision slightly higher than text (60/40 split)
    final_probability = (vision_score * 0.6) + (text_score * 0.4)
    return round(final_probability, 2)

if __name__ == "__main__":
    # Quick Test Run
    test_desc = "Critical emergency situation: An underground water pipe has completely failed."
    test_img = "images/burst_02.jpg"
    
    print("\n--- Testing Leak Detection Module ---")
    print(f"Description: '{test_desc}'")
    print(f"Text Score: {get_text_score(test_desc)}")
    print(f"Vision Score (Fallback to 0.5 if image is missing): {get_vision_score(test_img)}")
    print(f"Combined Probability: {verify_report(test_desc, test_img)}")