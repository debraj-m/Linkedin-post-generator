"""
Gemini AI client module
"""
import google.generativeai as genai
from typing import Optional, Tuple, List
import time
from src.config import Config

class GeminiClient:
    """Gemini AI client for content generation"""
    
    def __init__(self):
        self.model = None
        self.model_name = None
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        """Initialize Gemini model with fallback options"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("Gemini API key not found")
        
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        last_error = None
        
        for model_name in Config.SUPPORTED_MODELS:
            try:
                test_model = genai.GenerativeModel(model_name)
                # Test the model with a simple prompt
                test_response = test_model.generate_content("Hello")
                if test_response and test_response.text:
                    self.model = test_model
                    self.model_name = model_name
                    print(f"Successfully initialized model: {model_name}")
                    return
            except Exception as e:
                last_error = e
                print(f"Failed to initialize {model_name}: {str(e)}")
                continue
        
        # If no model works, raise an error
        raise Exception(f"Could not initialize any Gemini model. Last error: {last_error}")
    
    def generate_content(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Generate content using Gemini model with retry logic
        
        Args:
            prompt: The prompt to send to the model
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated content or None if failed
        """
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
                else:
                    print(f"Empty response on attempt {attempt + 1}")
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)  # Wait before retry
                else:
                    raise e
        
        return None
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test the connection to Gemini API
        
        Returns:
            Tuple of (success, message)
        """
        try:
            response = self.generate_content("Test connection")
            if response:
                return True, f"Successfully connected to {self.model_name}"
            else:
                return False, "No response from model"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def get_model_info(self) -> dict:
        """Get information about the current model"""
        return {
            "model_name": self.model_name,
            "status": "connected" if self.model else "disconnected"
        }
