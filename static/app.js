// Personal Finance AI Assistant Frontend

// Set today's date as default
document.getElementById('date').valueAsDate = new Date();

// Add expense form handler
document.getElementById('expenseForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const expenseData = {
        amount: parseFloat(document.getElementById('amount').value),
        category: document.getElementById('category').value,
        description: document.getElementById('description').value,
        date: document.getElementById('date').value
    };
    
    try {
        const response = await fetch('/api/expenses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(expenseData)
        });
        
        if (response.ok) {
            // Clear form
            document.getElementById('expenseForm').reset();
            document.getElementById('date').valueAsDate = new Date();
            
            // Refresh expenses list
            loadExpenses();
            
            alert('Expense added successfully!');
        }
    } catch (error) {
        console.error('Error adding expense:', error);
        alert('Error adding expense');
    }
});

// Chat functionality
document.getElementById('sendButton').addEventListener('click', sendMessage);
document.getElementById('chatInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    chatInput.value = '';
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        addMessageToChat(data.response, 'ai');
    } catch (error) {
        console.error('Error sending message:', error);
        addMessageToChat('Sorry, I\'m having trouble connecting right now.', 'ai');
    }
}

function addMessageToChat(message, sender) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = message;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Load and display expenses
async function loadExpenses() {
    try {
        const response = await fetch('/api/expenses');
        const expenses = await response.json();
        
        const expensesList = document.getElementById('expensesList');
        expensesList.innerHTML = '';
        
        if (expenses.length === 0) {
            expensesList.innerHTML = '<p>No expenses recorded yet. Add your first expense above!</p>';
            return;
        }
        
        expenses.slice(0, 10).forEach(expense => {
            const expenseDiv = document.createElement('div');
            expenseDiv.className = 'expense-item';
            expenseDiv.innerHTML = `
                <strong>$${expense[1].toFixed(2)}</strong> - ${expense[2]}<br>
                <small>${expense[3] || 'No description'} | ${expense[4]}</small>
            `;
            expensesList.appendChild(expenseDiv);
        });
    } catch (error) {
        console.error('Error loading expenses:', error);
    }
}

// Initial load
loadExpenses();

// Add welcome message
addMessageToChat('Hi! I\'m your personal finance assistant. Ask me about your spending patterns, budgeting tips, or anything finance-related!', 'ai');