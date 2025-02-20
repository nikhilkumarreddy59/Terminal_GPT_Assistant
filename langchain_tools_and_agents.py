import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import ShellTool

class LanguageAgent:
    def __init__(self):
        # Load environment variables
        env_path = find_dotenv()
        print(f"Found .env file at: {env_path}")
        load_dotenv(env_path)
        
        # Get API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("No OpenAI API key found in environment variables")
        
        print(f"API Key length: {len(self.api_key)}")
        print(f"API Key first 10 chars: {self.api_key[:10]}")
        
        # Initialize components
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()
    
    def _setup_llm(self):
        return ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=self.api_key
        )
    
    def _setup_tools(self):
        basic_tools = load_tools(["llm-math", "wikipedia"], llm=self.llm)
        shell_tool = ShellTool()
        return basic_tools + [shell_tool]
    
    def _setup_agent(self):
        return initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True
        )
    
    def process_input(self, user_input):
        try:
            return self.agent(user_input)['output']
        except Exception as e:
            return f"Error processing input: {str(e)}"

# Function to maintain compatibility with existing code
def agent_(input):
    agent = LanguageAgent()
    return agent.process_input(input)

# Test the agent if run directly
if __name__ == "__main__":
    agent = LanguageAgent()
    response = agent.process_input("What is 2 + 2?")
    print("Response:", response)
