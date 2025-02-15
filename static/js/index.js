

  function openModal() {
    document.getElementById('adminLoginModal').style.display = 'block';
    document.body.classList.add('modal-open'); // Prevents background scrolling
}

function closeModal() {
    document.getElementById('adminLoginModal').style.display = 'none';
    document.body.classList.remove('modal-open'); // Restores scrolling
}

// Close modal when clicking outside of it
window.onclick = function (event) {
    let modal = document.getElementById('adminLoginModal');
    if (event.target == modal) {
        closeModal();
    }
};

// Handle login validation
document.getElementById('adminLoginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission

    let username = document.getElementById('adminUsername').value;
    let password = document.getElementById('adminPassword').value;

    
    if (username === "admin" && password === "admin123") {
        
        window.location.href = "/admin_page"; // Redirect to admin page
    } else {
        alert("Invalid credentials! Please try again.");
    }
});


const themeToggle = document.getElementById('theme-toggle');
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');

themeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
});

mobileMenuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.classList.add('dark');
}
