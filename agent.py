from openai import AzureOpenAI
import httpx


class AIAgent:
    MODEL_NAME = "gpt-4o-2024-11-20"

    def __init__(self, config):
        self._open_ai_client = AzureOpenAI(
            api_key=config.azure_api_key,
            azure_endpoint=config.azure_endpoint,
            api_version=config.azure_api_version,
            http_client=httpx.Client(verify=False)
        )
        self._temperature = config.temperature
        self._agent_state = [
            {
                "role": "system",
                "content": config.system_prompt
            }
        ]

    def __call__(self, message: str) -> str:
        self._agent_state.append(
            {
                "role": "user", "content": message
            }
        )
        result = self._execute()
        self._agent_state.append(
            {
                "role": "assistant", "content": result
            }
        )
        return result

    def _execute(self) -> str:
        response = self._open_ai_client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=self._agent_state,
            temperature=self._temperature
        )
        return response.choices[0].message.content
