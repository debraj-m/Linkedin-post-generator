"""
Configuration module for LinkedIn Post Generator
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Model Configuration
    SUPPORTED_MODELS = [
        "gemini-1.5-flash",  # Latest and fastest
        "gemini-1.5-pro",   # Most capable
        "gemini-pro",       # Legacy but still supported
        "models/gemini-1.5-flash",  # With models/ prefix
        "models/gemini-1.5-pro",    # With models/ prefix
        "models/gemini-pro"         # With models/ prefix
    ]
    
    # App Configuration
    APP_TITLE = "LinkedIn Post Generator"
    APP_ICON = ""
    MAX_POSTS = 5
    MIN_POSTS = 1
    DEFAULT_POSTS = 3
    
    # Content Configuration
    MAX_POST_LENGTH = 1300
    MIN_POST_LENGTH = 1000
    
    # Tone Options
    TONE_OPTIONS = ["", "Professional", "Conversational", "Enthusiastic", "Educational", "Inspirational", "Analytical", "Thought Leadership", "Personal Storytelling"]
    
    # Post Types
    POST_TYPES = ["", "Story", "Tips", "Question", "Industry Insight", "Personal Experience", "Tutorial", "Case Study", "Opinion Piece"]
    
    # Trend Analysis
    ENABLE_TREND_ANALYSIS = True
    ENABLE_INSPIRATION_SEARCH = True
    
    @classmethod
    def validate_config(cls):
        """Validate configuration"""
        errors = []
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY environment variable is required")
            
        return errors
