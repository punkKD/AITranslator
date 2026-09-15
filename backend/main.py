from typing import Optional, Union
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from functions.textTranslator import *
from functions.imageTextGrabber import *


app = FastAPI(title="KD Translate APP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextTranslateRequest(BaseModel):
    source_text: str
    source_lang: Optional[str] = "auto"
    target_lang: str = "English"


class TextTranslateResponse(BaseModel):
    detected_lang: str
    confidence: str
    translated_text: str


class ImageTranslateRequest(BaseModel):
    image_url: str
    image_context: str
    image_location: str
    image_purpose: str
    target_lang: str = "English"


class ImageTranslateResponse(BaseModel):
    identified_text: str
    detected_lang: str
    confidence: str
    translated_text: str


@app.post("/translate/text", response_model=TextTranslateResponse)
def translate_text(req: TextTranslateRequest)-> TextTranslateResponse:
    try:
        source_lang, confidence = detect_language(req.source_text)
        translated_text = translate_adaptive(req.source_text, source_lang, req.target_lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return TextTranslateResponse(
        detected_lang=source_lang,
        confidence=confidence,
        translated_text=translated_text,
    )


@app.post("/translate/image", response_model=ImageTranslateResponse)
def translate_image(req: ImageTranslateRequest)-> ImageTranslateResponse:
    try:
        identified_text = detect_image(
            req.image_url,
            image_context=req.image_context,
            image_location=req.image_location,
            image_purpose=req.image_purpose,
        )
        source_lang, confidence = detect_language(identified_text)
        translated_text = translate_adaptive(identified_text, source_lang, req.target_lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ImageTranslateResponse(
        identified_text=identified_text,
        detected_lang=source_lang,
        confidence=confidence,
        translated_text=translated_text,
    )

@app.get("/translate/health")
def health() -> dict:
    return {"status": "ok"}

# Serve the built Vue frontend once `npm run build` has produced frontend/dist.
# This lets one container serve both the API and the UI in production.
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(frontend_dist):
    print(f"Serving frontend from {frontend_dist}")
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")