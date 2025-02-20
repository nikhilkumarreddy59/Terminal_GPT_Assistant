from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import ShellTool
from dotenv import load_dotenv
import os

class TerminalAssistant:
    """An intelligent terminal assistant that interprets natural language and executes Linux commands."""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
            
        # Initialize components
        self.llm = self._setup_llm()
        self.tools = self._setup_tools()
        self.agent = self._setup_agent()

    def _setup_llm(self):
        """Initialize the language model."""
        return ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=self.api_key
        )

    def _setup_tools(self):
        """Setup tools including Shell access and other utilities."""
        shell_tool = ShellTool()
        basic_tools = load_tools(["llm-math"], llm=self.llm)  # Add other tools as needed
        return basic_tools + [shell_tool]

    def _setup_agent(self):
        """Initialize the agent with tools and the language model."""
        return initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True,
            agent_kwargs={
                'system_message': """You are an intelligent terminal assistant designed to help users interact with their Linux system.
                Your primary functions are:
                1. Interpret natural language requests into Linux commands
                2. Execute system operations safely
                3. Provide clear explanations of what commands do
                4. Handle system tasks and file operations
                
                Always explain what you're doing and why. If a command might be destructive,
                warn the user first and ask for confirmation."""
            }
        )

    def process_command(self, user_input: str) -> str:
        """Process a natural language command and return the result."""
        try:
            # Execute the command through the agent
            response = self.agent(user_input)
            return response['output']
        except Exception as e:
            return f"Error processing command: {str(e)}"

    def execute_shell_command(self, command: str) -> str:
        """Directly execute a shell command with safety checks."""
        dangerous_commands = ['rm -rf', 'mkfs', 'dd', '> /dev']
        
        # Check for dangerous commands
        if any(cmd in command for cmd in dangerous_commands):
            return "⚠️ This command could be destructive. Please review and confirm."
            
        try:
            shell_tool = ShellTool()
            return shell_tool.run(command)
        except Exception as e:
            return f"Error executing command: {str(e)}" 