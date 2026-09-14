import os
import numpy as np
import cohere  # Or your local Ollama / OpenAI client

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
metadata_prompt= """

You are an expert literary translator and cultural bridge fluent in both {source_lang} and {target_lang}. Your goal is to translate the text below into English while retaining maximum cultural nuance, social hierarchy, emotional subtext, and implied context.
Follow this exact three-step process:

Follow this exact three-step process:

1. METADATA ANALYSIS: Before translating, identify and list any:
   - Dropped pronouns or subjects and who they actually refer to.
   - Honorifics, speech levels, or registers used, and what they reveal about the relationship/social hierarchy between the speakers.
   - Culturally specific idioms, double meanings, or untranslatable concepts.

2. NUANCED TRANSLATION: Provide the final {target_lang} translation. Prioritize capturing the true tone, emotional weight, 
and subtext over a rigid literal, word-for-word translation. If a sentence requires extra words in English to convey the 
original respect or sarcasm, include them naturally.

3. TRANSLATOR'S NOTES: Briefly explain any critical nuances or cultural context that were impossible to fully capture 
in the {target_lang} text.\n

CONTEXT OF THE PIECE: {context}

TEXT TO TRANSLATE:{text}

Things to note: 
if a year is mentioned, translate it into the English format (e.g., 23년 → 2023).
Only output the final translation and any necessary translator's notes.
Do not include any headings or anything in this prompt in your final translation. 
"""



def translate_adaptive(text: str, source_lang: str, target_lang: str, context: str = "General"):
    direct_prompt = metadata_prompt.format(source_lang=source_lang, target_lang=target_lang, context=context, text=text)
    direct_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": direct_prompt}])
    direct_translation = direct_res.message.content[0].text

    return direct_translation
def detect_language(text: str):
    #prompts sent to the model to detect the language of the input text and provide a confidence score
    prompt = f"Detect the language of the following text and provide a confidence score (list multiple languages if applicable):{text}"

    response = co.chat(model="command-a-translate", messages=[{"role": "user", "content": prompt}])
    detected_language = response.message.content[0].text
    confidence_score = response.message.content[1].text if len(response.message.content) > 1 else "N/A"
    return detected_language,confidence_score

