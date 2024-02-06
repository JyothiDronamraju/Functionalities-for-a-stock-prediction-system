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
    
