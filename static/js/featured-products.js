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
    let isScrolling = false;
    
    function calculateOriginalWidth() {
        // Önce scroll pozisyonunu kaydet ve isScrolling flag'ini ayarla
        const savedScroll = slider.scrollLeft;
        isScrolling = true;
        
        // En basit ve doğru yöntem: slider'ın toplam genişliğinin yarısı
        // Çünkü içeriği ikiye böldük (orijinal + kopya)
        let calculatedWidth = slider.scrollWidth / 2;
        
        // Alternatif: İkinci setin başlangıç pozisyonunu kullan (daha doğru)
        const cards = slider.querySelectorAll('.featured-product-card');
        if (cards.length > 0) {
            const midIndex = Math.floor(cards.length / 2);
            if (cards[midIndex]) {
                const midCardLeft = cards[midIndex].offsetLeft;
                if (midCardLeft > 0 && midCardLeft < calculatedWidth * 1.5) {
                    calculatedWidth = midCardLeft;
                }
            }
        }
        
        // Sadece geçerli bir genişlik varsa güncelle
        if (calculatedWidth > 0 && isFinite(calculatedWidth)) {
            originalWidth = calculatedWidth;
        }
        
        // Scroll pozisyonunu geri yükle
        requestAnimationFrame(function() {
            slider.scrollLeft = savedScroll;
            setTimeout(function() {
                isScrolling = false;
            }, 50);
        });
    }
    
    // Sayfa yüklendikten sonra genişliği hesapla
    let initTimeout;
    let isInitialized = false;
    
    function initializeSlider() {
        if (isInitialized) return;
        isInitialized = true;
        
        calculateOriginalWidth();
        // Scroll pozisyonunu orijinal içeriğin başlangıcına ayarla
        isScrolling = true; // İlk yüklemede scroll event'ini engelle
        requestAnimationFrame(function() {
            slider.scrollLeft = 0;
            setTimeout(function() {
                isScrolling = false;
            }, 300);
        });
    }
    
    // İlk yükleme - DOMContentLoaded zaten tetiklenmiş (zaten içindeyiz)
    initTimeout = setTimeout(initializeSlider, 300);
    
    // Görüntüler yüklendiğinde de kontrol et (genişlik hesaplaması için)
    window.addEventListener('load', function() {
        clearTimeout(initTimeout);
        isInitialized = false; // Yeniden hesaplama için reset
        initTimeout = setTimeout(initializeSlider, 150);
    });
    
    // Scroll event listener - sonsuz döngü için
    let scrollTimeout;
    slider.addEventListener('scroll', function() {
        // Throttle scroll events - sadece belirli aralıklarla kontrol et
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            if (isScrolling || originalWidth <= 0) return;
            
            const currentScroll = slider.scrollLeft;
            const tolerance = 5; // Küçük tolerans değeri
            
            // Eğer klonun başına geldiysek (orijinal genişliğe ulaştıysak)
            if (currentScroll >= originalWidth - tolerance) {
                isScrolling = true;
                // Sessizce orijinal başlangıca dön (animasyon yok)
                // scroll event'ini tetiklememek için requestAnimationFrame kullan
                requestAnimationFrame(function() {
                    slider.scrollLeft = currentScroll - originalWidth;
                    setTimeout(function() {
                        isScrolling = false;
                    }, 100);
                });
            }
            // Eğer geriye kaydırıyorsak ve başa geldiysek
            else if (currentScroll <= tolerance) {
                isScrolling = true;
                // Orijinal sona git - scroll event'ini tetiklememek için requestAnimationFrame kullan
                requestAnimationFrame(function() {
                    slider.scrollLeft = originalWidth + currentScroll;
                    setTimeout(function() {
                        isScrolling = false;
                    }, 100);
                });
            }
        }, 10); // Her 10ms'de bir kontrol et (throttle)
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
    let isResizing = false;
    window.addEventListener('resize', function() {
        if (isResizing) return;
        isResizing = true;
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            const savedScroll = slider.scrollLeft;
            const oldWidth = originalWidth;
            calculateOriginalWidth();
            // Genişlik değiştiyse scroll pozisyonunu normalize et
            if (oldWidth > 0 && originalWidth > 0 && oldWidth !== originalWidth) {
                requestAnimationFrame(function() {
                    isScrolling = true;
                    let normalizedScroll = (savedScroll / oldWidth) * originalWidth;
                    // Orijinal genişlik sınırları içinde tut
                    if (normalizedScroll >= originalWidth) {
                        normalizedScroll = normalizedScroll % originalWidth;
                    }
                    slider.scrollLeft = Math.max(0, Math.min(normalizedScroll, originalWidth));
                    setTimeout(function() {
                        isScrolling = false;
                        isResizing = false;
                    }, 150);
                });
            } else {
                isResizing = false;
            }
        }, 250);
    });
});

