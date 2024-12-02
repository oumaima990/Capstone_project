import re

# Define BayesianKnowledgeTracing class for Knowledge Components (KCs)
class BayesianKnowledgeTracing:
    def __init__(self, prior, learn, forget, guess, baseline=0.9):
        self.prior = prior
        self.learn = learn
        self.forget = forget
        self.guess = guess
        self.baseline = baseline
        self.value = prior

# File path to the Arabic data text file
file_path = r"C:\Users\Oumaima Elmarzouky\Desktop\cavalli\Annotated\cavalli\madamira\madamira\SampleTextInput.txt.mada"

# Define regex patterns for extracting attributes
word_pattern = re.compile(r';;WORD (.+)')
case_pattern = re.compile(r'cas:(\w+)')
pos_pattern = re.compile(r'pos:(\w+)')
gender_pattern = re.compile(r'gen:(\w+)')
mood_pattern = re.compile(r'mod:(\w+)')
definiteness_pattern = re.compile(r'stt:(\w+)')

# Function to infer dependencies based on morph_data
def infer_dependencies(morph_data):
    # Define dependencies for each KC as BayesianKnowledgeTracing instances
    dependencies = {
        "KC_Grammar_Noun": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Verb": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Adjective": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Preposition": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Pronoun": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Punctuation": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Case_Nominative": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Case_Accusative": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Case_Genitive": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Mood_Indicative": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Mood_Subjunctive": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Grammar_Mood_Jussive": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Masculine": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Feminine": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Definiteness_Definite": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
        "KC_Definiteness_Indefinite": BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1),
    }




    # Extract attributes from morph_data
    case = morph_data.get("Case")
    pos = morph_data.get("Pos")
    gender = morph_data.get("Gender")
    mood = morph_data.get("Mood")
    definiteness = morph_data.get("Definiteness")

    # Link pos (part-of-speech) to KCs
    if pos == 'noun':
        dependencies["KC_Grammar_Noun"].value += 0.05
    elif pos == 'verb':
        dependencies["KC_Grammar_Verb"].value += 0.05
    elif pos == 'adj':
        dependencies["KC_Grammar_Adjective"].value += 0.05
    elif pos == 'prep':
        dependencies["KC_Grammar_Preposition"].value += 0.05
    elif pos in ('pron', 'poss'):
        dependencies["KC_Grammar_Pronoun"].value += 0.05
    elif pos == 'punc':
        dependencies["KC_Grammar_Punctuation"].value += 0.02

    # Link case (grammatical case) to KCs
    if case == 'n':
        dependencies["KC_Grammar_Case_Nominative"].value += 0.05
    elif case == 'a':
        dependencies["KC_Grammar_Case_Accusative"].value += 0.05
    elif case == 'g':
        dependencies["KC_Grammar_Case_Genitive"].value += 0.05

    # Link gender to KCs
    if gender == 'm':
        dependencies["KC_Masculine"].value += 0.05
    elif gender == 'f':
        dependencies["KC_Feminine"].value += 0.05

    # Link mood to KCs
    if mood == 'i':
        dependencies["KC_Grammar_Mood_Indicative"].value += 0.05
    elif mood == 's':
        dependencies["KC_Grammar_Mood_Subjunctive"].value += 0.05
    elif mood == 'j':
        dependencies["KC_Grammar_Mood_Jussive"].value += 0.05

    # Link definiteness to KCs
    if definiteness == 'd':  # Definite
        dependencies["KC_Definiteness_Definite"].value += 0.05
    elif definiteness == 'i':  # Indefinite
        dependencies["KC_Definiteness_Indefinite"].value += 0.05

    # Return dependencies where value exceeds prior
    inferred_dependencies = {k: v.value for k, v in dependencies.items() if v.value > v.prior}
    return inferred_dependencies

# Read the file and process each word block
output = {}
with open(file_path, 'r', encoding='utf-8') as file:
    block = {}
    for line in file:
        # Check if it's the start of a new word block
        word_match = word_pattern.search(line)
        if word_match:
            # Save the previous block if it exists and infer dependencies
            if block:
                dependencies = infer_dependencies(block)
                output[f"KC_Vocab_{block['Word']}"] = dependencies
            # Start a new block with the word
            block = {'Word': word_match.group(1)}
        
        # Extract Case, Pos, Gender, Mood, and Definiteness
        case_match = case_pattern.search(line)
        if case_match:
            block['Case'] = case_match.group(1)
        
        pos_match = pos_pattern.search(line)
        if pos_match:
            block['Pos'] = pos_match.group(1)
        
        gender_match = gender_pattern.search(line)
        if gender_match:
            block['Gender'] = gender_match.group(1)
        
        mood_match = mood_pattern.search(line)
        if mood_match:
            block['Mood'] = mood_match.group(1)
        
        definiteness_match = definiteness_pattern.search(line)
        if definiteness_match:
            block['Definiteness'] = definiteness_match.group(1)

    # Append the last block
    if block:
        dependencies = infer_dependencies(block)
        output[f"KC_Vocab_{block['Word']}"] = dependencies

# Display the final output
for word, dependencies in output.items():
    print(f"{word}: {dependencies}")
