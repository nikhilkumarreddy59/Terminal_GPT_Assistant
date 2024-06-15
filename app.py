from flask import Flask, render_template, request
from langchain_tools_and_agents import agent_
app = Flask(__name__)

chat_history = []

def get_response_text(input_text):
    # This function generates the response text
    return input_text

@app.route('/', methods=['GET', 'POST'])
def home():
    global chat_history
    if request.method == 'POST':
        user_input = request.form['user_input']
        chat_history.append({'sender': 'user-message', 'text': user_input})
        response_text = agent_(user_input)
        chat_history.append({'sender': 'bot-message', 'text': response_text})
    return render_template('index.html', chat_history=chat_history)


if __name__ == '__main__':
    app.run(debug=True)
