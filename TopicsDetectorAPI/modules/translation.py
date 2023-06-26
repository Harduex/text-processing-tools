from typing import Optional
from transformers import AutoTokenizer, MarianMTModel

class TranslationModel:
    _instance: Optional[MarianMTModel] = None

    @classmethod
    def get_instance(cls, source_language: str, target_language: str) -> MarianMTModel:
        if cls._instance is None:
            model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
            cls._instance = MarianMTModel.from_pretrained(model_name)
        return cls._instance

    @classmethod
    def get_tokenizer(cls, source_language: str, target_language: str) -> AutoTokenizer:
        model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
        return AutoTokenizer.from_pretrained(model_name)


def translate(text, source_language="bg", target_language="en"):
    model = TranslationModel.get_instance(source_language, target_language)
    tokenizer = TranslationModel.get_tokenizer(source_language, target_language)
    batch = tokenizer([text], return_tensors="pt")
    generated_ids = model.generate(**batch)
    translated_text = tokenizer.batch_decode(
        generated_ids, skip_special_tokens=True)[0]
    return translated_text

