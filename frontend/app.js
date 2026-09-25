let medicines = [];

async function init() {
    try {
        const response = await fetch('/api/medicines');
        medicines = await response.json();
        updateStats();
    } catch (error) {
        console.error('Error loading medicines:', error);
    }
}

function updateStats() {
    const total = medicines.length;
    const lowStock = medicines.filter(m => m.stock < m.minimum_stock && m.stock > 0).length;
    const outOfStock = medicines.filter(m => m.stock === 0).length;

    document.getElementById('total-products').textContent = total;
    document.getElementById('low-stock').textContent = lowStock;
    document.getElementById('out-of-stock').textContent = outOfStock;
}

document.getElementById('search-input').addEventListener('input', async (e) => {
    const query = e.target.value;
    const resultsDiv = document.getElementById('search-results');

    if (!query) {
        resultsDiv.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/api/medicines/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();

        resultsDiv.innerHTML = results.map(med => `
            <div class="search-result-item" onclick="selectMedicine('${med.name}')">
                <div class="search-result-name">${med.name}</div>
                <div class="search-result-generic">${med.generic_name}</div>
                <div class="search-result-price">₹${med.price} | Stock: ${med.stock} units</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Search error:', error);
    }
});

function selectMedicine(name) {
    document.getElementById('chat-input').value = `Tell me about ${name}`;
    document.getElementById('search-results').innerHTML = '';
}

document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('chat-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        sendMessage();
    }
});

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    const chatHistory = document.getElementById('chat-history');

    chatHistory.innerHTML += `
        <div class="chat-message user-message">
            <div class="message-content">${escapeHtml(message)}</div>
        </div>
    `;

    input.value = '';

    chatHistory.innerHTML += `
        <div class="chat-message ai-message">
            <div class="loading"><div class="spinner"></div> Thinking...</div>
        </div>
    `;
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        chatHistory.removeChild(chatHistory.lastChild);

        const sourceHtml = data.sources.length > 0
            ? `<div class="message-sources">Source: ${data.sources.map(s => `<span class="source-tag">${escapeHtml(s)}</span>`).join('')}</div>`
            : '';

        chatHistory.innerHTML += `
            <div class="chat-message ai-message">
                <div class="message-content">${escapeHtml(data.answer)}</div>
                ${sourceHtml}
            </div>
        `;
    } catch (error) {
        chatHistory.removeChild(chatHistory.lastChild);
        chatHistory.innerHTML += `
            <div class="chat-message ai-message">
                <div class="message-content" style="color: #d9534f;">Error: ${escapeHtml(error.message)}</div>
            </div>
        `;
        console.error('Chat error:', error);
    }

    chatHistory.scrollTop = chatHistory.scrollHeight;
}

document.getElementById('low-stock-btn').addEventListener('click', () => {
    const lowStockItems = medicines.filter(m => m.stock < m.minimum_stock && m.stock > 0);
    displayInventory(lowStockItems, 'Low Stock Items');
});

document.getElementById('expiring-btn').addEventListener('click', () => {
    const today = new Date();
    const threeMonthsFromNow = new Date(today.getTime() + 90 * 24 * 60 * 60 * 1000);
    const expiringItems = medicines.filter(m => {
        const expiryDate = new Date(m.expiry_date);
        return expiryDate <= threeMonthsFromNow && expiryDate > today;
    });
    displayInventory(expiringItems, 'Expiring Soon');
});

function displayInventory(items, title) {
    const inventoryList = document.getElementById('inventory-list');

    if (items.length === 0) {
        inventoryList.innerHTML = `<p style="grid-column: 1/-1; color: #666;">No items to display</p>`;
        return;
    }

    inventoryList.innerHTML = items.map(item => `
        <div class="inventory-item">
            <div class="inventory-item-name">${item.name}</div>
            <div class="inventory-item-generic">${item.generic_name}</div>
            <div class="inventory-item-stock">
                Stock: <span class="${item.stock < item.minimum_stock ? 'inventory-item-warning' : ''}">${item.stock} units</span>
            </div>
        </div>
    `).join('');
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

init();
