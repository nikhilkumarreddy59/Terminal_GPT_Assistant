import argparse
from terminal_assistant import TerminalAssistant
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Intelligent Terminal Assistant - Execute natural language commands in Linux"
    )
    parser.add_argument(
        'command',
        nargs='*',
        help="The natural language command to execute"
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help="Run in interactive mode"
    )

    args = parser.parse_args()
    assistant = TerminalAssistant()

    if args.interactive:
        print("🤖 Terminal Assistant - Interactive Mode")
        print("Type 'exit' or 'quit' to end the session")
        
        while True:
            try:
                command = input("\n💻 > ")
                if command.lower() in ['exit', 'quit']:
                    break
                    
                response = assistant.process_command(command)
                print(f"\n🤖 {response}")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
    
    elif args.command:
        command = ' '.join(args.command)
        response = assistant.process_command(command)
        print(response)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 