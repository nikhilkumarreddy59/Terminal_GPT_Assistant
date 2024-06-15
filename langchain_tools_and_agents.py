from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI
import os
import openai

from langchain_openai import ChatOpenAI  # For interacting with OpenAI's LLMs
from langchain_core.prompts import ChatPromptTemplate  # For crafting prompts
from langchain_core.output_parsers import StrOutputParser  # For parsing LLM responses (optional)

from langchain_community.tools import ShellTool
openai.api_key = os.getenv("OPENAI_API_KEY_2")
llm_model = "gpt-3.5-turbo"

llm = ChatOpenAI(temperature=0, model=llm_model,openai_api_key=openai.api_key)
tools = load_tools(["llm-math", "wikipedia"], llm=llm)



shell_tool = ShellTool()


def agent_(input):
    agent = initialize_agent(
        tools + [shell_tool],
        llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True)
    return agent(input)['output']
