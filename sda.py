def ingest_transcript():
    """
    Takes meeting transcript input at runtime.
    User enters multiple lines and types 'DONE' to finish.
    """
    print("Enter meeting transcript statements (type 'DONE' to finish):\n")

    lines = []
    while True:
        line = input("> ")
        if line.strip().upper() == "DONE":
            break
        if len(line.strip()) > 10:
            lines.append(line.strip())

    return lines


def classify_requirement(text_segment):
    """
    Simulates LLM-based classification of requirements.
    """

    keywords_nfr = ["performance", "secure", "security", "reliable", "fast",
                    "availability", "response time", "scalable"]

    for word in keywords_nfr:
        if word in text_segment.lower():
            return {
                "requirement": text_segment,
                "type": "Non-Functional Requirement",
                "justification": "This requirement describes a system quality or constraint."
            }

    return {
        "requirement": text_segment,
        "type": "Functional Requirement",
        "justification": "This requirement describes a system feature or action."
    }

def explain_requirement(requirement_object):
    """
    Formats requirement with explanation.
    """
    return (
        f"Requirement: {requirement_object['requirement']}\n"
        f"Type: {requirement_object['type']}\n"
        f"Reason: {requirement_object['justification']}\n"
    )


def run_pipeline():
    """
    Runs the full Pipe-and-Filter pipeline.
    """
    print("\nStarting Requirements Analysis Pipeline...\n")

    segments = ingest_transcript()
    results = []

    for segment in segments:
        classified = classify_requirement(segment)
        explained = explain_requirement(classified)
        results.append(explained)

    return results

if __name__ == "__main__":
    output = run_pipeline()

    print("\n--- Analysis Results ---\n")
    for item in output:
        print(item)
        print("-" * 50)
