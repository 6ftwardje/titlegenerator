// Global variables
let currentVideoFile = null;
let currentTranscript = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {
    // Initialize clickbait slider
    const clickbaitSlider = document.getElementById('clickbait');
    const clickbaitValue = document.getElementById('clickbait-value');

    clickbaitSlider.addEventListener('input', function () {
        clickbaitValue.textContent = this.value;
    });

    // Initialize file upload
    initializeFileUpload();

    // Initialize drag and drop
    initializeDragAndDrop();
}

function initializeFileUpload() {
    const fileInput = document.getElementById('video-upload');
    const uploadArea = document.getElementById('file-upload-area');

    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    // Make upload area clickable
    uploadArea.addEventListener('click', function () {
        fileInput.click();
    });
}

function initializeDragAndDrop() {
    const uploadArea = document.getElementById('file-upload-area');

    uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#00ffff';
        uploadArea.style.background = 'rgba(0, 212, 255, 0.15)';
    });

    uploadArea.addEventListener('dragleave', function (e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#00d4ff';
        uploadArea.style.background = 'rgba(0, 212, 255, 0.05)';
    });

    uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#00d4ff';
        uploadArea.style.background = 'rgba(0, 212, 255, 0.05)';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (isValidVideoFile(file)) {
                handleFileUpload(file);
            } else {
                showNotification('Alleen video bestanden (.mp4, .mov, .m4v) zijn toegestaan.', 'error');
            }
        }
    });
}

function isValidVideoFile(file) {
    const validTypes = ['video/mp4', 'video/quicktime', 'video/x-m4v'];
    const validExtensions = ['.mp4', '.mov', '.m4v'];

    return validTypes.includes(file.type) ||
        validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
}

function handleFileUpload(file) {
    // Check file size before processing
    const fileSizeMB = Math.round(file.size / (1024 * 1024));
    
    if (fileSizeMB > 25) {
        showFileSizeError(fileSizeMB);
        return;
    }

    currentVideoFile = file;

    // Show video preview
    const videoPreview = document.getElementById('video-preview');
    const videoPlayer = document.getElementById('video-player');
    const fileUploadArea = document.getElementById('file-upload-area');

    // Create video URL
    const videoURL = URL.createObjectURL(file);
    videoPlayer.src = videoURL;

    // Show preview, hide upload area
    fileUploadArea.style.display = 'none';
    videoPreview.style.display = 'block';

    showNotification(`Video "${file.name}" succesvol geüpload! (${fileSizeMB}MB)`, 'success');
}

