# Text Summarization Dashboard

A web-based dashboard for accurate text summarization using advanced AI models. Transform long texts into concise summaries with adjustable parameters.

![Dashboard](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.3+-red)

## 🌟 Features

- **AI-Powered Summarization**: Uses `facebook/bart-large-cnn` transformer model for accurate summaries
- **Interactive Dashboard**: Clean, modern web interface with real-time feedback
- **Adjustable Parameters**: Control summary length with min/max token sliders
- **Live Statistics**: Track compression ratio, word counts, and token usage
- **Copy to Clipboard**: Easy sharing of generated summaries
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Batch Processing**: Summarize multiple texts programmatically via API
- **Error Handling**: Comprehensive validation and user-friendly error messages

## 📋 Requirements

- Python 3.8+
- Flask 2.3+
- Transformers 4.30+
- PyTorch 2.0+
- NumPy, Pandas, Scikit-learn
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd c:\Users\pooje\Desktop\Text_Summarization
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

> **Note**: First-time setup will download the BART model (~1.5GB). This may take a few minutes.

### 3. Start the Backend Server

```bash
cd backend
python app.py
```

You should see output like:
```
 * Running on http://0.0.0.0:5000
 * WARNING in production, do not use the development server
```

### 4. Open the Frontend

1. Navigate to the `frontend` folder
2. Open `index.html` in your web browser
3. Or use a local server:

```bash
cd frontend
python -m http.server 8000
```

Then visit: `http://localhost:8000`

## 📊 Project Structure

```
Text_Summarization/
├── backend/
│   ├── app.py                 # Flask application & API endpoints
│   ├── summarizer.py          # Summarization logic & model handling
│   └── requirements.txt       # Python dependencies
└── frontend/
    ├── index.html             # Main dashboard page
    ├── style.css              # Styling & responsive design
    └── script.js              # Frontend logic & API calls
```

## 🔌 API Endpoints

### POST `/summarize`

Summarize a single text with adjustable parameters.

**Request:**
```json
{
    "text": "Your text here...",
    "min_length": 30,
    "max_length": 130
}
```

**Response:**
```json
{
    "status": "success",
    "summary": "Summarized text...",
    "input_length": 100,
    "summary_length": 30,
    "input_tokens": 150,
    "summary_tokens": 45,
    "compression_ratio": 3.33
}
```

### POST `/summarize-batch`

Summarize multiple texts at once.

**Request:**
```json
{
    "texts": ["text1...", "text2..."],
    "min_length": 30,
    "max_length": 130
}
```

### GET `/model-info`

Get information about the current model.

### GET `/health`

Check API connectivity and model status.

## 💡 Usage Guide

### Dashboard Interface

1. **Adjust Parameters**
   - Use the "Minimum Summary Length" slider to set the minimum summary size (10-100 tokens)
   - Use the "Maximum Summary Length" slider to set the maximum summary size (50-300 tokens)
   - The range will update in real-time

2. **Enter Your Text**
   - Paste or type your text in the input area
   - Minimum 10 words required
   - Word count updates automatically

3. **Generate Summary**
   - Click "Summarize Text" button or press Ctrl+Enter
   - Wait for the model to process (usually 5-15 seconds)
   - Summary appears in the output section

4. **View Statistics**
   - Input Words: Original text word count
   - Summary Words: Summarized text word count
   - Compression Ratio: How much the text was compressed
   - Token counts for technical reference

5. **Copy & Share**
   - Click the "Copy" button to copy summary to clipboard
   - Use "Clear" to reset the dashboard

## 🔧 Configuration

### Adjust Default Parameters

**In `frontend/script.js`:**
```javascript
const API_BASE_URL = 'http://localhost:5000';  // Change backend URL
const DEBOUNCE_DELAY = 300;                     // Input debounce delay
```

**In `backend/app.py`:**
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port/host
```

### Use Different Model

**In `backend/app.py`:**
```python
summarizer = get_summarizer("facebook/bart-large-cnn")  # Change model
# Other options:
# - "t5-base"
# - "sshleifer/distilbart-cnn-6-6"
# - "google/pegasus-reddit_tifu"
```

## 📈 Performance Tips

1. **First Run**: Model downloads on first use (~1.5GB for BART)
2. **GPU Acceleration**: Modify `summarizer.py` line 34 to use GPU:
   ```python
   device=0  # 0 for GPU, -1 for CPU
   ```
3. **Batch Processing**: Use `/summarize-batch` for multiple texts
4. **Timeout**: Set longer timeouts for very long texts

## 🛠 Troubleshooting

### Backend Connection Error
- Ensure Flask server is running on `http://localhost:5000`
- Check firewall settings
- Verify port 5000 is not in use: `netstat -an | findstr :5000`

### Model Download Issues
- First run requires internet connection
- Models are cached in `~/.cache/huggingface/`
- Check available disk space (~2GB)

### Summary Quality Issues
- Longer texts often produce better summaries
- Adjust min/max length parameters
- Try different text sources

### Performance Issues
- Use GPU acceleration if available
- Reduce max_length for faster processing
- Consider using smaller models (distilbert, t5-base)

## 📦 Technologies Used

- **Backend**:
  - Flask: Web framework
  - Transformers: Pre-trained NLP models
  - PyTorch: Deep learning framework
  - NumPy/Pandas: Data processing
  - Scikit-learn: Machine learning utilities

- **Frontend**:
  - HTML5: Markup
  - CSS3: Styling & animations
  - Vanilla JavaScript: Interactivity
  - Fetch API: API communication

## 🎨 Customization

### Change Color Scheme

Edit `frontend/style.css` variables:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #10b981;
    --danger-color: #ef4444;
    /* ... other variables ... */
}
```

### Add New Features

1. Add endpoints in `backend/app.py`
2. Add UI elements in `frontend/index.html`
3. Add styling in `frontend/style.css`
4. Add event handlers in `frontend/script.js`

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Optimize performance

## 📝 License

This project is open-source and available for personal and educational use.

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Flask/Transformers documentation
3. Test endpoints with Postman or cURL

## 🚀 Deployment

### For Production:

1. **Use Gunicorn instead of Flask's dev server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Deploy Frontend to static hosting**

3. **Use Environment Variables:**
   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=0
   ```

4. **Add HTTPS/SSL certificates**

5. **Set up proper logging and monitoring**

## 📊 Example Use Cases

- **Content Creation**: Summarize articles for social media
- **Research**: Quick overview of multiple papers
- **Customer Support**: Summarize long customer messages
- **News**: Digest multiple news sources
- **Education**: Condense textbook chapters
- **Business**: Executive summaries of reports

## 🔐 Security Notes

- This is a development version
- For production, add authentication
- Validate all inputs
- Use HTTPS
- Implement rate limiting
- Add CORS restrictions

---

**Happy Summarizing! 📝✨**
