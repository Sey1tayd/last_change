// Mobile Categories Menu Toggle Functionality

document.addEventListener('DOMContentLoaded', function() {
  const mobileMenuToggle = document.getElementById('mobileMenuToggle');
  const mobileCategoriesDrawer = document.getElementById('mobileCategoriesDrawer');
  const mobileCategoriesOverlay = document.getElementById('mobileCategoriesOverlay');
  const mobileCategoriesClose = document.getElementById('mobileCategoriesClose');
  
  function openMobileMenu() {
    if (mobileCategoriesDrawer) {
      mobileCategoriesDrawer.classList.add('active');
    }
    if (mobileCategoriesOverlay) {
      mobileCategoriesOverlay.classList.add('active');
    }
    if (mobileMenuToggle) {
      mobileMenuToggle.classList.add('active');
    }
    document.body.style.overflow = 'hidden';
  }
  
  function closeMobileMenu() {
    if (mobileCategoriesDrawer) {
      mobileCategoriesDrawer.classList.remove('active');
    }
    if (mobileCategoriesOverlay) {
      mobileCategoriesOverlay.classList.remove('active');
    }
    if (mobileMenuToggle) {
      mobileMenuToggle.classList.remove('active');
    }
    document.body.style.overflow = '';
  }
  
  // Toggle menu button
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      if (mobileCategoriesDrawer && mobileCategoriesDrawer.classList.contains('active')) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });
  }
  
  // Close button
  if (mobileCategoriesClose) {
    mobileCategoriesClose.addEventListener('click', closeMobileMenu);
  }
  
  // Overlay click to close
  if (mobileCategoriesOverlay) {
    mobileCategoriesOverlay.addEventListener('click', closeMobileMenu);
  }
  
  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && mobileCategoriesDrawer && mobileCategoriesDrawer.classList.contains('active')) {
      closeMobileMenu();
    }
  });
  
  // Close menu when clicking on a category link
  const mobileCategoryLinks = document.querySelectorAll('.mobile-categories-list a');
  mobileCategoryLinks.forEach(function(link) {
    link.addEventListener('click', function() {
      // Small delay to allow navigation
      setTimeout(closeMobileMenu, 100);
    });
  });
});

