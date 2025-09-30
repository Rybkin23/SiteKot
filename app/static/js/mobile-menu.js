console.log('Mobile menu script loaded');

function initMobileMenu() {
    console.log('Initializing mobile menu');

    const menuButton = document.querySelector('.mobile-menu-button');
    const mainNav = document.querySelector('.main-nav');

    if (!menuButton || !mainNav) {
        console.warn('Mobile menu elements not found');
        return;
    }

    menuButton.addEventListener('click', function (e) {
        e.stopPropagation();
        console.log('Menu button clicked');

        this.classList.toggle('active');
        mainNav.classList.toggle('active');

        if (mainNav.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
            document.body.classList.add('menu-open');
        } else {
            document.body.style.overflow = '';
            document.body.classList.remove('menu-open');
        }
    });

    document.querySelectorAll('.main-nav a').forEach(link => {
        link.addEventListener('click', function (e) {
            if (this.getAttribute('href').startsWith('#')) {
                setTimeout(() => {
                    menuButton.classList.remove('active');
                    mainNav.classList.remove('active');
                    document.body.style.overflow = '';
                    document.body.classList.remove('menu-open');
                }, 300);
            } else {
                e.preventDefault();
                console.log('Closing menu');
                menuButton.classList.remove('active');
                mainNav.classList.remove('active');
                document.body.style.overflow = '';
                document.body.classList.remove('menu-open');

                window.location.href = this.href;
            }
        });
    });

    document.addEventListener('click', function (event) {
        if (mainNav.classList.contains('active') &&
            !event.target.closest('.main-nav') &&
            !event.target.closest('.mobile-menu-button')) {
            console.log('Click outside - closing menu');
            menuButton.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.style.overflow = '';
            document.body.classList.remove('menu-open');
        }
    });

    mainNav.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 768 && mainNav.classList.contains('active')) {
            menuButton.classList.remove('active');
            mainNav.classList.remove('active');
            document.body.style.overflow = '';
            document.body.classList.remove('menu-open');
        }
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileMenu);
} else {
    initMobileMenu();
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initMobileMenu };
}