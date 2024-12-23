import pandas as pd
from difflib import SequenceMatcher
from docx import Document
import re

# Threshold for approximate match
APPROXIMATE_MATCH_THRESHOLD = 0.6

# Function to remove punctuation and tashkil (Arabic diacritics) from words
def remove_punctuation_and_tashkil(word):
    word = re.sub(r'[^\w\s]', '', word)  # Remove punctuation
    word = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', word)  # Remove Arabic diacritics (Tashkil)
    return word

# Function to categorize matches
def categorize_match(darija, arabic):
    darija_clean = remove_punctuation_and_tashkil(darija)
    arabic_clean = remove_punctuation_and_tashkil(arabic)
    
    # Check for exact match
    if darija_clean == arabic_clean:
        return "Exact Match"
    
    # Check for approximate match
    similarity = SequenceMatcher(None, darija_clean, arabic_clean).ratio()
    if similarity >= APPROXIMATE_MATCH_THRESHOLD:
        return "Approximate Match"
    
    # Default to no match
    return "No Match"

# Function to process document and save results
def process_and_save(doc_path):
    exact_matches = []
    approximate_matches = []
    no_matches = []
    
    unique_pairs = set()  # To ensure no duplicate entries
    
    # Open the Word document and read lines
    doc = Document(doc_path)
    for para in doc.paragraphs:
        line = para.text.strip()
        if not line:  # Skip empty lines
            continue
        
        # Split line into Darija and Arabic, assuming they are separated by a hyphen or space
        if " - " in line:
            darija, arabic = map(str.strip, line.split(" - "))
        elif "   " in line:  # Handle pairs separated by triple spaces
            parts = line.split("   ")
            if len(parts) == 2:
                darija, arabic = map(str.strip, parts)
            else:
                continue  # Skip malformed lines
        else:
            continue  # Skip lines that do not match expected patterns
        
        # Avoid processing duplicates
        pair = (darija, arabic)
        if pair in unique_pairs:
            continue
        unique_pairs.add(pair)
        
        # Categorize the match
        category = categorize_match(darija, arabic)
        if category == "Exact Match":
            exact_matches.append((darija, arabic))
        elif category == "Approximate Match":
            approximate_matches.append((darija, arabic))
        else:
            no_matches.append((darija, arabic))
    
    # Convert results to DataFrames
    exact_df = pd.DataFrame(exact_matches, columns=["Darija", "Arabic"])
    approximate_df = pd.DataFrame(approximate_matches, columns=["Darija", "Arabic"])
    no_match_df = pd.DataFrame(no_matches, columns=["Darija", "Arabic"])
    
    # Save to Excel files
    exact_df.to_excel("exact_matches_Unit3.xlsx", index=False)
    approximate_df.to_excel("approximate_matches_Unit3.xlsx", index=False)
    no_match_df.to_excel("no_matches_Unit3.xlsx", index=False)

# Specify the path to your document
process_and_save(r"C:\Users\Oumaima Elmarzouky\Desktop\Capstone\unit 3.docx")

print("Files saved: 'exact_matches_Unit6.xlsx', 'approximate_matches_Unit6.xlsx', 'no_matches_Unit6.xlsx'")
