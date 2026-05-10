import re

def clean_aozora_text(text):
    text = re.sub(r'《[^》]*》', '', text)     
    text = re.sub(r'［＃[^］]*］', '', text)    
    text = text.replace('｜', '')             
    return text

with open("text_ja.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

cleaned_text = clean_aozora_text(raw_text)

with open("clean_text_ja.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_text)

print("Cleaned Japanese text saved as clean_text_ja.txt")