from enum import Enum


class AiModels(Enum):
    GEMINI_PRO = "Gemini Pro"
    LLAMA = "Llama 3.2:3b"


    def __str__(self):
        return self.value
