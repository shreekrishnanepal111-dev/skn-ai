from flask import Flask, render_template_string, request, jsonify
from groq import Groq

app = Flask(__name__)

# Your Groq API Key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

GEMINI_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skn AI</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { display: flex; height: 100vh; background-color: #131314; color: #e3e3e3; }
        .sidebar { width: 260px; background-color: #1e1f20; padding: 16px; display: flex; flex-direction: column; gap: 20px; }
        .new-chat { background-color: #28292a; color: #e3e3e3; border: none; padding: 12px 16px; border-radius: 20px; cursor: pointer; text-align: left; font-weight: 500; font-size: 14px; }
        .new-chat:hover { background-color: #333537; }
        .main-content { flex: 1; display: flex; flex-direction: column; height: 100vh; justify-content: space-between; padding: 20px 0; }
        .header { padding: 0 30px; font-size: 22px; font-weight: bold; color: #a8c7fa; }
        #chat-window { flex: 1; overflow-y: auto; padding: 20px 15%; display: flex; flex-direction: column; gap: 20px; }
        .message { padding: 14px 18px; border-radius: 12px; max-width: 80%; line-height: 1.5; font-size: 15px; }
        .user-msg { background-color: #28292a; align-self: flex-end; color: #e3e3e3; border-bottom-right-radius: 2px; }
        .ai-msg { background-color: transparent; align-self: flex-start; color: #e3e3e3; border-bottom-left-radius: 2px; }
        .input-container { padding: 0 15%; margin-top: 10px; }
        .input-box { display: flex; background-color: #1e1f20; border-radius: 28px; padding: 8px 16px; border: 1px solid #444746; }
        .input-box input { flex: 1; background: transparent; border: none; outline: none; color: white; padding: 10px; font-size: 16px; }
        .input-box button { background-color: #a8c7fa; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; color: #040e25; font-weight: bold; }
        .input-box button:hover { background-color: #7cacf8; }
    </style>
</head>
<body>
    <div class="sidebar">
        <button class="new-chat" onclick="location.reload()">+ New Chat</button>
        <div style="font-size: 12px; color: #8e918f; margin-top: auto;">Skn AI Server • Powered by Groq</div>
    </div>
    
    <div class="main-content">
        <div class="header">Skn AI</div>
        <div id="chat-window">
            <div class="message ai-msg"><b>Skn AI:</b> Hello! How can I help you today?</div>
        </div>
        <div class="input-container">
            <div class="input-box">
                <input type="text" id="user-input" placeholder="Ask Skn AI..." onkeypress="handleKey(event)" />
                <button onclick="sendPrompt()">➔</button>
            </div>
        </div>
    </div>

    <script>
        function handleKey(e) { if (e.key === 'Enter') sendPrompt(); }
        async function sendPrompt() {
            const input = document.getElementById('user-input');
            const window = document.getElementById('chat-window');
            const prompt = input.value.trim();
            if (!prompt) return;

            window.innerHTML += `<div class="message user-msg">${prompt}</div>`;
            input.value = '';
            window.scrollTop = window.scrollHeight;

            const aiDiv = document.createElement('div');
            aiDiv.className = 'message ai-msg';
            aiDiv.innerHTML = '<b>Skn AI:</b> Thinking...';
            window.appendChild(aiDiv);
            window.scrollTop = window.scrollHeight;

            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt })
            });
            const data = await res.json();
            aiDiv.innerHTML = `<b>Skn AI:</b> ${data.response}`;
            window.scrollTop = window.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(GEMINI_UI)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt', '')
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"Error connecting to API: {e}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)