import pandas as pd
import re
import json

# Function to clean lemmas by removing punctuation and diacritics (tashkil)
def clean_lemma(lemma):
    # Remove punctuation and diacritics
    lemma = re.sub(r'[^\w\s]', '', lemma)
    lemma = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', lemma)
    return lemma

# Function to generate BKT parameters based on match category
def get_bkt_parameters(category):
    if category == "Exact Match":
        return (0.75, 0.5, 0.2, 0.1)  # High initial knowledge, easier learning, low guess/slip
    elif category == "Approximate Match":
        return (0.5, 0.3, 0.4, 0.1)  # Moderate knowledge, moderate learning difficulty, moderate guess/slip
    else:  # No Match
        return (0.05, 0.1, 0.5, 0.1)  # Low knowledge, difficult learning, higher guess/slip

# Function to create structured JSON-like output for all categories
def create_combined_bkt_file(categories, output_file):
    # Initialize a list to store structured output
    bkt_data = []

    # Process each category
    for input_file, (category, unit, grade) in categories.items():
        # Load the categorized file
        df = pd.read_excel(input_file)
        
        # Iterate through each row in the DataFrame
        for _, row in df.iterrows():
            darija, arabic = row['Darija'], row['Arabic']
            
            # Clean the Arabic lemma for the key
            cleaned_lemma = clean_lemma(darija)
            
            # Retrieve BKT parameters based on the match category
            p_L0, p_T, p_G, p_S = get_bkt_parameters(category)
            
            # Build the structured data
            bkt_entry = {
                "model": "knowledge.KnowledgeNode",
                "fields": {
                    "name": f"KC_Vocab_{cleaned_lemma}",
                    "description": f"Vocabulary for KC_Vocab_{cleaned_lemma}",
                    "p_L0": p_L0,
                    "p_T": p_T,
                    "p_G": p_G,
                    "p_S": p_S,
                    "baseline": 0.9,
                    "grade": grade,
                    "unit": unit
                }
            }
            bkt_data.append(bkt_entry)
    
    # Write all structured data to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bkt_data, f, ensure_ascii=False, indent=4)
    print(f"Combined file saved: {output_file}")

# Main function to process and save combined output
def process_and_save_combined_file():
    # Define file paths, categories, units, and grades
    categories = {
        "exact_matches_Unit3.xlsx": ("Exact Match", 1, 1),
        "approximate_matches_Unit3.xlsx": ("Approximate Match", 1, 1),
        "no_matches_Unit3.xlsx": ("No Match", 1, 1)
    }
    
    # Combined output file
    output_file = "combined_bkt_data3.json"
    
    # Create the combined file
    create_combined_bkt_file(categories, output_file)
    print(f"Combined file saved: {output_file}")

# Run the function to create a combined file
process_and_save_combined_file()
