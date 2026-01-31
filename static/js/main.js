// Mobile Navigation Toggle
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        
        // Animate hamburger icon
        const spans = navToggle.querySelectorAll('span');
        spans[0].style.transform = navMenu.classList.contains('active') 
            ? 'rotate(45deg) translateY(8px)' : 'none';
        spans[1].style.opacity = navMenu.classList.contains('active') ? '0' : '1';
        spans[2].style.transform = navMenu.classList.contains('active') 
            ? 'rotate(-45deg) translateY(-8px)' : 'none';
    });
    
    // Close menu when clicking on a link
    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            const spans = navToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });
}

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offset = 80; // Account for fixed navbar
            const targetPosition = target.offsetTop - offset;
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Animated Counter for Statistics
const animateCounter = (element, target) => {
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    };
    
    updateCounter();
};

// Intersection Observer for Counter Animation
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const target = parseInt(entry.target.getAttribute('data-target'));
            animateCounter(entry.target, target);
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-number').forEach(counter => {
    counterObserver.observe(counter);
});

// Portfolio Filter
const filterButtons = document.querySelectorAll('.filter-btn');
const portfolioItems = document.querySelectorAll('.portfolio-item');

if (filterButtons.length > 0) {
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            const filter = button.getAttribute('data-filter');
            
            portfolioItems.forEach(item => {
                const category = item.getAttribute('data-category');
                
                if (filter === 'all' || category === filter) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease-in';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Flash Message Auto-Close
const flashMessages = document.querySelectorAll('.flash');
flashMessages.forEach(flash => {
    // Auto-close after 5 seconds
    setTimeout(() => {
        flash.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => flash.remove(), 300);
    }, 5000);
    
    // Close button
    const closeBtn = flash.querySelector('.flash-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            flash.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => flash.remove(), 300);
        });
    }
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Scroll to Top Button
const scrollTopBtn = document.getElementById('scrollTop');

if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    });
    
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Navbar Background on Scroll
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(0, 0, 0, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.7)';
    } else {
        navbar.style.background = 'rgba(0, 0, 0, 0.95)';
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.5)';
    }
});

// Form Validation
const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        // The form uses Flask-WTF form fields rendered as HTML
        // Check for the actual field names in the rendered form
        const nameField = document.querySelector('input[name="name"]');
        const emailField = document.querySelector('input[name="email"]');
        const phoneField = document.querySelector('input[name="phone"]');
        const projectField = document.querySelector('select[name="project_type"]');
        const messageField = document.querySelector('textarea[name="message"]');
        
        // Basic validation only if all fields exist
        if (nameField && emailField && phoneField && projectField && messageField) {
            const name = nameField.value.trim();
            const email = emailField.value.trim();
            const phone = phoneField.value.trim();
            const project = projectField.value;
            const message = messageField.value.trim();
            
            let isValid = true;
            let errorMessage = '';
            
            // Name validation
            if (name.length < 3) {
                isValid = false;
                errorMessage += 'Name must be at least 3 characters long.\n';
            }
            
            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                isValid = false;
                errorMessage += 'Please enter a valid email address.\n';
            }
            
            // Phone validation
            const phoneRegex = /^[+]?[\d\s-]{10,}$/;
            if (!phoneRegex.test(phone)) {
                isValid = false;
                errorMessage += 'Please enter a valid phone number.\n';
            }
            
            // Project type validation
            if (!project) {
                isValid = false;
                errorMessage += 'Please select a project type.\n';
            }
            
            // Message validation
            if (message.length < 20) {
                isValid = false;
                errorMessage += 'Project description must be at least 20 characters.\n';
            }
            
            if (!isValid) {
                e.preventDefault();
                alert(errorMessage);
            }
        }
    });
    
    // Real-time validation feedback
    const inputs = contactForm.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = '#f44336';
            } else {
                this.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            }
        });
        
        input.addEventListener('focus', function() {
            this.style.borderColor = '#4da3ff';
        });
    });
}

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const fadeInObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            fadeInObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

// Apply fade-in animation to cards
document.querySelectorAll('.service-card, .portfolio-item, .why-card, .testimonial-card, .process-step').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    fadeInObserver.observe(el);
});

// Parallax Effect for Hero Section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero-content');
    if (hero && scrolled < window.innerHeight) {
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
        hero.style.opacity = 1 - (scrolled / 600);
    }
});

// Loading Animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

// Service Card Tilt Effect
const serviceCards = document.querySelectorAll('.service-card');
serviceCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
    });
});

// Fetch and Display Live Stats (if API endpoint is available)
const fetchStats = async () => {
    try {
        const response = await fetch('/api/stats');
        if (response.ok) {
            const stats = await response.json();
            
            // Update stats if elements exist
            const projectsCounter = document.querySelector('[data-stat="projects"]');
            const clientsCounter = document.querySelector('[data-stat="clients"]');
            const completedCounter = document.querySelector('[data-stat="completed"]');
            
            if (projectsCounter) projectsCounter.textContent = stats.total_projects;
            if (clientsCounter) clientsCounter.textContent = stats.total_clients;
            if (completedCounter) completedCounter.textContent = stats.completed_projects;
        }
    } catch (error) {
        console.log('Stats API not available:', error);
    }
};

// Call fetchStats on page load
fetchStats();

// Keyboard Accessibility
document.addEventListener('keydown', (e) => {
    // ESC key closes mobile menu
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
    }
});

// Print current year in footer (if dynamic year element exists)
const yearElement = document.querySelector('.current-year');
if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// Prevent form double submission
if (contactForm) {
    let isSubmitting = false;
    contactForm.addEventListener('submit', function(e) {
        if (isSubmitting) {
            e.preventDefault();
            return false;
        }
        isSubmitting = true;
        
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            submitBtn.style.opacity = '0.7';
        }
    });
}

console.log('ByCodeHub - All systems operational ✓');