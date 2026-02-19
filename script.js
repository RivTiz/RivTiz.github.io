document.addEventListener('DOMContentLoaded', () => {
    // Dynamic Year in Footer
    const yearElement = document.getElementById('year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // Smooth Scrolling for Anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Intersection Observer for Reveal Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Fade in sections on scroll
    document.querySelectorAll('.section-title, .glass-card, .timeline-item').forEach(el => {
        el.style.opacity = '0'; // Initial state
        el.style.transform = 'translateY(20px)';
        el.classList.add('transition-element');
        observer.observe(el);
    });

    // Walkthrough Scroll Logic
    const scrollContainer = document.getElementById('walkthroughScroll');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const dots = document.querySelectorAll('.dot');

    if (scrollContainer) {
        // Button Clicks
        prevBtn.addEventListener('click', () => {
            scrollContainer.scrollBy({ left: -300, behavior: 'smooth' });
        });

        nextBtn.addEventListener('click', () => {
            scrollContainer.scrollBy({ left: 300, behavior: 'smooth' });
        });

        // Update Dots & Button State on Scroll
        scrollContainer.addEventListener('scroll', () => {
            const scrollLeft = scrollContainer.scrollLeft;
            const scrollWidth = scrollContainer.scrollWidth;
            const clientWidth = scrollContainer.clientWidth;

            // Disable buttons at ends
            prevBtn.disabled = scrollLeft <= 10;
            nextBtn.disabled = scrollLeft + clientWidth >= scrollWidth - 10;

            // Approximate active slide (this is a simple estimation based on scroll pct)
            const scrollPct = scrollLeft / (scrollWidth - clientWidth);
            const activeIndex = Math.round(scrollPct * (dots.length - 1));

            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === activeIndex);
            });
        });
    }

    // Optional cursor effect
    const cursor = document.querySelector('.cursor-glow');
    if (cursor) {
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });
    }
});
