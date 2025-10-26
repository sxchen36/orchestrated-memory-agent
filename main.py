"""
Main entry point for the AI Companion Agent
"""
from agent import CompanionAgent
import os
from dotenv import load_dotenv


def main():
    """Main function to run the agent"""
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        print("📝 Copy .env.example to .env and add your API key")
        return
    
    # Initialize the agent
    print("🚀 Initializing AI Companion...")
    agent = CompanionAgent()
    
    print("🤖 AI Companion is ready!")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        try:
            response = agent.run(user_input)
            print(f"Agent: {response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
