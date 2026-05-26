/* ----------------------------------------------------
   RealityCheck AI JS Engine - Premium SPA Controller
---------------------------------------------------- */

document.addEventListener("DOMContentLoaded", () => {
    // API Configuration
    let API_BASE = window.location.origin;
    if (
        window.location.protocol === "file:" ||
        ((window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") && window.location.port !== "8000")
    ) {
        API_BASE = "http://127.0.0.1:8000";
    }

    // Selectors & Elements
    const canvas = document.getElementById("particles-canvas");
    const themeToggleBtn = document.getElementById("theme-toggle");
    const tabUrlBtn = document.getElementById("tab-url-btn");
    const tabTextBtn = document.getElementById("tab-text-btn");
    const contentUrl = document.getElementById("content-url");
    const contentText = document.getElementById("content-text");
    const scanUrlInput = document.getElementById("scan-url");
    const scanTextInput = document.getElementById("scan-text");
    const charCounter = document.getElementById("text-char-counter");
    const analyzeBtn = document.getElementById("analyze-submit-btn");
    const errorBanner = document.getElementById("error-banner");
    const errorMessage = document.getElementById("error-message");
    const errorCloseBtn = document.getElementById("error-close-btn");

    // Output Elements
    const loadingDeck = document.getElementById("analysis-loading-deck");
    const loadingSubtext = document.getElementById("loading-subtext");
    const resultsDeck = document.getElementById("analysis-results-deck");
    const scoreCircle = document.getElementById("results-score-circle");
    const scoreValue = document.getElementById("results-score-value");
    const scoreBadge = document.getElementById("results-score-badge");
    const fakeProbValue = document.getElementById("results-fake-prob");
    const fakeBarFill = document.getElementById("results-fake-bar");
    const biasTypeVal = document.getElementById("results-bias-type");
    const biasDescVal = document.getElementById("results-bias-desc");
    
    // Bias Pills
    const pillNeutral = document.getElementById("pill-neutral");
    const pillSensational = document.getElementById("pill-sensational");
    const pillPolarized = document.getElementById("pill-polarized");

    // Detail Display Panels
    const highlightsBadge = document.getElementById("results-highlights-badge");
    const highlightedTextBlock = document.getElementById("results-highlighted-text");
    const sourceLabel = document.getElementById("results-source-label");
    const lengthLabel = document.getElementById("results-length-label");
    const explanationsList = document.getElementById("results-explanations-list");

    // Sidebar Elements
    const historyList = document.getElementById("history-items-list");
    const historyCount = document.getElementById("history-count");
    const clearHistoryBtn = document.getElementById("clear-history-btn");

    // Application state
    let activeTab = "url"; // or 'text'
    let analysisHistory = [];

    // --------------------------------------------------------
    // 1. Dynamic Canvas Particle System
    // --------------------------------------------------------
    let particles = [];
    const ctx = canvas.getContext("2d");

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 1.5 + 0.5;
            this.speedX = Math.random() * 0.15 - 0.075;
            this.speedY = Math.random() * 0.15 - 0.075;
            this.alpha = Math.random() * 0.5 + 0.1;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Bounce boundary checks
            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
        }

        draw() {
            const isLightTheme = document.body.classList.contains("light-theme");
            ctx.save();
            ctx.globalAlpha = this.alpha;
            // Shift particle color based on current active theme
            ctx.fillStyle = isLightTheme ? "rgba(99, 102, 241, 0.4)" : "rgba(6, 182, 212, 0.4)";
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }

    function initParticles() {
        particles = [];
        const count = Math.min(Math.floor(canvas.width / 15), 80);
        for (let i = 0; i < count; i++) {
            particles.push(new Particle());
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animateParticles);
    }

    initParticles();
    animateParticles();

    // --------------------------------------------------------
    // 2. Dark/Light Theme Manager
    // --------------------------------------------------------
    const cachedTheme = localStorage.getItem("realitycheck-theme");
    if (cachedTheme === "light") {
        document.body.classList.add("light-theme");
        themeToggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
    }

    themeToggleBtn.addEventListener("click", () => {
        document.body.classList.toggle("light-theme");
        const activeTheme = document.body.classList.contains("light-theme") ? "light" : "dark";
        localStorage.setItem("realitycheck-theme", activeTheme);
        themeToggleBtn.innerHTML = activeTheme === "light" 
            ? '<i class="fa-solid fa-sun"></i>' 
            : '<i class="fa-solid fa-moon"></i>';
    });

    // --------------------------------------------------------
    // 3. Tab Navigation Controls
    // --------------------------------------------------------
    tabUrlBtn.addEventListener("click", () => {
        activeTab = "url";
        tabUrlBtn.classList.add("active");
        tabTextBtn.classList.remove("active");
        contentUrl.classList.add("active");
        contentText.classList.remove("active");
        hideError();
    });

    tabTextBtn.addEventListener("click", () => {
        activeTab = "text";
        tabTextBtn.classList.add("active");
        tabUrlBtn.classList.remove("active");
        contentText.classList.add("active");
        contentUrl.classList.remove("active");
        hideError();
    });

    // Dynamic character validation counter
    scanTextInput.addEventListener("input", () => {
        const charsCount = scanTextInput.value.length;
        charCounter.textContent = `${charsCount} character${charsCount === 1 ? "" : "s"}`;
    });

    // --------------------------------------------------------
    // 4. Alert & Error Banner Helper
    // --------------------------------------------------------
    function showError(msg) {
        errorMessage.textContent = msg;
        errorBanner.style.display = "flex";
        errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function hideError() {
        errorBanner.style.display = "none";
    }

    errorCloseBtn.addEventListener("click", hideError);

    // --------------------------------------------------------
    // 5. Submit Form Verification Request
    // --------------------------------------------------------
    analyzeBtn.addEventListener("click", async () => {
        hideError();

        // Build Payload according to the active tab
        const payload = {};
        if (activeTab === "url") {
            const rawUrl = scanUrlInput.value.trim();
            if (!rawUrl) {
                showError("Please enter a valid target URL article to proceed.");
                return;
            }
            if (!rawUrl.startsWith("http://") && !rawUrl.startsWith("https://")) {
                showError("URL link must begin with 'http://' or 'https://'.");
                return;
            }
            payload.url = rawUrl;
        } else {
            const rawText = scanTextInput.value.trim();
            if (!rawText) {
                showError("Please enter news block content or paragraph text to evaluate.");
                return;
            }
            if (rawText.length < 30) {
                showError(`Content block is too brief (${rawText.length} characters). Please enter at least 30 characters for valid parsing.`);
                return;
            }
            payload.text = rawText;
        }

        // Lock form UI
        analyzeBtn.disabled = true;
        document.querySelector(".btn-text").classList.add("hidden");
        document.querySelector(".btn-loader").classList.remove("hidden");
        
        // Open Dashboard loader
        resultsDeck.classList.add("hidden");
        loadingDeck.classList.remove("hidden");
        updateLoadingText();

        const loadingTexts = [
            "Contacting analysis servers...",
            "Resolving publisher registry database...",
            "Crawling sentence and paragraph blocks...",
            "Running heuristic clickbait pattern matchers...",
            "Calculating extreme tone punctuation ratios...",
            "Constructing linguistic credibility scores..."
        ];
        let loaderCycleIdx = 0;
        const loaderInterval = setInterval(() => {
            if (loadingDeck.classList.contains("hidden")) {
                clearInterval(loaderInterval);
                return;
            }
            loadingSubtext.textContent = loadingTexts[loaderCycleIdx % loadingTexts.length];
            loaderCycleIdx++;
        }, 1200);

        try {
            const response = await fetch(`${API_BASE}/analyze`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const responseData = await response.json();

            if (!response.ok) {
                throw new Error(responseData.detail || "Server error during natural language processing.");
            }

            // Render output
            setTimeout(() => {
                clearInterval(loaderInterval);
                renderResults(responseData.data);
                saveHistory(responseData.data);
                
                // Reset loading panel
                loadingDeck.classList.add("hidden");
                resultsDeck.classList.remove("hidden");
                
                // Unlock submit buttons
                analyzeBtn.disabled = false;
                document.querySelector(".btn-text").classList.remove("hidden");
                document.querySelector(".btn-loader").classList.add("hidden");

                resultsDeck.scrollIntoView({ behavior: "smooth" });
            }, 600);

        } catch (error) {
            clearInterval(loaderInterval);
            loadingDeck.classList.add("hidden");
            analyzeBtn.disabled = false;
            document.querySelector(".btn-text").classList.remove("hidden");
            document.querySelector(".btn-loader").classList.add("hidden");
            showError(error.message);
        }
    });

    function updateLoadingText() {
        loadingSubtext.textContent = "Executing text pattern crawlers and scoring grammar structures...";
    }

    // --------------------------------------------------------
    // 6. Output Presentation & Micro-Animations
    // --------------------------------------------------------
    function renderResults(data) {
        // A. Score Circular Gauge count-up
        const score = data.score;
        let counter = 0;
        const speed = 15; // ms per frame
        
        // Calculate dynamic SVG fill offset
        // dasharray is 314
        const maxOffset = 314;
        
        // Start dial anim
        scoreCircle.style.strokeDashoffset = maxOffset;
        scoreValue.textContent = "0";

        const countInterval = setInterval(() => {
            if (counter >= score) {
                clearInterval(countInterval);
                scoreValue.textContent = score;
                scoreCircle.style.strokeDashoffset = maxOffset - (maxOffset * score) / 100;
            } else {
                counter++;
                scoreValue.textContent = counter;
                scoreCircle.style.strokeDashoffset = maxOffset - (maxOffset * counter) / 100;
            }
        }, speed);

        // Update Score Level Badge
        scoreBadge.className = "score-status-indicator";
        if (score >= 70) {
            scoreBadge.textContent = "Highly Credible";
            scoreBadge.classList.add("credible");
        } else if (score >= 40) {
            scoreBadge.textContent = "Mixed/Caution";
            scoreBadge.classList.add("warning");
        } else {
            scoreBadge.textContent = "Low Credibility";
            scoreBadge.classList.add("fake");
        }

        // B. Fake Probability Metric
        fakeProbValue.innerHTML = `${data.fake_probability.toFixed(1)}<span class="unit">%</span>`;
        fakeBarFill.style.width = `${data.fake_probability}%`;

        // C. Bias Classification Spectrum
        biasTypeVal.textContent = data.bias;
        
        // Reset and apply proper pill highlighting
        pillNeutral.className = "bias-pill";
        pillSensational.className = "bias-pill";
        pillPolarized.className = "bias-pill";

        if (data.bias === "Neutral") {
            biasDescVal.textContent = "Neutral, objective factual grammar. Devoid of highly emotional clickbait or editorial slants.";
            pillNeutral.classList.add("active-neutral");
        } else if (data.bias === "Sensationalist") {
            biasDescVal.textContent = "Sensationalized adjectives and hyperbole designed to stir curiosity or surprise.";
            pillSensational.classList.add("active-sensational");
        } else {
            biasDescVal.textContent = "Highly polarized opinionated slant, extreme punctuation, or capitalized emotional phrases.";
            pillPolarized.classList.add("active-polarized");
        }

        // D. Highlights Text Map rendering
        // Crucial logic: Descending character index slice injections to prevent offset drifting!
        const raw = data.raw_text;
        const highlights = [...data.highlights];
        
        // Sort in descending order of starting character index
        highlights.sort((a, b) => b.start_idx - a.start_idx);

        let highlightedHtml = raw;

        highlights.forEach(item => {
            const start = item.start_idx;
            const end = item.end_idx;
            
            // Re-slice and wrap highlighted tag
            const before = highlightedHtml.substring(0, start);
            const flagged = highlightedHtml.substring(start, end);
            const after = highlightedHtml.substring(end);

            highlightedHtml = `${before}<span class="nlp-highlight category-${item.category}" data-tooltip="${item.explanation}">${flagged}</span>${after}`;
        });

        highlightedTextBlock.innerHTML = highlightedHtml;
        highlightsBadge.textContent = `${data.highlights.length} Flagged Phrase${data.highlights.length === 1 ? "" : "s"}`;

        // E. Detailed Explanations checklists
        explanationsList.innerHTML = "";
        
        // Metadata values
        sourceLabel.textContent = data.source;
        lengthLabel.textContent = `${data.word_count} words`;

        // Check if there are warning checklist items
        data.explanations.forEach(exp => {
            const card = document.createElement("div");
            card.className = "explanation-card-item";

            const iconSpan = document.createElement("span");
            iconSpan.className = "explanation-item-icon";
            
            // Choose icon color depending on contents
            if (exp.includes("Highly Polarized") || exp.includes("reputation") || exp.includes("known unreliable") || exp.includes("banned") || exp.includes("Fake News")) {
                iconSpan.innerHTML = '<i class="fa-solid fa-circle-radiation"></i>';
                iconSpan.classList.add("danger-type");
            } else if (exp.includes("sensationalist") || exp.includes("clickbait") || exp.includes("exclamation") || exp.includes("capitalization") || exp.includes("very short") || exp.includes("brief")) {
                iconSpan.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
                iconSpan.classList.add("warning-type");
            } else {
                iconSpan.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                iconSpan.classList.add("success-type");
            }

            const textSpan = document.createElement("span");
            textSpan.className = "explanation-item-text";
            textSpan.textContent = exp;

            card.appendChild(iconSpan);
            card.appendChild(textSpan);
            explanationsList.appendChild(card);
        });
    }

    // --------------------------------------------------------
    // 7. LocalStorage Caching & Sidebar History Logs
    // --------------------------------------------------------
    function loadHistory() {
        const cached = localStorage.getItem("realitycheck-history");
        if (cached) {
            try {
                analysisHistory = JSON.parse(cached);
            } catch (e) {
                analysisHistory = [];
            }
        } else {
            analysisHistory = [];
        }
        renderHistoryList();
    }

    function saveHistory(item) {
        // Prevent duplicate logs (if source or text is identical)
        const isDuplicate = analysisHistory.some(prev => 
            (prev.source === item.source && prev.raw_text === item.raw_text)
        );

        if (isDuplicate) return;

        // Bundle item, keep only a quick preview title
        const headlinePreview = item.raw_text.split("\n")[0].substring(0, 75) + "...";
        
        const historyItem = {
            id: Date.now().toString(),
            title: headlinePreview,
            source: item.source,
            score: item.score,
            raw: item // Embed complete result structure so we can reload it instantly!
        };

        // Add to front of log array, cap at 10 items
        analysisHistory.unshift(historyItem);
        if (analysisHistory.length > 10) {
            analysisHistory.pop();
        }

        localStorage.setItem("realitycheck-history", JSON.stringify(analysisHistory));
        renderHistoryList();
    }

    function renderHistoryList() {
        historyCount.textContent = analysisHistory.length;
        historyList.innerHTML = "";

        if (analysisHistory.length === 0) {
            historyList.innerHTML = `
                <div class="empty-history">
                    <i class="fa-solid fa-folder-open"></i>
                    <p>No recent analyses. Scanned texts will appear here.</p>
                </div>
            `;
            clearHistoryBtn.style.display = "none";
            return;
        }

        clearHistoryBtn.style.display = "flex";

        analysisHistory.forEach(item => {
            const card = document.createElement("div");
            card.className = "history-card";
            card.setAttribute("data-id", item.id);

            let pillClass = "credible";
            if (item.score < 40) pillClass = "fake";
            else if (item.score < 70) pillClass = "warning";

            card.innerHTML = `
                <div class="history-card-header">
                    <span class="history-source"><i class="fa-regular fa-bookmark"></i> ${item.source}</span>
                    <span class="history-score-pill ${pillClass}">${item.score}%</span>
                </div>
                <div class="history-title">${item.title}</div>
            `;

            // Card Click Event - reload history instantly
            card.addEventListener("click", () => {
                hideError();
                renderResults(item.raw.raw ? item.raw.raw : item.raw);
                resultsDeck.classList.remove("hidden");
                resultsDeck.scrollIntoView({ behavior: "smooth" });
            });

            historyList.appendChild(card);
        });
    }

    // Clear history action
    clearHistoryBtn.addEventListener("click", () => {
        analysisHistory = [];
        localStorage.removeItem("realitycheck-history");
        renderHistoryList();
        hideError();
    });

    // Initialize sidebar loader
    loadHistory();
});
