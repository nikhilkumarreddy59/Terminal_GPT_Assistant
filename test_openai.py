import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

def verify_api_key():
    """Verify that the API key exists and is properly formatted"""
    # Find and load the .env file
    env_path = find_dotenv()
    if not env_path:
        print("❌ Error: No .env file found")
        return None
    
    print(f"✓ Found .env file at: {env_path}")
    load_dotenv(env_path)
    
    # Get and verify API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        return None
    
    if not api_key.startswith('sk-'):
        print("❌ Error: API key doesn't start with 'sk-'. This may be invalid.")
        return None
    
    print("✓ API key found and properly formatted")
    print(f"  Length: {len(api_key)} characters")
    print(f"  Prefix: {api_key[:7]}...")
    return api_key

def test_openai_connection(api_key):
    """Test the OpenAI API connection with a simple request"""
    if not api_key:
        return False
        
    try:
        print("\nTesting OpenAI API connection...")
        client = OpenAI(api_key=api_key)
        
        # Simple test message
        messages = [
            {"role": "system", "content": "You are a test assistant. Respond with 'Test successful!'"},
            {"role": "user", "content": "Run test"}
        ]
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=20
        )
        
        # Verify response
        if response and response.choices:
            print("✓ API connection successful!")
            print(f"Response: {response.choices[0].message.content}")
            return True
            
    except Exception as e:
        print("❌ API connection failed!")
        print(f"Error: {str(e)}")
        
        # Additional debugging info
        if "invalid_api_key" in str(e):
            print("\nTroubleshooting tips:")
            print("1. Check if the API key in .env is correct")
            print("2. Make sure there are no quotes or spaces in the .env file")
            print("3. The .env file should look exactly like this:")
            print("OPENAI_API_KEY=sk-your-key-here")
            
    return False

def main():
    """Main test function"""
    print("=== OpenAI API Connection Test ===\n")
    
    # Step 1: Verify API key
    api_key = verify_api_key()
    if not api_key:
        print("\n❌ API key verification failed. Please check your .env file.")
        return
        
    # Step 2: Test API connection
    success = test_openai_connection(api_key)
    
    # Final result
    print("\n=== Test Results ===")
    if success:
        print("✓ All tests passed successfully!")
    else:
        print("❌ Tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 