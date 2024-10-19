from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Replace with your actual Google API key
API_KEY = "AIzaSyDHacLIUHyOYjz7tRUvYAhSkCl_V22t4M0"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

def get_palm_response(query):
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [{"parts": [{"text": query}]}]
    }
    
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    
    # Log the full response for debugging
    print("Full API Response:", response.text)
    
    if response.status_code == 200:
        try:
            # Parse the response JSON
            json_response = response.json()
            
            # Check if 'candidates' key exists and extract the content from it
            if 'candidates' in json_response:
                content = json_response['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                
                if parts and 'text' in parts[0]:
                    return parts[0]['text']
            
            return "No valid response from PaLM API."
        except json.JSONDecodeError:
            return "Error parsing the response JSON."
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_query():
    user_input = request.form['query']
    print(type(user_input))
    law_response = get_palm_response(user_input+"Please analyze the user's query. If the question is related to genuine legal matters under Indian law, provide a detailed response citing relevant laws, sections, and possible solutions. If the query is irrelevant, unrelated to Indian law, or offensive, do not provide any response and ignore the query. Limit your response to 1000 words. ")

    return jsonify({'response': law_response})

if __name__ == '__main__':
    app.run(debug=True)
