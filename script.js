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
            { name: 'APPLE', price: 120.50, projection: 130.00 },
            { name: 'TESLA', price: 200.50, projection: 220.00 },
            { name: 'MICROSOFT', price: 200.50, projection: 250.00 },
            { name: 'GOOGLE', price: 200.50, projection: 220.00 },
            { name: 'AWS', price: 230.50, projection: 270.00 }
        ];
        stockData.forEach(stock => {
            const stockDiv = document.createElement('div');
            stockDiv.className = 'stock-item';
            stockDiv.innerHTML = `<div>STOCK NAME AND PRICE: ${stock.name} - $${stock.price}</div>
                                  <div>STOCK PROJECTION: $${stock.projection}</div>`;
            stockInfoDiv.appendChild(stockDiv);
        });
    };
