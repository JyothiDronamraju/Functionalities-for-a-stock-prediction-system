const searchStockInput = document.getElementById('searchStock').value.trim();

const dashboardSection = document.getElementById('dashboard');
    const stockInfoDiv = document.getElementById('stock-info');

    function login() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username && password) {
            dashboardSection.style.display = 'block';
            loginForm.style.display = 'none';
            updateStockInfo();
        }
    }

    function updateStockInfo() {
        const stockData = [
            { name: 'MICROSOFT', price: 230.50, projection: 270.00 }
        ];
        stockData.forEach(stock => {
            const stockDiv = document.createElement('div');
            stockDiv.className = 'stock-item';
            stockDiv.innerHTML = `<div>STOCK NAME AND PRICE: ${stock.name} - $${stock.price}</div>
                                  <div>STOCK PROJECTION: $${stock.projection}</div>`;
            stockInfoDiv.appendChild(stockDiv);
        });
    };

    searchButton.addEventListener('click', async function() {
        const searchStockInput = document.getElementById('searchStock').value.trim();
        stockDataBody.innerHTML = '';
        try {
            const response = await fetch(/api/stock-predictions?stockName=${searchStockInput});
            const data = await response.json();
        } catch (error) {
            console.error('Error:', error);
            stockDataBody.innerHTML = '<tr><td colspan="3">An error occurred while fetching data</td></tr>';
        }
    });