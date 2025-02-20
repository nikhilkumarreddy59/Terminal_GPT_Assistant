from flask import Flask, request, jsonify, render_template
from terminal_assistant import TerminalAssistant
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the terminal assistant
assistant = TerminalAssistant()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def process_command():
    try:
        data = request.json
        user_input = data.get('command', '')
        
        if not user_input:
            return jsonify({'error': 'No command provided'}), 400
            
        logger.info(f"Processing command: {user_input}")
        response = assistant.process_command(user_input)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
