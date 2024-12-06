from transformers import pipeline
# For the tokenizer
from transformers import AutoTokenizer
import torch
from loguru import logger


MAX_LENGTH = 512

class LanguageDetector:
    def __init__(self, model="eleldar/language-detection"):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        if device.type == "cpu":
            logger.warning("The translation will be done in the CPU, this will take a lot of time")
        self.tokenizer = AutoTokenizer.from_pretrained(model, model_max_length=MAX_LENGTH)
        # Use the t5-large model for translation
        self.pipeline = pipeline(task="text-classification", model=model, tokenizer=self.tokenizer, framework="pt", device=device)

    def detect_lang(self, text: str) -> str:
        output = self.pipeline(text)
        assert len(output) == 1, f"The output should have only one element, but it has {len(output)}"
        return output[0]['label']

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
