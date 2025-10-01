import csv
from flask import Flask, request, jsonify, render_template
from trie import AutocompleteTrie
from spellchecker import SpellChecker

app = Flask(__name__)

print("Loading dictionary from CSV and building Trie...")
trie = AutocompleteTrie()
custom_dictionary_words = [] # List to hold our custom words for the spell checker

# Define the column names from your CSV file to match its header
WORD_COLUMN_NAME = 'word'
FREQUENCY_COLUMN_NAME = 'count'

try:
    with open('unigram_freq.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                word = row[WORD_COLUMN_NAME].lower().strip()
                frequency = int(row[FREQUENCY_COLUMN_NAME])
                if word and frequency > 0:
                    trie.insert(word, frequency)
                    custom_dictionary_words.append(word) # Add word to our custom list
            except (KeyError, ValueError, TypeError):
                # Skip any malformed rows in the CSV
                pass
    print("Trie has been successfully built.")

    # --- Initialize Spell Checker ---
    print("Initializing spell checker...")
    spell = SpellChecker()
    # Teach the spell checker all the words from our dictionary
    spell.word_frequency.load_words(custom_dictionary_words)
    print("Spell checker is ready.")

except FileNotFoundError:
    print(f"Error: unigram_freq.csv not found! Please ensure the file is in the correct directory.")
    spell = None # Ensure spell object exists even if file loading fails
    
# --- API Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/search/suggest')
def suggest():
    """Provides autocomplete and spelling correction suggestions."""
    query = request.args.get('q', '').lower()
    if not query or not spell:
        return jsonify({'suggestions': [], 'correction': ''})

    suggestions = trie.suggest(query)
    correction = ""

    # If there are no autocomplete suggestions, check for a spelling mistake
    if not suggestions and query:
        words_in_query = query.split()
        if words_in_query:
            last_word = words_in_query[-1]
            corrected_word = spell.correction(last_word)
            
            # If a correction was found and it's different from the original word
            if corrected_word and corrected_word != last_word:
                corrected_query_parts = words_in_query[:-1] + [corrected_word]
                correction = " ".join(corrected_query_parts)

    return jsonify({'suggestions': suggestions, 'correction': correction})

if __name__ == '__main__':
    app.run(debug=True)