"""
Content filtering and quality control module
"""
from typing import Tuple
from src.utils.gemini_client import GeminiClient

class ContentFilter:
    """Content filtering and quality guardrails"""
    
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
    
    def filter_content(self, text: str) -> Tuple[bool, str]:
        """
        Filter content for professional LinkedIn standards
        
        Args:
            text: Content to filter
            
        Returns:
            Tuple of (is_safe, result_message)
        """
        try:
            prompt = f"""Please analyze this LinkedIn post content for professional standards. 
            Check for:
            1. Appropriate professional language
            2. No controversial or offensive topics
            3. Professional tone suitable for LinkedIn
            4. No personal attacks or inappropriate content
            5. No misleading claims or misinformation
            
            Text: {text}
            
            Return only 'PASS' if content is appropriate, or 'FAIL: [specific reason]' if not.
            Be strict but fair in your assessment."""
            
            response = self.gemini_client.generate_content(prompt)
            if response:
                result = response.strip()
                is_safe = result.startswith('PASS')
                return is_safe, result
            else:
                return False, "Error: Could not analyze content"
                
        except Exception as e:
            return False, f"Error in content filtering: {str(e)}"
    
    def check_post_quality(self, text: str) -> Tuple[bool, str, dict]:
        """
        Check post quality and provide metrics
        
        Args:
            text: Post content to analyze
            
        Returns:
            Tuple of (is_quality, feedback, metrics)
        """
        try:
            prompt = f"""Analyze this LinkedIn post for quality metrics:
            
            Text: {text}
            
            Evaluate:
            1. Engagement potential (1-10)
            2. Professional tone (1-10) 
            3. Clarity and readability (1-10)
            4. Value to readers (1-10)
            5. Call-to-action effectiveness (1-10)
            
            Format your response as:
            SCORE: [overall score 1-10]
            ENGAGEMENT: [score]
            TONE: [score]
            CLARITY: [score]
            VALUE: [score]
            CTA: [score]
            FEEDBACK: [brief feedback]"""
            
            response = self.gemini_client.generate_content(prompt)
            if response:
                lines = response.strip().split('\n')
                metrics = {}
                feedback = ""
                overall_score = 0
                
                for line in lines:
                    if line.startswith('SCORE:'):
                        overall_score = int(line.split(':')[1].strip())
                    elif line.startswith('ENGAGEMENT:'):
                        metrics['engagement'] = int(line.split(':')[1].strip())
                    elif line.startswith('TONE:'):
                        metrics['tone'] = int(line.split(':')[1].strip())
                    elif line.startswith('CLARITY:'):
                        metrics['clarity'] = int(line.split(':')[1].strip())
                    elif line.startswith('VALUE:'):
                        metrics['value'] = int(line.split(':')[1].strip())
                    elif line.startswith('CTA:'):
                        metrics['cta'] = int(line.split(':')[1].strip())
                    elif line.startswith('FEEDBACK:'):
                        feedback = line.split(':')[1].strip()
                
                is_quality = overall_score >= 6
                return is_quality, feedback, metrics
            else:
                return False, "Could not analyze quality", {}
                
        except Exception as e:
            return False, f"Error in quality check: {str(e)}", {}
