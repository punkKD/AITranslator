from translator import *

while True:
    source_text = input("Enter text to translate: ")
    source_lang, confidence = detect_language(source_text)
    target_lang = "English"
    print(f"Detected Language: {source_lang} (Confidence: {confidence})\n\n")
    translated_text = translate_adaptive(source_text, source_lang, target_lang) 
    print(f"Translated Text: \n{translated_text}\n\n")   