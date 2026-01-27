// Custom admin JavaScript for dashboard functionality

document.addEventListener('DOMContentLoaded', function() {
    // Toggle sidebar on mobile
    const sidebarToggle = document.getElementById('logo');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('hidden');
        });
    }
    
    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('active');
            overlay.classList.add('hidden');
        });
    }
    
    // Close sidebar when clicking close button
    const sidebarClose = document.getElementById('sidebar-close');
    if (sidebarClose) {
        sidebarClose.addEventListener('click', function() {
            sidebar.classList.remove('active');
            overlay.classList.add('hidden');
        });
    }
    
    // Toggle sidebar collapse
    const sidebarCollapse = document.getElementById('sidebar-collapse');
    const collapseIcon = document.getElementById('collapse-icon');
    
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            document.body.classList.toggle('sidebar-collapsed');
            if (collapseIcon) {
                collapseIcon.classList.toggle('rotate-180');
            }
        });
    }
    
    // Toggle submenu
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const parentItem = this.closest('.parent-item');
            const subNav = parentItem.querySelector('.sub-nav');
            const caret = this.querySelector('.ph-caret-down');
            
            // Close other submenus
            navBtns.forEach(otherBtn => {
                if (otherBtn !== this) {
                    const otherParent = otherBtn.closest('.parent-item');
                    const otherSubNav = otherParent.querySelector('.sub-nav');
                    const otherCaret = otherBtn.querySelector('.ph-caret-down');
                    
                    if (otherSubNav) {
                        otherSubNav.style.maxHeight = '0';
                        otherSubNav.classList.remove('open');
                    }
                    if (otherCaret) {
                        otherCaret.style.transform = 'rotate(0deg)';
                    }
                }
            });
            
            // Toggle current submenu
            if (subNav) {
                if (subNav.classList.contains('open')) {
                    subNav.style.maxHeight = '0';
                    subNav.classList.remove('open');
                    if (caret) {
                        caret.style.transform = 'rotate(0deg)';
                    }
                } else {
                    subNav.style.maxHeight = subNav.scrollHeight + 'px';
                    subNav.classList.add('open');
                    if (caret) {
                        caret.style.transform = 'rotate(180deg)';
                    }
                }
            }
        });
    });
    
    // Toggle notification dropdown
    const notificationBtn = document.getElementById('notification-btn');
    const notificationDropdown = document.getElementById('notification-dropdown');
    
    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', function() {
            notificationDropdown.classList.toggle('hidden');
        });
        
        // Close dropdown when clicking elsewhere
        document.addEventListener('click', function(event) {
            if (!notificationBtn.contains(event.target) && !notificationDropdown.contains(event.target)) {
                notificationDropdown.classList.add('hidden');
            }
        });
    }
    
    // Toggle user menu
    const userMenuTrigger = document.getElementById('user-menu-trigger-aside');
    const userMenuDropdown = document.getElementById('user-menu-dropdown-aside');
    
    if (userMenuTrigger && userMenuDropdown) {
        userMenuTrigger.addEventListener('click', function() {
            userMenuDropdown.classList.toggle('hidden');
        });
        
        // Close dropdown when clicking elsewhere
        document.addEventListener('click', function(event) {
            if (!userMenuTrigger.contains(event.target) && !userMenuDropdown.contains(event.target)) {
                userMenuDropdown.classList.add('hidden');
            }
        });
    }
    
    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.documentElement.classList.toggle('dark');
            // Save preference to localStorage
            const isDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
        
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        }
    }
    
    // Initialize all submenus as closed
    const subNavs = document.querySelectorAll('.sub-nav');
    subNavs.forEach(subNav => {
        subNav.style.maxHeight = '0';
        subNav.classList.remove('open');
    });
});

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Utility function to format numbers with thousands separators
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}