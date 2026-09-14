import os
import numpy as np
import cohere  # Or your local Ollama / OpenAI client

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
metadata_prompt= """

You are an expert literary translator and cultural bridge fluent in both {source_lang} and {target_lang}. Your goal is to translate the text below into English while retaining maximum cultural nuance, social hierarchy, emotional subtext, and implied context.

Follow this exact three-step process:

1. METADATA ANALYSIS: Before translating, identify and list any:
   - Dropped pronouns or subjects and who they actually refer to.
   - Honorifics, speech levels, or registers used, and what they reveal about the relationship/social hierarchy between the speakers.
   - Culturally specific idioms, double meanings, or untranslatable concepts.

2. NUANCED TRANSLATION: Provide the final {target_lang} translation. Prioritize capturing the true tone, emotional weight, and subtext over a rigid literal, word-for-word translation. If a sentence requires extra words in English to convey the original respect or sarcasm, include them naturally.

3. TRANSLATOR'S NOTES: Briefly explain any critical nuances or cultural context that were impossible to fully capture in the {target_lang} text.

CONTEXT OF THE PIECE: {context}

TEXT TO TRANSLATE:{text}
"""

# def cosine_similarity(v1, v2):
#     return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def translate_adaptive(text: str, source_lang: str, target_lang: str, context: str = "General"):
    # 1. Direct Translation Path
    direct_prompt = metadata_prompt.format(source_lang=source_lang, target_lang=target_lang, context=context, text=text)
    direct_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": direct_prompt}])
    print("Direct Translation Response:", direct_res.message.content)
    direct_translation = direct_res.message.content[0].text

    # # 2. Back-translate for Validation
    # back_prompt = f"Translate the following text strictly from {target_lang} to {source_lang}:\n{direct_translation}"
    # back_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": back_prompt}])
    # back_translation = back_res.message.content[0].text

    # # 3. Calculate Embedding Similarity Score
    # embeds = co.embed(
    #     texts=[text, back_translation], 
    #     model="embed-multilingual-v3.0", 
    #     input_type="classification"
    # ).embeddings.float
    
    # similarity_score = cosine_similarity(embeds[0], embeds[1])

    # # 4. Fallback/Pivot Routing Condition
    # # If meaning loss is high (similarity threshold < 0.82), attempt the Pivot Path via Mandarin
    # if similarity_score < 0.82:
    #     print(f"Direct translation similarity score: {similarity_score:.4f} (below threshold, using direct translation)")
    #     pivot_prompt_1 = f"Translate from {source_lang} to Mandarin Chinese preserving all context and honorific nuances:\n{text}"
    #     zh_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": pivot_prompt_1}])
    #     zh_translation = zh_res.message.content[0].text

    #     pivot_prompt_2 = f"Translate from Mandarin Chinese to {target_lang}:\n{zh_translation}"
    #     en_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": pivot_prompt_2}])
    #     return en_res.message.content[0].text
    # else:
    #     print(f"Direct translation similarity score: {similarity_score:.4f} (above threshold, using direct translation)")

    return direct_translation
def detect_language(text: str):
    #prompts sent to the model to detect the language of the input text and provide a confidence score
    prompt = f"Detect the language of the following text and provide a confidence score (list multiple languages if applicable):{text}"

    response = co.chat(model="command-a-translate", messages=[{"role": "user", "content": prompt}])
    detected_language = response.message.content[0].text
    confidence_score = response.message.content[1].text if len(response.message.content) > 1 else "N/A"
    return detected_language,confidence_score

