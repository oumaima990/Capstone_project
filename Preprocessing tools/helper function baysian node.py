import re

def create_bayesian_nodes(file_path):
    node_lemmas = []
    node_form_txt = []
    with open(file_path, "r", encoding="utf-8") as file:
        word_form = ""
        lemma = ""
        lex_count = 0  # To keep track of lex occurrences per word entry

        for line in file:
            if line.startswith(";;WORD "):
                word_form = line.split(";;WORD ")[-1].strip()
                lex_count = 0  # Reset for each new word

            if "lex:" in line:
                lex_count += 1
                # Only consider the second lex occurrence
                if lex_count == 2:
                    lemma = re.search(r"lex:(\S+)", line).group(1)
                    # Remove any trailing underscore followed by numbers
                    cleaned_lemma = re.sub(r"_[0-9]+$", "", lemma)
                    
                        # Add nodes with word form and cleaned lemma
                    node_form = f"KC_Vocab_{word_form}: BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1, baseline=0.9)"
                    #node_lemma = f"KC_Vocab_{cleaned_lemma}: BayesianKnowledgeTracing(0.3, 0.1, 0.2, 0.1, baseline=0.9)"
                    node_lemma = f"{cleaned_lemma}"

                    node_form_txt.append(node_form)
                    node_lemmas.append(node_lemma)

    return node_lemmas,node_form_txt

# Example usage
file_path = r"C:\Users\Oumaima Elmarzouky\Desktop\cavalli\Annotated\cavalli\madamira\madamira\SampleTextInput.txt.mada"
node_lemmas,node_form_txt = create_bayesian_nodes(file_path)
print("surface forme")
#for node in node_form_txt:
    #print(node)
#print("----------------------")
print("")
print("lemmas forms")
for node in node_lemmas:
    print(node)
