/**
 * Text Summarization Dashboard - Frontend JavaScript
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000';
const DEBOUNCE_DELAY = 300;

// DOM Elements
const inputText = document.getElementById('inputText');
const summarizeBtn = document.getElementById('summarizeBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');
const summaryDiv = document.getElementById('summary');
const loadingIndicator = document.getElementById('loadingIndicator');
const alertContainer = document.getElementById('alertContainer');

const minLengthSlider = document.getElementById('minLength');
const maxLengthSlider = document.getElementById('maxLength');
const minLengthValue = document.getElementById('minLengthValue');
const maxLengthValue = document.getElementById('maxLengthValue');
const lengthRange = document.getElementById('lengthRange');

const inputWordCount = document.getElementById('inputWordCount');
const statInputWords = document.getElementById('statInputWords');
const statSummaryWords = document.getElementById('statSummaryWords');
const statCompressionRatio = document.getElementById('statCompressionRatio');
const statInputTokens = document.getElementById('statInputTokens');
const statSummaryTokens = document.getElementById('statSummaryTokens');

// State variables
let lastSummaryResult = null;

/**
 * Show loading indicator
 */
function showLoading() {
    loadingIndicator.style.display = 'flex';
    summarizeBtn.disabled = true;
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    loadingIndicator.style.display = 'none';
    summarizeBtn.disabled = false;
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertId = 'alert-' + Date.now();
    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.id = alertId;
    alert.innerHTML = `
        <span class="alert-icon">${icons[type]}</span>
        <span class="alert-text">${message}</span>
        <button class="alert-close" onclick="document.getElementById('${alertId}').remove()">×</button>
    `;

    alertContainer.appendChild(alert);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        const element = document.getElementById(alertId);
        if (element) {
            element.remove();
        }
    }, 5000);
}

/**
 * Update word count from input text
 */
function updateWordCount() {
    const text = inputText.value.trim();
    const words = text.length > 0 ? text.split(/\s+/).length : 0;
    inputWordCount.textContent = `${words} word${words !== 1 ? 's' : ''}`;
}

/**
 * Debounce function
 */
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Update slider displays
 */
function updateSliderDisplays() {
    const minLen = parseInt(minLengthSlider.value);
    const maxLen = parseInt(maxLengthSlider.value);

    // Ensure min is less than max
    if (minLen >= maxLen) {
        if (event.target === minLengthSlider) {
            maxLengthSlider.value = minLen + 50;
        } else {
            minLengthSlider.value = maxLen - 50;
        }
    }

    minLengthValue.textContent = minLengthSlider.value;
    maxLengthValue.textContent = maxLengthSlider.value;
    lengthRange.textContent = `${minLengthSlider.value} - ${maxLengthSlider.value}`;
}

/**
 * Validate input text
 */
function validateInput(text) {
    const trimmed = text.trim();

    if (!trimmed) {
        showAlert('Please enter some text to summarize', 'warning');
        return false;
    }

    const wordCount = trimmed.split(/\s+/).length;
    if (wordCount < 10) {
        showAlert('Text must contain at least 10 words', 'warning');
        return false;
    }

    return true;
}

/**
 * Make API call to summarize text
 */
async function summarizeText() {
    const text = inputText.value;

    if (!validateInput(text)) {
        return;
    }

    const minLen = parseInt(minLengthSlider.value);
    const maxLen = parseInt(maxLengthSlider.value);

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                min_length: minLen,
                max_length: maxLen
            })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
            displaySummary(data);
            showAlert('Summary generated successfully!', 'success');
        } else {
            showAlert(`Error: ${data.message || 'Failed to generate summary'}`, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert(`Network error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Display summary and update statistics
 */
function displaySummary(result) {
    lastSummaryResult = result;

    // Update summary text
    summaryDiv.innerHTML = `<p>${result.summary}</p>`;
    copyBtn.style.display = 'inline-flex';

    // Update statistics
    statInputWords.textContent = result.input_length;
    statSummaryWords.textContent = result.summary_length;
    statCompressionRatio.textContent = `${result.compression_ratio}x`;
    statInputTokens.textContent = result.input_tokens;
    statSummaryTokens.textContent = result.summary_tokens;

    // Scroll to summary
    document.querySelector('.output-section').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Clear all inputs and outputs
 */
function clearAll() {
    inputText.value = '';
    summaryDiv.innerHTML = '<p class="placeholder">Your summary will appear here...</p>';
    copyBtn.style.display = 'none';
    inputWordCount.textContent = '0 words';

    statInputWords.textContent = '0';
    statSummaryWords.textContent = '0';
    statCompressionRatio.textContent = '0x';
    statInputTokens.textContent = '0';
    statSummaryTokens.textContent = '0';

    lastSummaryResult = null;
    inputText.focus();
}

/**
 * Copy summary to clipboard
 */
async function copySummary() {
    if (!lastSummaryResult) {
        showAlert('No summary to copy', 'warning');
        return;
    }

    try {
        await navigator.clipboard.writeText(lastSummaryResult.summary);
        showAlert('Summary copied to clipboard!', 'success');
    } catch (error) {
        showAlert(`Failed to copy: ${error.message}`, 'error');
    }
}

/**
 * Event Listeners
 */

// Input text event listeners
inputText.addEventListener('input', updateWordCount);

// Slider event listeners
minLengthSlider.addEventListener('input', updateSliderDisplays);
maxLengthSlider.addEventListener('input', updateSliderDisplays);

// Button event listeners
summarizeBtn.addEventListener('click', summarizeText);
clearBtn.addEventListener('click', clearAll);
copyBtn.addEventListener('click', copySummary);

// Allow Enter key to summarize (Ctrl+Enter)
inputText.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        summarizeText();
    }
});

/**
 * Initialize dashboard
 */
function initializeDashboard() {
    console.log('Initializing Text Summarization Dashboard...');
    updateWordCount();
    updateSliderDisplays();

    // Check API connectivity
    fetch(`${API_BASE_URL}/health`)
        .then(response => {
            if (response.ok) {
                console.log('✓ Connected to backend API');
                return response.json();
            } else {
                throw new Error('Backend not responding');
            }
        })
        .then(data => {
            if (data.model_loaded) {
                showAlert('✓ Ready to summarize text!', 'success');
            }
        })
        .catch(error => {
            console.error('Connection error:', error);
            showAlert('⚠ Cannot connect to backend. Make sure the Flask server is running on http://localhost:5000', 'warning');
            summarizeBtn.disabled = true;
        });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeDashboard);

// Export functions for debugging
window.debugSummarizer = {
    showAlert,
    summarizeText,
    clearAll,
    copySummary
};
