document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('#login form');
    const dashboardSection = document.querySelector('#dashboard');

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        
        dashboardSection.style.display = 'block';
        loginForm.style.display = 'none';
    });
});
	