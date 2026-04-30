document.addEventListener('DOMContentLoaded', () => {
    initHeroAnimation();
    initScrollReveal();
    initNavbarScroll();
    initUploadZones();
    initFormSubmit();
    initSyncScroll();
    initControls();
    initMobileMenu();
});

function initHeroAnimation() {
    const titleElement = document.getElementById('animated-title');
    if (!titleElement) return;
    
    const text = titleElement.innerText;
    titleElement.innerHTML = '';
    const words = text.split(' ');
    
    words.forEach((word, index) => {
        const span = document.createElement('span');
        span.innerText = word + ' ';
        span.style.animation = `fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards`;
        span.style.animationDelay = `${index * 0.1}s`;
        titleElement.appendChild(span);
    });
}

function initScrollReveal() {
    const reveals = document.querySelectorAll('.scroll-reveal');
    const stepperLines = document.querySelectorAll('.step-line');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                if (entry.target.classList.contains('how-it-works')) {
                    stepperLines.forEach(line => line.classList.add('animate'));
                }
            }
        });
    }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

    reveals.forEach(el => observer.observe(el));
}

function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

function initMobileMenu() {
    const btn = document.querySelector('.mobile-menu-btn');
    const links = document.querySelector('.nav-links');
    if(btn && links) {
        btn.addEventListener('click', () => {
            links.classList.toggle('show');
        });
    }
}

let uploadedFiles = { a: null, b: null };

function initUploadZones() {
    setupZone('a');
    setupZone('b');
}

function setupZone(zoneId) {
    const card = document.getElementById(`zone-${zoneId}`);
    const input = document.getElementById(`file-${zoneId}`);
    const preview = document.getElementById(`preview-${zoneId}`);
    const filenameEl = document.getElementById(`filename-${zoneId}`);
    const filesizeEl = document.getElementById(`filesize-${zoneId}`);
    const removeBtn = preview.querySelector('.btn-remove');
    
    // Drag & Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        card.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        card.addEventListener(eventName, () => card.classList.add('drag-over'), false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        card.addEventListener(eventName, () => card.classList.remove('drag-over'), false);
    });
    
    card.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            handleFile(files[0], zoneId, input);
            createParticleBurst(e.clientX, e.clientY, card);
        }
    }, false);
    
    input.addEventListener('change', function() {
        if (this.files.length) {
            handleFile(this.files[0], zoneId, input);
        }
    });
    
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // prevent opening file browser
        input.value = '';
        uploadedFiles[zoneId] = null;
        card.classList.remove('has-file');
        preview.classList.add('hidden');
        preview.classList.remove('success-glow');
        checkCompareButton();
    });
}

function handleFile(file, zoneId, inputElement) {
    if (file.type !== "application/pdf") {
        alert("Please upload a valid PDF file.");
        return;
    }
    
    const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
    if (sizeInMB > 50) {
        alert("File size exceeds 50MB limit.");
        return;
    }
    
    uploadedFiles[zoneId] = file;
    
    // Manually set files if from drop
    const dt = new DataTransfer();
    dt.items.add(file);
    inputElement.files = dt.files;
    
    document.getElementById(`filename-${zoneId}`).textContent = file.name;
    document.getElementById(`filesize-${zoneId}`).textContent = `${sizeInMB} MB`;
    
    const card = document.getElementById(`zone-${zoneId}`);
    const preview = document.getElementById(`preview-${zoneId}`);
    
    card.classList.add('has-file');
    preview.classList.remove('hidden');
    
    // Small success glow
    setTimeout(() => preview.classList.add('success-glow'), 50);
    setTimeout(() => preview.classList.remove('success-glow'), 1500);
    
    checkCompareButton();
}

function checkCompareButton() {
    const btn = document.getElementById('btn-compare');
    if (uploadedFiles.a && uploadedFiles.b) {
        btn.disabled = false;
        btn.classList.add('shimmer');
    } else {
        btn.disabled = true;
        btn.classList.remove('shimmer');
    }
}

