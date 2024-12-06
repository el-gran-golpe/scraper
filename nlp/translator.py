from __future__ import annotations

from transformers import pipeline
# For the tokenizer
from transformers import AutoTokenizer
import torch
from loguru import logger
from nlp.config import PIPELINE_PARAMS, MODEL, TASK, INITIAL_TOKEN

TRANSLATOR_WRONG_TAGS = ("City name (optional, probably does not need a translation)",)
MAX_LENGTH = 512
MAX_LENGTH_TO_DIVIDE = 128

class Translator:
    def __init__(self, lang_pair: tuple[str, str]):
        """
        :param lang_pair: A tuple of two strings, the first one is the source language, the second one is the target language
        """
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        if device.type == "cpu":
            logger.warning("The translation will be done in the CPU, this will take a lot of time")
        params = PIPELINE_PARAMS[lang_pair]
        self.tokenizer = AutoTokenizer.from_pretrained(params[MODEL], truncation=True, model_max_length=MAX_LENGTH,
                                                       add_special_tokens=False, use_fast=True)
        # Use the t5-large model for translation
        self.pipeline = pipeline(task=params[TASK], model=params[MODEL], tokenizer=self.tokenizer, framework="pt", device=device)
        self.lang_token = params[INITIAL_TOKEN]
        self._model_name = params[MODEL]

    def translate(self, text: str) -> tuple[str, bool]:
        text = text.split('.') if len(text) > MAX_LENGTH_TO_DIVIDE else [text]
        text = [self.lang_token + sentence.strip() for sentence in text if sentence != ""]
        output = self.pipeline(text)
        output = [self._clean_output(sentence['translation_text']) for sentence in output]
        reliable = not any(cleaned for _, cleaned in output)
        output = '. '.join(sentence for sentence, _ in output)
        return output, reliable

    def _clean_output(self, text: str, return_if_cleaned: bool = True) -> str | tuple[str, bool]:
        """
        Remove the initial token from the output
        """
        cleaned = False
        for tag in TRANSLATOR_WRONG_TAGS:
            if tag in text:
                text, cleaned = text.replace(tag, ""), True
        if return_if_cleaned:
            return text, cleaned
        return text


    def __enter__(self):
        """
        Allows to use the class as a context manager
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Allows to use the class as a context manager
        """
        self.close()

    def close(self):
        """
        Free memory used by the pipeline
        """
        del self.pipeline
        del self.tokenizer
