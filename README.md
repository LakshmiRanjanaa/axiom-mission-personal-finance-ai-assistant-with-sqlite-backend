# Personal Finance AI Assistant

A conversational AI assistant that helps track expenses and provides spending insights using SQLite database.

## Features
- Track expenses with categories
- Chat with AI about spending patterns
- View expense history
- Get personalized financial insights

## Setup
1. Install dependencies: `pip install flask openai sqlite3`
2. Set your OpenAI API key in `app.py`
3. Run: `python app.py`
4. Open http://localhost:5000

## Usage
- Add expenses using the form
- Chat with the AI about your spending
- Ask questions like "How much did I spend on food this month?"

## Database Schema
- expenses: id, amount, category, description, date
- Automatically created on first run