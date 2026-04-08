"""Avalai/OpenAI client helpers used by dataset generators."""

import os

import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()


class AvalaiClient:
    """Small wrapper for chat and embedding clients."""

    def __init__(self, api_key: str = "", base_url: str = "", model_name: str = "gpt-4o-mini"):
        self.api_key, self.base_url = self._set_api_config(api_key, base_url)
        self.model_name = model_name
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def get_chat_model(self):
        return ChatOpenAI(
            model_name=self.model_name,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url,
        )

    def get_embeddings(self):
        return OpenAIEmbeddings(openai_api_key=self.api_key, openai_api_base=self.base_url)

    def _set_api_config(self, api_key, base_url):
        default_api_key = os.environ.get("AVALAI_API_KEY")
        default_base_url = os.environ.get("AVALAI_BASE_URL", "https://api.avalai.ir/v1")
        return api_key or default_api_key, base_url or default_base_url
