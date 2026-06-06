"""
Text Summarization Module using Transformers
"""

import numpy as np
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import warnings

warnings.filterwarnings('ignore')


class TextSummarizer:
    """
    A class to handle text summarization using pre-trained transformer models.
    Supports adjustable summary length constraints.
    """
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize the summarizer with a pre-trained model.
        
        Args:
            model_name (str): Name of the pre-trained model from HuggingFace
        """
        try:
            self.model_name = model_name
            # Initialize the summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=model_name,
                device=-1  # Use CPU (change to 0 for GPU)
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            print(f"Model '{model_name}' loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def _validate_input(self, text):
        """
        Validate and preprocess input text.
        
        Args:
            text (str): Input text to validate
            
        Returns:
            str: Cleaned text
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input must be a non-empty string")
        
        # Clean the text
        text = text.strip()
        if len(text.split()) < 10:
            raise ValueError("Input text must contain at least 10 words")
        
        return text
    
    def _get_token_count(self, text):
        """
        Get the number of tokens in the text.
        
        Args:
            text (str): Input text
            
        Returns:
            int: Number of tokens
        """
        return len(self.tokenizer.encode(text))
    
    def summarize(self, text, min_length=30, max_length=130):
        """
        Generate a summary of the input text with specified length constraints.
        
        Args:
            text (str): The text to summarize
            min_length (int): Minimum length of summary in tokens (default: 30)
            max_length (int): Maximum length of summary in tokens (default: 130)
            
        Returns:
            dict: Dictionary containing summary and metadata
        """
        try:
            # Validate input
            cleaned_text = self._validate_input(text)
            
            # Get token and word counts
            input_tokens = self._get_token_count(cleaned_text)
            input_words = len(cleaned_text.split())

            # Enforce sensible length bounds
            if min_length < 30:
                min_length = 30
            if max_length < min_length + 20:
                max_length = min_length + 20

            # Use input size to choose a more reasonable summary length
            if input_words >= 250:
                min_length = max(min_length, int(input_words * 0.18))
                max_length = max(max_length, min(300, int(input_words * 0.35)))
            elif input_words >= 120:
                min_length = max(min_length, int(input_words * 0.16))
                max_length = max(max_length, min(260, int(input_words * 0.30)))
            else:
                min_length = max(min_length, int(input_words * 0.14))
                max_length = max(max_length, min(220, int(input_words * 0.40)))

            # Keep a safe gap between min and max
            if min_length >= max_length:
                min_length = max(30, max_length - 30)

            # Generate summary with a stronger beam search and length bias
            summary = self.summarizer(
                cleaned_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                num_beams=6,
                length_penalty=1.1,
                no_repeat_ngram_size=3,
                early_stopping=True
            )
            
            summary_text = summary[0]['summary_text']
            summary_tokens = self._get_token_count(summary_text)
            
            return {
                "status": "success",
                "summary": summary_text,
                "input_length": len(cleaned_text.split()),
                "summary_length": len(summary_text.split()),
                "input_tokens": input_tokens,
                "summary_tokens": summary_tokens,
                "compression_ratio": round(len(cleaned_text.split()) / len(summary_text.split()), 2)
            }
        
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Summarization failed: {str(e)}"
            }
    
    def summarize_batch(self, texts, min_length=30, max_length=130):
        """
        Summarize multiple texts at once.
        
        Args:
            texts (list): List of texts to summarize
            min_length (int): Minimum summary length
            max_length (int): Maximum summary length
            
        Returns:
            list: List of summary dictionaries
        """
        results = []
        for text in texts:
            result = self.summarize(text, min_length, max_length)
            results.append(result)
        
        return results
    
    def get_model_info(self):
        """
        Get information about the current model.
        
        Returns:
            dict: Model information
        """
        return {
            "model_name": self.model_name,
            "model_type": "Sequence-to-Sequence (Transformer)",
            "task": "Text Summarization",
            "default_min_length": 50,
            "default_max_length": 220
        }


# Initialize global summarizer instance
summarizer_instance = None


def get_summarizer(model_name="facebook/bart-large-cnn"):
    """
    Get or create a global summarizer instance.
    
    Args:
        model_name (str): Model name to use
        
    Returns:
        TextSummarizer: Summarizer instance
    """
    global summarizer_instance
    
    if summarizer_instance is None:
        summarizer_instance = TextSummarizer(model_name)
    
    return summarizer_instance
