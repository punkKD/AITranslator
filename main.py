from translator import *

source_text = input("Enter text to translate: ")
source_lang, confidence = detect_language(source_text)
target_lang = "English"
translated_text = translate_adaptive(source_text, source_lang, target_lang) 
print(f"Detected Language: {source_lang} (Confidence: {confidence})")
print(f"Translated Text: {translated_text}")   