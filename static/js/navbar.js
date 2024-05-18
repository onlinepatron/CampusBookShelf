document.getElementById('navbarToggler').addEventListener('click', function() {
    var navIcon = document.getElementById('navIcon');
    if (navIcon.classList.contains('fa-bars')) {
        navIcon.classList.remove('fa-bars');
        navIcon.classList.add('fa-times');
    } else {
        navIcon.classList.remove('fa-times');
        navIcon.classList.add('fa-bars');
    }
});

