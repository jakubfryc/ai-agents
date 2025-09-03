import re
from typing import Callable

from tavily import TavilyClient


class AgentTools:
    def __init__(self, config):
        self._config = config
        self._agent_tools = {
            'calculate': self._calculate,
            'cats_weight': self._cats_weight_information,
            'get_knowledge': self._get_knowledge
        }

    def get_tool(self, tool_name) -> Callable:
        return self._agent_tools.get(tool_name)

    def _calculate(self, expression: str) -> str:
        if not re.fullmatch(r'[\d\s\+\-\*\/\.\(\)]+', expression):
            return "Only mathematical operations are allowed."
        return eval(expression)

    def _cats_weight_information(self, cat_type: str) -> str:
        if cat_type == 'barry':
            return '20kg'
        elif cat_type == 'harry':
            return '40kg'
        elif cat_type == 'garry':
            return '10kg'
        else:
            return 'average cat weight is 5 kg'

    def _get_knowledge(self, question: str) -> str:
        tavily_client = TavilyClient(api_key=self._config.tavily_api_key)
        return tavily_client.search(question).get('results')[0]['content']
