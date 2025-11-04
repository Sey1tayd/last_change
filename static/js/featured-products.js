document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('featuredProductsSlider');

    if (!slider) {
        return;
    }

    // Sonsuz döngü için içeriği kopyala
    const originalContent = slider.innerHTML;
    slider.innerHTML = originalContent + originalContent;
    
    // Yeni linkleri al (kopyalanan içerik dahil)
    const productLinks = slider.querySelectorAll('.product-link');
    
    // Orijinal içeriğin genişliğini hesapla
    let originalWidth = 0;
    let isAdjusting = false;
    let rafId = null;
    let wheelDirection = 0;
    
    function calculateOriginalWidth() {
        const cards = slider.querySelectorAll('.featured-product-card');
        if (cards.length === 0) return 0;
        
        // İkinci setin ilk kartının pozisyonunu kullan (en doğru yöntem)
        const halfIndex = Math.floor(cards.length / 2);
        if (cards[halfIndex]) {
            const secondSetStart = cards[halfIndex].offsetLeft;
            if (secondSetStart > 0) {
                return secondSetStart;
            }
        }
        
        // Alternatif: Toplam genişliğin yarısı
        return slider.scrollWidth / 2;
    }
    
    let lastScrollLeft = 0;
    
    function adjustScrollPosition() {
        if (isAdjusting || originalWidth <= 0) return;
        
        const currentScroll = slider.scrollLeft;
        const scrollDelta = currentScroll - lastScrollLeft;
        
        // İleri yönde: İkinci setin başına ulaştıysak, orijinal başa dön
        if (currentScroll >= originalWidth) {
            isAdjusting = true;
            // Smooth scroll'u geçici olarak devre dışı bırak
            const originalBehavior = slider.style.scrollBehavior;
            slider.style.scrollBehavior = 'auto';
            slider.scrollLeft = currentScroll - originalWidth;
            slider.style.scrollBehavior = originalBehavior;
            lastScrollLeft = slider.scrollLeft;
            wheelDirection = 0; // Reset
            setTimeout(function() {
                isAdjusting = false;
            }, 10);
            return;
        }
        
        // Geri yönde: Başlangıca ulaştıysak ve geri kaydırıyorsak, ikinci setin sonuna git
        // scrollDelta < 0 veya wheelDirection < 0: geri kaydırma
        const isScrollingBackward = scrollDelta < 0 || wheelDirection < 0;
        if (currentScroll <= 0 && isScrollingBackward && lastScrollLeft >= 0) {
            isAdjusting = true;
            // Smooth scroll'u geçici olarak devre dışı bırak
            const originalBehavior = slider.style.scrollBehavior;
            slider.style.scrollBehavior = 'auto';
            // İkinci setin sonuna git (orijinal genişliğin sonuna yakın)
            slider.scrollLeft = originalWidth - 1;
            slider.style.scrollBehavior = originalBehavior;
            lastScrollLeft = slider.scrollLeft;
            wheelDirection = 0; // Reset
            setTimeout(function() {
                isAdjusting = false;
            }, 10);
            return;
        }
        
        lastScrollLeft = currentScroll;
        // Wheel direction'ı sıfırla (sadece bir kez kullan)
        if (wheelDirection !== 0) {
            setTimeout(function() {
                wheelDirection = 0;
            }, 50);
        }
    }
    
    // Sayfa yüklendikten sonra genişliği hesapla ve başlangıç pozisyonunu ayarla
    function initializeSlider() {
        // Genişliği hesapla
        originalWidth = calculateOriginalWidth();
        
        // Scroll pozisyonunu orijinal içeriğin başlangıcına ayarla
        if (originalWidth > 0) {
            isAdjusting = true;
            slider.scrollLeft = 0;
            lastScrollLeft = 0;
            // Kısa bir gecikme ile flag'i kaldır
            setTimeout(function() {
                isAdjusting = false;
            }, 100);
        }
    }
    
    // İlk yükleme
    setTimeout(initializeSlider, 100);
    
    // Görüntüler yüklendiğinde de kontrol et (genişlik hesaplaması için)
    window.addEventListener('load', function() {
        originalWidth = calculateOriginalWidth();
        if (originalWidth > 0) {
            isAdjusting = true;
            const currentPos = slider.scrollLeft;
            slider.scrollLeft = currentPos;
            lastScrollLeft = currentPos;
            setTimeout(function() {
                isAdjusting = false;
            }, 100);
        }
    });
    
    // Scroll event listener - sonsuz döngü için
    slider.addEventListener('scroll', function() {
        if (rafId) {
            cancelAnimationFrame(rafId);
        }
        
        rafId = requestAnimationFrame(function() {
            adjustScrollPosition();
            rafId = null;
        });
    }, { passive: true });
    
    // Wheel event - geri kaydırmayı daha iyi algılamak için
    slider.addEventListener('wheel', function(e) {
        wheelDirection = e.deltaX > 0 ? 1 : -1;
        // Wheel event'inden sonra scroll event'i tetiklenecek ve adjustScrollPosition çalışacak
    }, { passive: true });

    // Drag/Swipe functionality
    let isDown = false;
    let startX;
    let scrollLeft;

    // Otomatik kaydırma DEVRE DIŞI - performans için kaldırıldı
    let autoScrollInterval = null;
    let isPaused = false;
    // const scrollSpeed = 1; // Piksel cinsinden kaydırma hızı
    // const scrollDelay = 15; // Her X ms'de bir kaydır
    
    function startAutoScroll() {
        // Auto-scroll devre dışı - performans için
        return;
    }
    
    function stopAutoScroll() {
        if (autoScrollInterval) {
            clearInterval(autoScrollInterval);
            autoScrollInterval = null;
        }
    }
    
    // Hover durumunda duraklat
    slider.addEventListener('mouseenter', function() {
        isPaused = true;
    });
    
    slider.addEventListener('mouseleave', function() {
        isPaused = false;
        // Drag sırasında mouseleave olursa drag'i sonlandır
        if (isDown) {
            isDown = false;
            slider.classList.remove('dragging');
            slider.style.cursor = 'grab';
        }
    });

    slider.addEventListener('mousedown', function(e) {
        isDown = true;
        slider.classList.add('dragging');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
        slider.style.cursor = 'grabbing';
    });

    slider.addEventListener('mouseup', function() {
        isDown = false;
        slider.classList.remove('dragging');
        slider.style.cursor = 'grab';
    });

    slider.addEventListener('mousemove', function(e) {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 2; // Scroll hızı
        slider.scrollLeft = scrollLeft - walk;
    });

    // Touch events for mobile
    let touchStartX;
    let touchScrollLeft;

    slider.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].pageX - slider.offsetLeft;
        touchScrollLeft = slider.scrollLeft;
    }, { passive: true });

    slider.addEventListener('touchmove', function(e) {
        if (!touchStartX) return;
        const touchX = e.touches[0].pageX - slider.offsetLeft;
        const walk = (touchX - touchStartX) * 2;
        slider.scrollLeft = touchScrollLeft - walk;
    }, { passive: true });

    slider.addEventListener('touchend', function() {
        touchStartX = null;
    });

    // Ürün linklerine tıklama - özel sayfaya yönlendirme
    productLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const slug = this.getAttribute('data-slug');
            window.location.href = '/urun/' + slug + '/';
        });
    });


    // Klavye navigasyonu (opsiyonel)
    slider.setAttribute('tabindex', '0');
    slider.addEventListener('keydown', function(e) {
        const card = slider.querySelector('.featured-product-card');
        if (!card) return;
        const cardWidth = card.offsetWidth;
        const gap = 30;
        
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            slider.scrollBy({
                left: -(cardWidth + gap),
                behavior: 'smooth'
            });
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            slider.scrollBy({
                left: (cardWidth + gap),
                behavior: 'smooth'
            });
        }
    });
    
    // Resize event - genişliği yeniden hesapla
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            const savedScroll = slider.scrollLeft;
            const oldWidth = originalWidth;
            originalWidth = calculateOriginalWidth();
            
            // Genişlik değiştiyse scroll pozisyonunu normalize et
            if (oldWidth > 0 && originalWidth > 0 && oldWidth !== originalWidth) {
                isAdjusting = true;
                let normalizedScroll = (savedScroll / oldWidth) * originalWidth;
                // Orijinal genişlik sınırları içinde tut
                if (normalizedScroll >= originalWidth) {
                    normalizedScroll = normalizedScroll % originalWidth;
                }
                slider.scrollLeft = Math.max(0, Math.min(normalizedScroll, originalWidth));
                lastScrollLeft = slider.scrollLeft;
                setTimeout(function() {
                    isAdjusting = false;
                }, 100);
            }
        }, 250);
    });
});