function createParticleBurst(x, y, container) {
    const colors = ['#6C63FF', '#00D4FF', '#22c55e'];
    for (let i = 0; i < 8; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random direction
        const angle = Math.random() * Math.PI * 2;
        const velocity = 50 + Math.random() * 50;
        const tx = Math.cos(angle) * velocity;
        const ty = Math.sin(angle) * velocity;
        
        particle.style.setProperty('--tx', `${tx}px`);
        particle.style.setProperty('--ty', `${ty}px`);
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        const rect = container.getBoundingClientRect();
        // Fallback position to center if x,y are 0
        const startX = x ? x - rect.left : rect.width/2;
        const startY = y ? y - rect.top : rect.height/2;
        
        particle.style.left = `${startX}px`;
        particle.style.top = `${startY}px`;
        particle.style.animation = `particleBurst 0.6s ease-out forwards`;
        
        container.appendChild(particle);
        setTimeout(() => particle.remove(), 600);
    }
}

// Ripple Effect for buttons
document.addEventListener('click', function(e) {
    if(e.target.closest('.btn-primary') || e.target.closest('.btn-outline')) {
        const btn = e.target.closest('.btn-primary') || e.target.closest('.btn-outline');
        if(btn.disabled) return;
        
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;
        
        const size = Math.max(rect.width, rect.height);
        ripple.style.width = ripple.style.height = `${size}px`;
        // Centering
        ripple.style.marginLeft = `-${size/2}px`;
        ripple.style.marginTop = `-${size/2}px`;
        
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }
});

