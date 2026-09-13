import os
import numpy as np
import cohere  # Or your local Ollama / OpenAI client

co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def translate_adaptive(text: str, source_lang: str, target_lang: str):
    # 1. Direct Translation Path
    direct_prompt = f"Translate the following text strictly from {source_lang} to {target_lang}:\n{text}"
    direct_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": direct_prompt}])
    direct_translation = direct_res.message.content[0].text

    # 2. Back-translate for Validation
    back_prompt = f"Translate the following text strictly from {target_lang} to {source_lang}:\n{direct_translation}"
    back_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": back_prompt}])
    back_translation = back_res.message.content[0].text

    # 3. Calculate Embedding Similarity Score
    embeds = co.embed(
        texts=[text, back_translation], 
        model="embed-multilingual-v3.0", 
        input_type="classification"
    ).embeddings.float
    
    similarity_score = cosine_similarity(embeds[0], embeds[1])

    # 4. Fallback/Pivot Routing Condition
    # If meaning loss is high (similarity threshold < 0.82), attempt the Pivot Path via Mandarin
    if similarity_score < 0.82:
        pivot_prompt_1 = f"Translate from {source_lang} to Mandarin Chinese preserving all context and honorific nuances:\n{text}"
        zh_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": pivot_prompt_1}])
        zh_translation = zh_res.message.content[0].text

        pivot_prompt_2 = f"Translate from Mandarin Chinese to {target_lang}:\n{zh_translation}"
        en_res = co.chat(model="command-a-translate", messages=[{"role": "user", "content": pivot_prompt_2}])
        return en_res.message.content[0].text

    return direct_translation

source_text = "안녕하세요, 오늘 날씨가 참 좋네요."
soure_lanng = "Korean"
target_lang = "English"

while True:
    