from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)


def analyze_mental_health(user_input):
    prompt = f"""
    You are a mental health AI assistant for veterans called althea. AI.
    Your goal is to analyze the following user input and detect their stress level.
    Then, suggest relaxation techniques or crisis support if needed.

    User Input: "{user_input}"
  Classify the stress level as:
    - Low (No intervention needed, provide motivational response)
    - Moderate (Suggest stress-relief exercises like meditation)
    - High (Encourage seeking professional help, provide emergency helpline)

user: "{user_input}"
Provide a friendly and supportive response.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 for better responses
        messages=[{"role": "system", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"response": "Please type a message."})

    ai_response = get_vetmind_response(user_input)
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)
    
print("Welcome to Althea AI – Your Mental Health Companion for Veterans 🥇🩷")
while True:
    user_text = input("\n📝 How are you feeling today? (Type 'exit' to quit): ")
    
    if user_text.lower() == "exit":
        print("\n💙 Take care! Althea AI is always here for you. 💙")
        break
ai_response = analyze_mental_health(user_text)
print("\n🤖 VetMind AI: ", ai_response)
