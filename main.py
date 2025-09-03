from agent import AIAgent
from agent_tools import AgentTools
from utils import AIAgentConfig, ActionParser


def run_agent_loop(
        prompt: str,
        ai_agent: AIAgent,
        ai_agent_tools: AgentTools,
        action_parser: ActionParser,
        max_turns=5
):
    for _ in range(max_turns):
        print(prompt)
        result = ai_agent(prompt)
        print(result)
        action, action_input = action_parser(result)
        if not action:
            break
        ai_tool = ai_agent_tools.get_tool(action.lower().strip())
        if ai_tool:
            action_result = ai_tool(action_input.lower().strip())
        else:
            action_result = 'Unknown tool'
        prompt = f"Observation: {action_result}"


if __name__ == '__main__':
    config = AIAgentConfig.load_from_local(prompt_name_file="system_new.md")
    run_agent_loop(
        prompt=input("Q: "),
        ai_agent=AIAgent(config=config),
        ai_agent_tools=AgentTools(config=config),
        action_parser=ActionParser()
    )
