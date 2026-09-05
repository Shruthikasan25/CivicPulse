import json
from datetime import datetime

class EvidenceFusionEngine:
    def __init__(self):
        # High-priority keywords that indicate a severe infrastructure failure
        self.critical_keywords = ['burst', 'gushing', 'flowing', 'shooting', 'massive', 'flooded', 'continuous']
        self.moderate_keywords = ['puddle', 'wet', 'trickle', 'seeping', 'damp']

    def analyze_text(self, description):
        """Analyzes the citizen's text for urgency signals."""
        desc_lower = description.lower()
        score = 50  # Base score
        
        # Check for critical severity
        if any(word in desc_lower for word in self.critical_keywords):
            score += 35
        # Check for moderate severity
        elif any(word in desc_lower for word in self.moderate_keywords):
            score += 15
            
        return min(score, 100) # Cap at 100

    def analyze_image_mock(self, image_path):
        """
        Placeholder for the Computer Vision model (YOLO/Classifier).
        For Phase 1, it safely verifies if visual evidence is attached without crashing.
        """
        if image_path and image_path != "None":
            return 85 # High confidence if an image is provided
        return 40 # Low confidence if no visual evidence exists

    def evaluate_new_report(self, report_data):
        """The main real-time AI fusion pipeline."""
        print(f"\n--- Processing New Citizen Report ---")
        
        # 1. Text NLP Analysis
        text_confidence = self.analyze_text(report_data.get('description', ''))
        
        # 2. Vision Analysis (Mocked for Phase 1 stability)
        vision_confidence = self.analyze_image_mock(report_data.get('image_path'))
        
        # 3. Evidence Fusion (Weighted Average)
        # 60% weight to image evidence, 40% to text description
        final_confidence = int((vision_confidence * 0.6) + (text_confidence * 0.4))
        
        # 4. Action Decision
        action = "DISPATCH CREW" if final_confidence >= 80 else "MONITOR / VERIFY"

        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "evaluation": {
                "text_urgency_score": text_confidence,
                "visual_evidence_score": vision_confidence,
                "ai_confidence_score": final_confidence,
                "recommended_action": action
            }
        }
        return response

if __name__ == "__main__":
    # Test Scenario: A judge submits a critical new report right now
    engine = EvidenceFusionEngine()
    
    test_report = {
        "description": "Water is gushing continuously from a massive crack in the middle of the road!",
        "image_path": "images/real_leak.jpg",
        "latitude": 12.971593,
        "longitude": 79.158502
    }
    
    result = engine.evaluate_new_report(test_report)
    print(json.dumps(result, indent=4))