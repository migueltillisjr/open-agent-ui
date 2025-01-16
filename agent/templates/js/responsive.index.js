function responsiveMenu() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
        console.log(sidebar)
        console.log('Sidebar element FOUND!');
    } else {
        console.error('Sidebar element not found!');
    }
}