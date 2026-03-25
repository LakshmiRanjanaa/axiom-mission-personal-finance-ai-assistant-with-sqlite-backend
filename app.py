from flask import Flask, render_template, request, jsonify
import sqlite3
import openai
from datetime import datetime
import json

app = Flask(__name__)

# TODO: Set your OpenAI API key here
openai.api_key = "your-openai-api-key-here"

# Database setup
def init_db():
    """Initialize SQLite database with expenses table"""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_expenses():
    """Get all expenses from database"""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = cursor.fetchall()
    
    conn.close()
    return expenses

def add_expense(amount, category, description, date):
    """Add new expense to database"""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, description, date))
    
    conn.commit()
    conn.close()

def get_spending_summary():
    """Get spending summary for AI context"""
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Total spending
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()[0] or 0
    
    # Spending by category
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    by_category = cursor.fetchall()
    
    conn.close()
    return {
        'total': total,
        'by_category': by_category
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def api_get_expenses():
    """API endpoint to get all expenses"""
    expenses = get_expenses()
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def api_add_expense():
    """API endpoint to add new expense"""
    data = request.json
    add_expense(
        data['amount'],
        data['category'],
        data['description'],
        data['date']
    )
    return jsonify({'status': 'success'})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat with AI about expenses"""
    user_message = request.json['message']
    
    # Get current spending data for context
    summary = get_spending_summary()
    expenses = get_expenses()[:10]  # Last 10 expenses
    
    # Create context for AI
    context = f"""
    You are a personal finance assistant. Here's the user's spending data:
    Total spent: ${summary['total']:.2f}
    Spending by category: {summary['by_category']}
    Recent expenses: {expenses}
    
    Provide helpful, specific advice about their spending patterns.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": user_message}
            ],
            max_tokens=200
        )
        
        ai_response = response.choices[0].message.content
        return jsonify({'response': ai_response})
    
    except Exception as e:
        return jsonify({'response': f'Sorry, AI is not available. Error: {str(e)}'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)