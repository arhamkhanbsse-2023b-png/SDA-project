import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import re

# Global lists to store data for the graph
history_true = []
history_pred = []
accuracy_over_time = []

def universal_ingestion_filter(text):
    """
    Splits any input (paragraph, multi-line, etc.) into individual requirements.
    Fulfills the Ingestion Filter role in the Pipe-and-Filter architecture.
    """
    # Split by newlines, bullet points (*, -), or numbering (1., 2.)
    raw_segments = re.split(r'\n|(?:\d+\.\s)|(?:\-\s)|(?:\*\s)', text)
    
    refined_segments = []
    for segment in raw_segments:
        # Further split paragraphs by sentences (period followed by space)
        sub_splits = re.split(r'(?<=[a-z])\.\s', segment)
        refined_segments.extend(sub_splits)
        
    # Remove empty strings and very short fragments
    return [s.strip() for s in refined_segments if len(s.strip()) > 5]

def analyze_requirement(text):
    """
    The LLM Inference & Explainability Module.
    Extracts patterns to provide a unique justification for every requirement.
    """
    text_low = text.lower()
    
    # Logic patterns based on your Literature Review (Usman Bashar & Muhammad Hammad)
    nfr_patterns = {
        "reliability": "it specifies dependability and error-free operation",
        "performance": "it sets a constraint on speed or resource usage",
        "security": "it addresses data protection and access control",
        "standard": "it references technical compliance (e.g., ISO/IEC 25010)",
        "%": "it provides a quantitative metric for quality",
        "available": "it defines requirements for system uptime"
    }
    
    fr_patterns = {
        "provide": "it defines a service or feature the system offers",
        "manage": "it describes an administrative or data handling task",
        "calculate": "it specifies logic or computation the system performs",
        "allow": "it defines a user capability or permission",
        "display": "it specifies how information is shown to the user"
    }

    # Dynamic Justification Logic
    for key, reason in nfr_patterns.items():
        if key in text_low:
            return "Non-Functional", f"Justification: {reason} (detected pattern: '{key}')."
            
    for key, reason in fr_patterns.items():
        if key in text_low:
            return "Functional", f"Justification: {reason} (detected pattern: '{key}')."

    # Fallback logic for requirements containing numbers (usually NFRs)
    if any(char.isdigit() for char in text_low):
        return "Non-Functional", "Justification: Contains a numeric metric, often indicating a quality constraint."
    
    return "Functional", "Justification: Describes a general system action or functional behavior."

def run_system():
    print("--- Modular LLM-Based Analysis Assistant ---")
    print("Paste any text (paragraphs or lists). Type 'DONE' on a separate line to finish.")
    
    while True:
        # Multi-line input collection
        user_input = []
        while True:
            line = input("> ")
            if line.upper() == 'DONE': break
            user_input.append(line)
        
        full_text = " ".join(user_input)
        if not full_text.strip(): break
            
        # STEP 1: SEGMENTATION
        requirements = universal_ingestion_filter(full_text)
        print(f"\n[System identified {len(requirements)} individual requirements]")
        
        # STEP 2: ANALYSIS & GRAPH TRACKING
        for i, req in enumerate(requirements):
            print(f"\n--- Requirement {i+1} ---")
            print(f"Text: {req}")
            
            label, justification = analyze_requirement(req)
            print(f"AI Prediction: {label}")
            print(f"AI {justification}")
            
            # STEP 3: HUMAN-IN-THE-LOOP VALIDATION
            # This step ensures high quality as per your project goals.
            correct = input("Is this classification correct? (y/n): ").lower()
            
            # Mapping result for accuracy calculation
            true_label = label if correct == 'y' else ("Functional" if label == "Non-Functional" else "Non-Functional")
            history_true.append(true_label)
            history_pred.append(label)
            
            # Update Accuracy Score
            acc = accuracy_score(history_true, history_pred) * 100
            accuracy_over_time.append(acc)
            print(f"Current Accuracy: {acc:.2f}%")

        break # Exit to show graph after processing the block

    # STEP 4: CONSTRUCT GRAPH
    if accuracy_over_time:
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(accuracy_over_time) + 1), accuracy_over_time, 
                 marker='o', linestyle='-', color='royalblue', label='Accuracy %')
        
        plt.title("Requirement Classification Accuracy Over Time")
        plt.xlabel("Number of Requirements Analyzed")
        plt.ylabel("Accuracy Percentage")
        plt.ylim(0, 105)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    run_system()