"""
Cost estimation module for API usage tracking
"""
from typing import Dict
import time

class CostEstimator:
    """Estimate costs and track API usage"""
    
    # Gemini pricing (approximate, check current pricing)
    GEMINI_PRICING = {
        "gemini-1.5-flash": {
            "input": 0.075 / 1000000,   # $0.075 per 1M input tokens
            "output": 0.3 / 1000000     # $0.30 per 1M output tokens
        },
        "gemini-1.5-pro": {
            "input": 3.5 / 1000000,     # $3.50 per 1M input tokens
            "output": 10.5 / 1000000    # $10.50 per 1M output tokens
        },
        "gemini-pro": {
            "input": 0.5 / 1000000,     # $0.50 per 1M input tokens (legacy pricing)
            "output": 1.5 / 1000000     # $1.50 per 1M output tokens
        }
    }
    
    def __init__(self):
        self.session_stats = {
            "requests": 0,
            "estimated_input_tokens": 0,
            "estimated_output_tokens": 0,
            "estimated_cost": 0.0,
            "start_time": time.time()
        }
    
    def estimate_tokens(self, text: str) -> int:
        """
        Rough token estimation (1 token ≈ 4 characters for English)
        
        Args:
            text: Input text
            
        Returns:
            Estimated token count
        """
        return len(text) // 4
    
    def estimate_request_cost(self, model_name: str, input_text: str, output_text: str) -> Dict:
        """
        Estimate cost for a single request
        
        Args:
            model_name: Name of the model used
            input_text: Input prompt text
            output_text: Generated output text
            
        Returns:
            Dictionary with cost breakdown
        """
        # Clean model name to match pricing keys
        clean_model_name = model_name.replace("models/", "")
        
        # Get pricing info
        if clean_model_name in self.GEMINI_PRICING:
            pricing = self.GEMINI_PRICING[clean_model_name]
        else:
            # Default to flash pricing if model not found
            pricing = self.GEMINI_PRICING["gemini-1.5-flash"]
        
        # Estimate tokens
        input_tokens = self.estimate_tokens(input_text)
        output_tokens = self.estimate_tokens(output_text)
        
        # Calculate costs
        input_cost = input_tokens * pricing["input"]
        output_cost = output_tokens * pricing["output"]
        total_cost = input_cost + output_cost
        
        # Update session stats
        self.session_stats["requests"] += 1
        self.session_stats["estimated_input_tokens"] += input_tokens
        self.session_stats["estimated_output_tokens"] += output_tokens
        self.session_stats["estimated_cost"] += total_cost
        
        return {
            "model": clean_model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6),
            "cost_formatted": f"${total_cost:.6f}"
        }
    
    def get_session_summary(self) -> Dict:
        """Get summary of current session usage"""
        session_duration = time.time() - self.session_stats["start_time"]
        
        return {
            "session_duration_minutes": round(session_duration / 60, 2),
            "total_requests": self.session_stats["requests"],
            "total_input_tokens": self.session_stats["estimated_input_tokens"],
            "total_output_tokens": self.session_stats["estimated_output_tokens"],
            "estimated_total_cost": round(self.session_stats["estimated_cost"], 6),
            "cost_formatted": f"${self.session_stats['estimated_cost']:.6f}",
            "avg_cost_per_request": round(
                self.session_stats["estimated_cost"] / max(1, self.session_stats["requests"]), 6
            )
        }
    
    def reset_session(self):
        """Reset session statistics"""
        self.session_stats = {
            "requests": 0,
            "estimated_input_tokens": 0,
            "estimated_output_tokens": 0,
            "estimated_cost": 0.0,
            "start_time": time.time()
        }
    
    def format_cost_display(self, cost_info: Dict) -> str:
        """Format cost information for display"""
        return f"""
        **Cost Breakdown:**
        - Model: {cost_info['model']}
        - Tokens: {cost_info['input_tokens']} in + {cost_info['output_tokens']} out
        - Cost: {cost_info['cost_formatted']}
        """
