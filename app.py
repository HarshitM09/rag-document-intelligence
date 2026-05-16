import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import google.generativeai as genai
import database

app = Flask(__name__)
app.secret_key = 'super_secret_onboarding_key' # Required for session management

# Initialize Gemini API
GEMINI_API_KEY = "AIzaSyCXDBxPipJC1qX2Ukn11OrgdfaNLiGnd5o"
genai.configure(api_key=GEMINI_API_KEY)

# --- AUTHENTICATION ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = database.get_user_by_username(username)
        if user and user['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials.")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# --- MAIN ROUTES ---

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', role=session.get('role'), username=session.get('username'))

@app.route('/resources')
def resources():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if session.get('role') == 'admin':
        return redirect(url_for('dashboard'))
    return render_template('resources.html', role=session.get('role'), username=session.get('username'))

# --- ADMIN ROUTES ---

@app.route('/admin/users', methods=['GET', 'POST'])
def handle_users():
    if not session.get('logged_in') or session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
        
    if request.method == 'GET':
        return jsonify(database.get_all_users())
        
    if request.method == 'POST':
        data = request.json
        success = database.create_user(data['username'], data['password'], data.get('role', 'user'))
        if success:
            return jsonify({"success": True}), 201
        return jsonify({"error": "User already exists"}), 400

# --- API ROUTES (CRUD) ---

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if not session.get('logged_in'):
         return jsonify({"error": "Unauthorized"}), 403

    if request.method == 'GET':
        all_tasks = database.get_all_tasks()
        if session.get('role') == 'admin':
            return jsonify(all_tasks)
        else:
            user_tasks = [t for t in all_tasks if t.get('assigned_to') == session.get('username')]
            return jsonify(user_tasks)
    
    if request.method == 'POST':
        if session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 403
            
        data = request.json
        new_task = database.add_task(data['task_name'], data['category'], data.get('status', 'Pending'), data.get('assigned_to', ''))
        return jsonify(new_task), 201

@app.route('/api/tasks/<task_id>', methods=['PUT', 'DELETE'])
def handle_single_task(task_id):
    if not session.get('logged_in'):
         return jsonify({"error": "Unauthorized"}), 403

    if request.method == 'PUT':
        data = request.json
        success = database.update_task(task_id, data)
        return jsonify({"success": success})
        
    if request.method == 'DELETE':
        if session.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 403
        success = database.delete_task(task_id)
        return jsonify({"success": success})

# --- AI INTEGRATION ROUTES ---

@app.route('/api/ai_suggestion', methods=['GET'])
def ai_suggestion():
    if not GEMINI_API_KEY:
        return jsonify({"suggestion": "Gemini API key is missing. Please set GEMINI_API_KEY in your environment variables to receive smart suggestions."})
    
    tasks = database.get_all_tasks()
    if session.get('role') != 'admin':
        tasks = [t for t in tasks if t.get('assigned_to') == session.get('username')]
        
    pending_tasks = [t['task_name'] for t in tasks if t['status'] != 'Completed']
    
    if not pending_tasks:
        return jsonify({"suggestion": "Amazing job! You've completed all your onboarding tasks. Take a moment to relax and welcome to the team!"})

    prompt = f"""
    A new joiner has the following pending onboarding tasks: {', '.join(pending_tasks)}. 
    Based on typical corporate onboarding priorities, suggest what they should focus on next and why. 
    Keep it encouraging, welcoming, and strictly to 2-3 sentences.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return jsonify({"suggestion": response.text.strip()})
    except Exception as e:
        return jsonify({"suggestion": "Our AI is taking a quick coffee break. Please try again later!"})

@app.route('/api/chat', methods=['POST'])
def chat():
    if not GEMINI_API_KEY:
        return jsonify({"response": "I am currently offline because the Gemini API key is missing."})
        
    user_message = request.json.get('message', '')
    
    system_instruction = "You are a helpful HR/IT onboarding assistant. Answer the new joiner's questions based on general corporate onboarding best practices. Be polite, concise, and welcoming."
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
        response = model.generate_content(user_message)
        return jsonify({"response": response.text.strip()})
    except Exception as e:
        return jsonify({"response": "Sorry, I encountered an error connecting to my brain. Please try again!"})

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)