function showFileSizeError(fileSizeMB) {
    const errorMessage = `Video bestand is te groot (${fileSizeMB}MB). Maximum grootte is 25MB.

Om je video te verwerken:
1. Comprimeer de video naar onder 25MB
2. Extraheer alleen audio (veel kleiner)
3. Gebruik een video compressie tool zoals HandBrake of FFmpeg
4. Overweeg om lange video's op te splitsen in kortere segmenten

Aanbevolen: Extraheer audio als MP3 (meestal 5-15MB voor typische video's)`;

    // Create a modal with file size guidance
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 600px; text-align: left;">
            <h3 style="color: #ef4444; margin-bottom: 1rem;">
                <i class="fas fa-exclamation-triangle"></i> Bestand te groot
            </h3>
            <div style="margin-bottom: 1.5rem;">
                <p><strong>Huidige bestandsgrootte:</strong> ${fileSizeMB}MB</p>
                <p><strong>Maximum toegestaan:</strong> 25MB</p>
            </div>
            <div style="background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <h4 style="color: #ef4444; margin-bottom: 0.5rem;">Oplossingen:</h4>
                <ul style="margin: 0; padding-left: 1.5rem;">
                    <li>Comprimeer de video naar onder 25MB</li>
                    <li>Extraheer alleen audio (veel kleiner)</li>
                    <li>Gebruik HandBrake, FFmpeg of online tools</li>
                    <li>Splits lange video's op in kortere segmenten</li>
                </ul>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <h4 style="color: #10b981; margin-bottom: 0.5rem;">Aanbeveling:</h4>
                <p style="margin: 0;">Extraheer audio als MP3 - meestal 5-15MB voor typische video's</p>
            </div>
            <button onclick="this.closest('.modal').remove()" class="generate-btn" style="width: 100%;">
                <i class="fas fa-check"></i> Begrepen
            </button>
        </div>
    `;

    document.body.appendChild(modal);
}

async function processVideo() {
    if (!currentVideoFile) {
        showNotification('Geen video bestand geselecteerd.', 'error');
        return;
    }

    showLoadingModal('Audio extraheren en transcriberen...');

    try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('video', currentVideoFile);

        // Call Netlify function for transcription
        const response = await fetch('/.netlify/functions/transcribe-video', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.success) {
            currentTranscript = result.transcript;
            
            // Show transcript section
            const transcriptContainer = document.getElementById('transcript-container');
            const transcriptText = document.getElementById('transcript-text');

            transcriptText.value = result.transcript;
            transcriptContainer.style.display = 'block';

            showNotification('Transcript succesvol gegenereerd!', 'success');
            transcriptContainer.scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(result.error || 'Transcript kon niet worden gegenereerd');
        }

    } catch (error) {
        console.error('Transcription error:', error);
        
        // Check if it's a file size error
        if (error.message.includes('25MB') || error.message.includes('te groot')) {
            showFileSizeError(Math.round(currentVideoFile.size / (1024 * 1024)));
        } else {
            showNotification(`Fout bij transcriberen: ${error.message}`, 'error');
        }
        
        // Fallback to mock transcript for demo purposes
        const mockTranscript = generateMockTranscript();
        currentTranscript = mockTranscript;
        
        const transcriptContainer = document.getElementById('transcript-container');
        const transcriptText = document.getElementById('transcript-text');
        
        transcriptText.value = mockTranscript;
        transcriptContainer.style.display = 'block';
        
        showNotification('Transcript gegenereerd (demo modus)', 'info');
        transcriptContainer.scrollIntoView({ behavior: 'smooth' });
    } finally {
        hideLoadingModal();
    }
}

function generateMockTranscript() {
    const mockTranscripts = [
        "Goedemiddag allemaal, welkom bij deze nieuwe marktupdate. Ik zie dat Bitcoin vandaag weer flink in beweging is gekomen. We zitten momenteel rond de 43.000 dollar niveau, wat een belangrijke steun/resistentie zone is. De technische analyse laat zien dat we mogelijk een breakout kunnen verwachten in de komende dagen. Let goed op het volume en de RSI indicator.",

        "Hallo traders, hier is je dagelijkse crypto update. Ethereum heeft vandaag een sterke rally laten zien en breekt door het 2.500 dollar niveau. Dit is een bullish signaal dat suggereert dat we mogelijk naar 3.000 dollar kunnen gaan. De MACD indicator bevestigt deze trend. Houd je stop loss dicht bij de hand.",

        "Welkom bij deze trade breakdown. Ik heb vandaag een interessante setup gezien in de Solana chart. We hebben een perfecte bullish flag pattern die zich heeft gevormd na de recente pullback. De prijs test momenteel de trendline support en als deze houdt, kunnen we een mooie bounce naar boven verwachten. Risico-reward ratio is ongeveer 1:3."
    ];

    return mockTranscripts[Math.floor(Math.random() * mockTranscripts.length)];
}

async function generateContent() {
    if (!currentTranscript) {
        showNotification('Geen transcript beschikbaar.', 'error');
        return;
    }

    showLoadingModal('Titel en beschrijving genereren...');

    try {
        // Get user preferences
        const preferences = getUserPreferences();

        // Call Netlify function for content generation
        const response = await fetch('/.netlify/functions/generate-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                transcript: currentTranscript,
                preferences: preferences
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        if (result.success) {
            // Display results
            displayResults(result.content);
            showNotification('Content succesvol gegenereerd!', 'success');
        } else {
            throw new Error(result.error || 'Content kon niet worden gegenereerd');
        }

    } catch (error) {
        console.error('Content generation error:', error);
        showNotification(`Fout bij genereren: ${error.message}`, 'error');
        
        // Fallback to mock content for demo purposes
        const preferences = getUserPreferences();
        const generatedContent = generateMockContent(currentTranscript, preferences);
        displayResults(generatedContent);
        showNotification('Content gegenereerd (demo modus)', 'info');
    } finally {
        hideLoadingModal();
        
        // Scroll to results
        document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
    }
}

function getUserPreferences() {
    return {
        platforms: Array.from(document.getElementById('platforms').selectedOptions).map(opt => opt.value),
        clickbaitLevel: parseInt(document.getElementById('clickbait').value),
        language: document.getElementById('language').value,
        useEmojis: document.getElementById('use-emojis').checked,
        useHashtags: document.getElementById('use-hashtags').checked,
        topicHint: document.getElementById('topic-hint').value,
        extraHashtags: document.getElementById('extra-hashtags').value
    };
}

function generateMockContent(transcript, preferences) {
    const clickbaitLevel = preferences.clickbaitLevel;
    const useEmojis = preferences.useEmojis;
    const useHashtags = preferences.useHashtags;

    // Generate title based on clickbait level
    let title = generateMockTitle(transcript, clickbaitLevel, useEmojis);

    // Generate description
    let description = generateMockDescription(transcript, preferences);

    // Generate hashtags
    let hashtags = [];
    if (useHashtags) {
        hashtags = generateMockHashtags(preferences.extraHashtags);
    }

    return { title, description, hashtags };
}

function generateMockTitle(transcript, clickbaitLevel, useEmojis) {
    const emoji = useEmojis ? '🚨 ' : '';

    if (clickbaitLevel <= 2) {
        return emoji + "Marktupdate: Bitcoin bewegingen en technische analyse";
    } else if (clickbaitLevel <= 5) {
        return emoji + "BREAKING: Bitcoin breekt door belangrijk niveau - wat nu?";
    } else if (clickbaitLevel <= 8) {
        return emoji + "🚨 KRITIEK: Bitcoin staat op het punt van een MASSIEVE beweging!";
    } else {
        return emoji + "🚨🚨🚨 ALARM: Bitcoin gaat EXPLODEREN - mis dit NIET!";
    }
}

function generateMockDescription(transcript, preferences) {
    const language = preferences.language;
    const useEmojis = preferences.useEmojis;

    if (language === 'nl') {
        let desc = "In deze video bespreek ik de laatste ontwikkelingen in de crypto markt.\n\n";
        desc += "🔍 Belangrijkste inzichten:\n";
        desc += "• Technische analyse van Bitcoin en Ethereum\n";
        desc += "• Marktsentiment en volume analyse\n";
        desc += "• Toekomstige prijsdoelen en risico's\n\n";
        desc += "💡 Wat betekent dit voor jouw portfolio?\n";
        desc += "Deze bewegingen kunnen grote impact hebben op je crypto holdings. Blijf op de hoogte van de laatste ontwikkelingen.\n\n";
        desc += "📈 Volg voor meer dagelijkse updates en trade breakdowns!";

        return useEmojis ? desc : desc.replace(/[🔍💡📈]/g, '');
    } else {
        let desc = "In this video, I discuss the latest developments in the crypto market.\n\n";
        desc += "🔍 Key insights:\n";
        desc += "• Technical analysis of Bitcoin and Ethereum\n";
        desc += "• Market sentiment and volume analysis\n";
        desc += "• Future price targets and risks\n\n";
        desc += "💡 What does this mean for your portfolio?\n";
        desc += "These movements can have a major impact on your crypto holdings. Stay updated on the latest developments.\n\n";
        desc += "📈 Follow for more daily updates and trade breakdowns!";

        return useEmojis ? desc : desc.replace(/[🔍💡📈]/g, '');
    }
}

function generateMockHashtags(extraHashtags) {
    const baseHashtags = ['#crypto', '#bitcoin', '#altcoins', '#forex', '#trading'];
    const extra = extraHashtags.split(',').map(h => h.trim()).filter(h => h);

    return [...baseHashtags, ...extra].slice(0, 10);
}

function displayResults(content) {
    // Show results section
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';

    // Set title
    document.getElementById('generated-title').value = content.title;

    // Set description
    document.getElementById('generated-description').value = content.description;

    // Set hashtags if available
    if (content.hashtags && content.hashtags.length > 0) {
        const hashtagsCard = document.getElementById('hashtags-card');
        const hashtagsText = document.getElementById('generated-hashtags');

        hashtagsText.value = content.hashtags.join(' ');
        hashtagsCard.style.display = 'block';
    }
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.value || element.textContent;

    navigator.clipboard.writeText(text).then(() => {
        showNotification('Gekopieerd naar klembord!', 'success');
    }).catch(() => {
        // Fallback for older browsers
        element.select();
        document.execCommand('copy');
        showNotification('Gekopieerd naar klembord!', 'success');
    });
}

function downloadText(elementId, filename) {
    const element = document.getElementById(elementId);
    const text = element.value || element.textContent;

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
    showNotification('Download gestart!', 'success');
}

function showLoadingModal(text) {
    const modal = document.getElementById('loading-modal');
    const loadingText = document.getElementById('loading-text');

    loadingText.textContent = text;
    modal.style.display = 'flex';
}

function hideLoadingModal() {
    const modal = document.getElementById('loading-modal');
    modal.style.display = 'none';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1001;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
    `;

    // Add to page
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Add notification styles to head
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .notification-content i {
        font-size: 1.2rem;
    }
`;
document.head.appendChild(notificationStyles);
