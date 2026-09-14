from textTranslator import *
from imageTranslator import *

while True:
    choice=input("Choose an option:\n1. Translate Text\n2. Translate Image\n3. Exit\nEnter your choice (1, 2, or 3): ")
    if choice == "1":
        # Get user input for text translation
        source_text = input("Enter text to translate: ")
        source_lang, confidence = detect_language(source_text)
        target_lang = "English"
        print(f"Detected Language: {source_lang} (Confidence: {confidence})\n\n")
        translated_text = translate_adaptive(source_text, source_lang, target_lang)
        print(f" \n{translated_text}\n\n")

    elif choice == "2":
        # Get user input for image translation
        image_url = input("Enter the URL of the image to translate: ")
        image_context = input("Enter the context of the text in the image (e.g., signboard, menu, name): ")
        image_location = input("Enter the country or region where the image was taken: ")
        image_purpose = input("Enter the purpose of the translation (e.g., tourist, business, academic research): ")
        identified_text = detect_image(image_url, image_context=image_context, image_location=image_location, image_purpose=image_purpose)
        print(f"Identified Text: \n{identified_text}\n\n")
        source_lang, confidence = detect_language(identified_text)
        target_lang = "English"
        print(f"Detected Language: {source_lang} (Confidence: {confidence})\n\n")
        translated_text = translate_adaptive(identified_text, source_lang, target_lang)
        print(f" \n{translated_text}\n\n")
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")