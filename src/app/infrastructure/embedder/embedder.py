from app.usecases import interfaces

import torch
from transformers import DistilBertModel, DistilBertTokenizer


class Embedder(interfaces.embedder.Embedder):
    def __init__(self, model_path: str, device: str):
        self._model = DistilBertModel.from_pretrained(model_path).to(device)
        self._tokenizer = DistilBertTokenizer.from_pretrained(model_path)

    def get_embedding(self, text: str) -> list[float]:
        inputs = self._tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        with torch.no_grad():
            outputs = self._model(**inputs)
        return outputs.last_hidden_state[:, 0, :].squeeze().tolist()
