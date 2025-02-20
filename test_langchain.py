import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI

def test_langchain():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    print(f"API Key first 10 chars: {api_key[:10] if api_key else 'None'}")
    
    try:
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=api_key
        )
        
        # Try a simple completion
        response = llm.predict("Say 'Hello, testing!'")
        
        print("LangChain Test successful!")
        print("Response:", response)
        return True
        
    except Exception as e:
        print("LangChain Test failed!")
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    test_langchain() 