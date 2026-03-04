// ============================================================
// COMPLEXE SCOLAIRE LES DIPLOMATES — main.js
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

  // ---- NAVBAR SCROLL EFFECT ----
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // ---- HAMBURGER MENU ----
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const spans = hamburger.querySelectorAll('span');
      const isOpen = navLinks.classList.contains('open');
      if (isOpen) {
        spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
      } else {
        spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
      }
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        hamburger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
      }
    });
  }

  // ---- PROGRESS BAR ANIMATION ----
  const progressFills = document.querySelectorAll('.progress-fill, .stat-bar-fill');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = el.style.width;
        el.style.width = '0';
        requestAnimationFrame(() => {
          el.style.transition = 'width 1s ease';
          el.style.width = target;
        });
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.2 });

  progressFills.forEach(el => observer.observe(el));

  // ---- FADE IN ON SCROLL ----
  const fadeEls = document.querySelectorAll('.kpi-card, .cycle-card, .article-card, .stat-card');
  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, i * 60);
        fadeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  fadeEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    fadeObserver.observe(el);
  });

  // ---- PAYMENT METHOD TOGGLE ----
  const methodOptions = document.querySelectorAll('.method-option');
  methodOptions.forEach(option => {
    option.addEventListener('click', () => {
      methodOptions.forEach(o => o.classList.remove('selected'));
      option.classList.add('selected');
    });
  });

  // ---- TABS ----
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  // ---- AUTO DISMISS MESSAGES (Django messages) ----
  const messages = document.querySelectorAll('.django-message');
  messages.forEach(msg => {
    setTimeout(() => {
      msg.style.transition = 'opacity 0.4s ease';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 400);
    }, 4000);
  });

});