function initFormSubmit() {
    const form = document.getElementById('upload-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!uploadedFiles.a || !uploadedFiles.b) return;
        
        const loadingOverlay = document.getElementById('loading-overlay');
        loadingOverlay.classList.remove('hidden');
        
        // Cycle status text
        const statusTexts = document.querySelectorAll('.status-text');
        let currentStatus = 0;
        const statusInterval = setInterval(() => {
            statusTexts[currentStatus].classList.remove('active');
            currentStatus = (currentStatus + 1) % statusTexts.length;
            statusTexts[currentStatus].classList.add('active');
        }, 3000);
        
        const formData = new FormData();
        formData.append('file1', uploadedFiles.a);
        formData.append('file2', uploadedFiles.b);
        
        try {
            const response = await fetch('/api/compare', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            clearInterval(statusInterval);
            loadingOverlay.classList.add('hidden');
            
            if (response.ok) {
                renderResults(result);
                document.getElementById('results-section').classList.remove('hidden');
                setTimeout(() => {
                    document.getElementById('results-section').classList.add('visible');
                    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            } else {
                alert("Error: " + (result.error || "Failed to compare documents."));
            }
        } catch (error) {
            clearInterval(statusInterval);
            loadingOverlay.classList.add('hidden');
            alert("Network error. Please try again.");
            console.error(error);
        }
    });

    document.getElementById('btn-cancel').addEventListener('click', () => {
        document.getElementById('loading-overlay').classList.add('hidden');
    });
}

function renderResults(result) {
    const diffContainerA = document.getElementById('diff-content-a');
    const diffContainerB = document.getElementById('diff-content-b');
    const insightsContainer = document.getElementById('insights-text');
    
    diffContainerA.innerHTML = '';
    diffContainerB.innerHTML = '';
    
    // Parse the raw comparison result
    let compData = result.comparison.raw_comparison;
    if (typeof compData === 'string') {
        try { compData = JSON.parse(compData); } catch(e) {}
    }
    
    let added = 0, removed = 0, modified = 0, unchanged = 0;
    
    // We assume compData is an array of objects with { "original": "", "modified": "", "status": "" }
    if (Array.isArray(compData)) {
        compData.forEach((item, index) => {
            const status = item.status || 'unchanged';
            if(status === 'added') added++;
            else if(status === 'removed') removed++;
            else if(status === 'modified') modified++;
            else unchanged++;
            
            // Render A
            const lineA = document.createElement('div');
            lineA.className = `diff-line ${status === 'added' ? 'hidden' : status}`;
            lineA.innerHTML = `
                <div class="line-num">${index+1}</div>
                <div class="line-content">${escapeHTML(item.original || '')}</div>
            `;
            diffContainerA.appendChild(lineA);
            
            // Render B
            const lineB = document.createElement('div');
            lineB.className = `diff-line ${status === 'removed' ? 'hidden' : status}`;
            lineB.innerHTML = `
                <div class="line-num">${index+1}</div>
                <div class="line-content">${escapeHTML(item.modified || '')}</div>
            `;
            diffContainerB.appendChild(lineB);
            
            // Add stagger animation
            lineA.style.animation = `fadeInUp 0.3s forwards`;
            lineA.style.animationDelay = `${Math.min(index * 10, 500)}ms`;
            lineA.style.opacity = '0';
            
            lineB.style.animation = `fadeInUp 0.3s forwards`;
            lineB.style.animationDelay = `${Math.min(index * 10, 500)}ms`;
            lineB.style.opacity = '0';
        });
    } else {
        diffContainerA.innerHTML = '<div class="diff-line"><div class="line-content">Error parsing comparison data</div></div>';
        diffContainerB.innerHTML = '<div class="diff-line"><div class="line-content">Error parsing comparison data</div></div>';
    }
    
    animateValue('stat-added', 0, added, 800);
    animateValue('stat-removed', 0, removed, 800);
    animateValue('stat-modified', 0, modified, 800);
    animateValue('stat-unchanged', 0, unchanged, 800);
    
    // Render Insights
    if(result.insights && result.insights.insights) {
        document.getElementById('report-insights').classList.remove('hidden');
        let insightHtml = result.insights.insights
            .replace(/\n\n/g, '</p><p>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
        insightsContainer.innerHTML = `<p>${insightHtml}</p>`;
    }
}

function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}

function animateValue(id, start, end, duration) {
    if (start === end) return;
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function initSyncScroll() {
    const panelA = document.getElementById('diff-content-a');
    const panelB = document.getElementById('diff-content-b');
    let isSyncingLeftScroll = false;
    let isSyncingRightScroll = false;
    
    if(!panelA || !panelB) return;

    panelA.onscroll = function() {
        if (!isSyncingLeftScroll) {
            isSyncingRightScroll = true;
            panelB.scrollTop = this.scrollTop;
            panelB.scrollLeft = this.scrollLeft;
        }
        isSyncingLeftScroll = false;
    }

    panelB.onscroll = function() {
        if (!isSyncingRightScroll) {
            isSyncingLeftScroll = true;
            panelA.scrollTop = this.scrollTop;
            panelA.scrollLeft = this.scrollLeft;
        }
        isSyncingRightScroll = false;
    }
}

function initControls() {
    // View Toggle
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    const viewer = document.getElementById('diff-container');
    
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const view = btn.getAttribute('data-view');
            
            viewer.classList.remove('view-split', 'view-unified');
            viewer.classList.add(`view-${view}`);
            
            // Re-sync scroll positions
            document.getElementById('diff-content-b').scrollTop = document.getElementById('diff-content-a').scrollTop;
        });
    });
    
    // Copy Diff
    document.getElementById('btn-copy-diff').addEventListener('click', function() {
        const lines = Array.from(document.getElementById('diff-content-a').querySelectorAll('.diff-line'));
        const linesB = Array.from(document.getElementById('diff-content-b').querySelectorAll('.diff-line'));
        
        let textToCopy = '';
        lines.forEach((line, i) => {
            const aContent = line.querySelector('.line-content').innerText;
            const bContent = linesB[i] ? linesB[i].querySelector('.line-content').innerText : '';
            
            if(line.classList.contains('added')) {
                textToCopy += `+ ${bContent}\n`;
            } else if(line.classList.contains('removed')) {
                textToCopy += `- ${aContent}\n`;
            } else if(line.classList.contains('modified')) {
                textToCopy += `~ ${bContent}\n`;
            } else {
                textToCopy += `  ${aContent}\n`;
            }
        });
        
        navigator.clipboard.writeText(textToCopy).then(() => {
            const originalText = this.innerHTML;
            this.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!`;
            setTimeout(() => {
                this.innerHTML = originalText;
            }, 2000);
        });
    });
    
    // Download Report
    document.getElementById('btn-download-report').addEventListener('click', () => {
        alert("Report downloading would be handled by the backend endpoint return or client-side PDF generation.");
        // We can wire it to generate a text report client-side.
    });
    
    // Search
    document.getElementById('diff-search').addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        const linesA = document.getElementById('diff-content-a').querySelectorAll('.diff-line');
        const linesB = document.getElementById('diff-content-b').querySelectorAll('.diff-line');
        
        linesA.forEach((line, i) => {
            const aText = line.innerText.toLowerCase();
            const bText = linesB[i] ? linesB[i].innerText.toLowerCase() : '';
            
            if(aText.includes(query) || bText.includes(query)) {
                line.style.display = 'flex';
                if(linesB[i]) linesB[i].style.display = 'flex';
            } else {
                line.style.display = 'none';
                if(linesB[i]) linesB[i].style.display = 'none';
            }
        });
    });
}
