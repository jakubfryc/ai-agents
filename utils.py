import os
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import dotenv


prompts_dir = Path("prompts")


def load_prompt(file_path):
    try:
        with open(prompts_dir / file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        for root, dirs, files in os.walk("/"):
            for file in files:
                if file == "main.md":
                    raise ValueError(f"path wrong {os.path.join(root, file)} found instead of {prompts_dir}")


@dataclass
class AIAgentConfig:
    azure_api_key: str
    azure_api_version: str
    azure_endpoint: str
    tavily_api_key: str
    system_prompt: str
    temperature: float = 0

    @classmethod
    def load_from_local(cls, prompt_name_file: str):
        dotenv.load_dotenv(".env", override=True)
        return cls(
            azure_api_key=os.environ['AZURE_OPENAI_API_KEY'],
            azure_api_version=os.environ['AZURE_OPENAI_API_VERSION'],
            azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
            tavily_api_key=os.environ['TAVILY_API_KEY'],
            system_prompt=load_prompt(prompt_name_file)
        )


class ActionParser:
    def __init__(self):
        self._action_re = re.compile(r'^Action: (\w+): (.*)$')

    def __call__(self, text) -> tuple[str] | Any:
        actions = [
            self._action_re.match(line)
            for line in text.split('\n')
            if self._action_re.match(line)
        ]
        if actions:
            return [a.groups() for a in actions if a][0]
        return None, None
