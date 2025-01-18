function responsiveMenu() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    } else {
        console.error('Sidebar element not found!');
    }
}