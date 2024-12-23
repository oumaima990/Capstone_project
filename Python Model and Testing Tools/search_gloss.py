#function to search from gloss :
import json

def search_gloss(word):
    gloss_file_path = r"C:\Users\Oumaima Elmarzouky\Desktop\Capstone\gloss_data.json"

    """
    Searches for a word in the gloss file and displays its details.

    Args:
        word (str): The word to search for.
        gloss_file_path (str): Path to the gloss JSON file.

    Returns:
        dict or None: A dictionary containing the word details if found, None otherwise.
    """
    try:
        # Load the gloss data from the JSON file
        with open(gloss_file_path, 'r', encoding='utf-8') as file:
            gloss_data = json.load(file)
        
        # Search for the word
        word_details = gloss_data.get(word)
        if word_details:
            print(f"Details for '{word}':")
            print(json.dumps(word_details, ensure_ascii=False, indent=4))
            return word_details
        else:
            print(f"Word '{word}' not found in the gloss file.")
            return None

    except FileNotFoundError:
        print(f"Error: File not found at {gloss_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse the gloss file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
