# From: Zero to AI Agent, Chapter 7, Section 7.1
# File: rule_based_vs_ml.py

"""
Compares rule-based systems (traditional AI) with machine learning approaches
using a plant problem diagnosis example.
"""

# Rule-Based System (Old School AI)
def diagnose_plant_problem_rules(symptoms):
    """
    Traditional rule-based approach to plant diagnosis.
    Every decision is explicitly programmed.
    
    Problems with this approach:
    - Requires extensive manual rule creation
    - Can't handle cases not explicitly programmed
    - Doesn't improve with experience
    - Misses subtle pattern combinations
    """
    # Convert symptoms to lowercase for comparison
    symptoms_lower = [s.lower() for s in symptoms]
    
    # Explicitly programmed decision tree
    if "yellow_leaves" in symptoms_lower:
        if "brown_tips" in symptoms_lower:
            return "Overwatering - reduce watering frequency"
        elif "pale_green" in symptoms_lower:
            return "Iron deficiency - add iron supplement"
        else:
            return "Nitrogen deficiency - add fertilizer"
    
    elif "brown_spots" in symptoms_lower:
        if "fuzzy_growth" in symptoms_lower:
            return "Fungal infection - apply fungicide"
        else:
            return "Bacterial infection - remove affected leaves"
    
    elif "wilting" in symptoms_lower:
        if "dry_soil" in symptoms_lower:
            return "Underwatering - increase water"
        else:
            return "Root rot - check drainage"
    
    elif "holes_in_leaves" in symptoms_lower:
        return "Pest damage - inspect for insects"
    
    else:
        return "Unknown problem - consult expert"


# Machine Learning Approach (Modern AI) - Conceptual
class PlantDiagnosisML:
    """
    Machine Learning approach to plant diagnosis.
    The system learns patterns from thousands of examples.
    
    In reality, this would use:
    - Computer vision to analyze plant images
    - Neural networks trained on plant disease databases
    - Pattern recognition across multiple features
    """
    
    def __init__(self):
        # In a real system, we'd load a trained model here
        self.model_trained = False
        self.training_examples = 0
    
    def train(self, examples):
        """
        Simulates training on plant examples.
        Real ML would use algorithms like:
        - Convolutional Neural Networks for image analysis
        - Random Forests for symptom classification
        - Deep Learning for complex pattern recognition
        """
        self.training_examples += len(examples)
        self.model_trained = True
        print(f"Model trained on {self.training_examples} plant examples")
        
        # A real model would learn patterns like:
        # - Yellow + drooping often means overwatering
        # - Spots with rings usually indicate fungal issues
        # - Certain patterns appear together in specific diseases
    
    def diagnose(self, plant_image_or_symptoms):
        """
        ML diagnosis based on learned patterns.
        
        Real advantages over rules:
        - Handles cases never explicitly programmed
        - Identifies subtle patterns humans miss
        - Improves with more data
        - Can consider hundreds of features simultaneously
        """
        if not self.model_trained:
            return "Model needs training first"
        
        # Simplified demonstration
        # Real ML would process image pixels, extract features,
        # and run through neural network layers
        
        return {
            'diagnosis': 'Likely fungal infection (confidence: 87%)',
            'alternative': 'Possible overwatering (confidence: 12%)',
            'recommendation': 'Reduce humidity, improve air circulation',
            'learned_from': f'{self.training_examples} similar cases'
        }


def demonstrate_approaches():
    """Shows the difference between rule-based and ML approaches."""
    
    print("="*60)
    print("RULE-BASED vs MACHINE LEARNING PLANT DIAGNOSIS")
    print("="*60)
    
    # Test case
    symptoms = ["yellow_leaves", "brown_tips", "drooping"]
    
    # Rule-based approach
    print("\n1. RULE-BASED APPROACH:")
    print("-" * 30)
    diagnosis_rules = diagnose_plant_problem_rules(symptoms)
    print(f"Symptoms: {symptoms}")
    print(f"Diagnosis: {diagnosis_rules}")
    print("\nLimitations:")
    print("• Only handles pre-programmed combinations")
    print("• Can't improve with experience")
    print("• Might miss subtle patterns")
    
    # ML approach
    print("\n2. MACHINE LEARNING APPROACH:")
    print("-" * 30)
    ml_system = PlantDiagnosisML()
    
    # Simulate training
    training_data = [
        {'image': 'plant1.jpg', 'diagnosis': 'overwatering'},
        {'image': 'plant2.jpg', 'diagnosis': 'fungal'},
        # ... thousands more examples
    ]
    ml_system.train(training_data)
    
    # Get diagnosis
    ml_diagnosis = ml_system.diagnose(symptoms)
    print(f"Symptoms: {symptoms}")
    print(f"ML Diagnosis: {ml_diagnosis}")
    
    print("\nAdvantages:")
    print("• Learns from experience")
    print("• Finds patterns humans might miss")
    print("• Handles novel combinations")
    print("• Improves with more data")


if __name__ == "__main__":
    demonstrate_approaches()
    
    print("\n" + "="*60)
    print("KEY TAKEAWAY")
    print("="*60)
    print("Rule-Based: You program every decision")
    print("Machine Learning: System learns patterns from data")
    print("\nModern AI uses ML because the world is too complex for rules!")
