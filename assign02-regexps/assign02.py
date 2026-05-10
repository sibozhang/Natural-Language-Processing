import re
import jieba
from janome.tokenizer import Tokenizer
import logging

jieba.setLogLevel(logging.INFO)

def match_initial_letter(text, char):
    pattern = rf'\b[{char}]\w*'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    output_format(matches, match_initial_letter.__name__)

def match_suffix(text, suffix):
    pattern = rf'\b\w*{suffix}\b'
    matches = re.findall(pattern, text)
    output_format(matches, match_suffix.__name__)

def match_bigrams(text, bigram):
    pattern = rf'\b\w*{bigram}\w*\b'
    matches = re.findall(pattern, text)
    output_format(matches, match_bigrams.__name__)

def find_identical_bigrams(text):
    pattern = r'\b(\w+)\s+\1\b'
    matches = re.findall(pattern, text)
    output_format(matches, find_identical_bigrams.__name__)

def filter_digit_to_word_lines(text):
    pattern = r'^\d.*[a-zA-Z]$'
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    output_format(matches, filter_digit_to_word_lines.__name__)

def parse_percentages(text):
    pattern = r'\b\d+(?:\.\d+)?%'
    matches = re.findall(pattern, text)
    output_format(matches, parse_percentages.__name__)

def output_format(matches, name):
    unique_matches = set(matches)
    print('----------\n'+name)
    print(f"Found {len(matches)} total matches ({len(unique_matches)} unique).")
    print(f"Top 20 results: {list(unique_matches)[:20]}")

def get_user_inputs(lang):
    print(f"\n--- Currently Processing: {lang.upper()} Text ---")
    while True:
        try:
            prompt_msg = "\nEnter [Start-Character] [End-Character] [Consecutive-Pair] (separated by spaces): "
            raw_input = input(prompt_msg).strip()

            if '，' in raw_input or ',' in raw_input or '、' in raw_input:
                raise ValueError("Comma detected! Please use only spaces as separators.")

            parts = raw_input.split()
            if len(parts) != 3:
                raise ValueError(f"Expected 3 parameters, but received {len(parts)}.")
            
            char, suffix, bigram = parts

            if not char.isalpha() or len(char) != 1:
                raise ValueError(f"'{char}' is not a valid character.")
            
            if not suffix.isalpha():
                raise ValueError(f"'{suffix}' is not a valid suffix.")
                
            if not bigram.isalpha() or len(bigram) != 2:
                raise ValueError(f"'{bigram}' is not a valid consecutive pair.")

            return char, suffix, bigram

        except ValueError as e:
            print(f"Invalid Input: {e}")
            print("Please try again. Example: a ly th")

def get_language_choice():
    while True:
        choice = input("Select language to process (en/zh/ja): ").strip().lower()
        if choice in ['en', 'zh', 'ja']:
            return choice
        print("Error: Invalid selection. Please choose 'en', 'zh', or 'ja'.")

def main():
    lang = get_language_choice()
    file_dict = {
        'en': 'text_en.txt',
        'zh': 'text_zh.txt',
        'ja': 'text_ja.txt'
    }

    file_path = file_dict[lang]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    if lang == 'en':
        processed_text = raw_text
    elif lang == 'zh':
        processed_text = " ".join(jieba.lcut(raw_text))
    elif lang == 'ja':
        t = Tokenizer()
        processed_text = " ".join([token.surface for token in t.tokenize(raw_text)])
    print(f"\n Successfully processed {file_path}")

    char, suffix, bigram = get_user_inputs(lang)

    match_initial_letter(processed_text,char)
    match_suffix(processed_text,suffix)
    match_bigrams(processed_text, bigram)
    find_identical_bigrams(processed_text)
    filter_digit_to_word_lines(processed_text)
    parse_percentages(processed_text)


if __name__ == "__main__":
    main()


