"""
Flask Backend for Text Summarization Dashboard
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import get_summarizer
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress Werkzeug's development server warning in the terminal
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# Create Flask app
app = Flask(__name__)
CORS(app)

# Global summarizer
summarizer = None


def initialize_summarizer():
    """Initialize the summarizer on app startup"""
    global summarizer
    try:
        logger.info("Initializing summarizer...")
        summarizer = get_summarizer("facebook/bart-large-cnn")
        logger.info("Summarizer initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize summarizer: {e}")
        raise


@app.before_request
def before_request():
    """Initialize summarizer before first request"""
    global summarizer
    if summarizer is None:
        initialize_summarizer()


@app.route('/', methods=['GET'])
def home():
    """Serve home page information"""
    return jsonify({
        "message": "Text Summarization API",
        "version": "1.0.0",
        "endpoints": {
            "POST /summarize": "Summarize text with adjustable length",
            "POST /summarize-batch": "Summarize multiple texts",
            "GET /model-info": "Get model information",
            "GET /health": "Health check"
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": summarizer is not None
    })


@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the current model"""
    try:
        if summarizer is None:
            initialize_summarizer()
        
        return jsonify(summarizer.get_model_info())
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize text endpoint
    
    Expected JSON:
    {
        "text": "The text to summarize",
        "min_length": 30,
        "max_length": 130
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        text = data.get('text', '').strip()
        min_length = data.get('min_length', 50)
        max_length = data.get('max_length', 220)
        
        # Validate input
        if not text:
            return jsonify({
                "status": "error",
                "message": "Text field is required and cannot be empty"
            }), 400
        
        # Validate length parameters
        try:
            min_length = int(min_length)
            max_length = int(max_length)
            
            if min_length < 10:
                min_length = 10
            if max_length < min_length + 20:
                max_length = min_length + 20
            if max_length > 300:
                max_length = 300
                
        except (ValueError, TypeError):
            return jsonify({
                "status": "error",
                "message": "min_length and max_length must be valid integers"
            }), 400
        
        # Initialize summarizer if needed
        if summarizer is None:
            initialize_summarizer()
        
        # Generate summary
        result = summarizer.summarize(text, min_length, max_length)
        
        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {e}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route('/summarize-batch', methods=['POST'])
def summarize_batch():
    """
    Summarize multiple texts endpoint
    
    Expected JSON:
    {
        "texts": ["text1", "text2", ...],
        "min_length": 30,
        "max_length": 130
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        texts = data.get('texts', [])
        min_length = data.get('min_length', 50)
        max_length = data.get('max_length', 220)
        
        if not texts or not isinstance(texts, list):
            return jsonify({
                "status": "error",
                "message": "texts field must be a non-empty list"
            }), 400
        
        # Validate length parameters
        try:
            min_length = int(min_length)
            max_length = int(max_length)
        except (ValueError, TypeError):
            return jsonify({
                "status": "error",
                "message": "min_length and max_length must be valid integers"
            }), 400
        
        # Initialize summarizer if needed
        if summarizer is None:
            initialize_summarizer()
        
        # Generate summaries
        results = summarizer.summarize_batch(texts, min_length, max_length)
        
        return jsonify({
            "status": "success",
            "count": len(results),
            "summaries": results
        }), 200
    
    except Exception as e:
        logger.error(f"Error in summarize-batch endpoint: {e}\n{traceback.format_exc()}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Run the Flask app without Flask debugger and reloader to avoid development warnings
    app.run(debug=False, host='0.0.0.0', port=5000)
