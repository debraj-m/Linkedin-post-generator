"""
Trend Analysis and Content Inspiration Module
Enhanced agentic capabilities for LinkedIn post generation
"""
from typing import List, Dict, Optional
from src.utils.gemini_client import GeminiClient
from src.config import Config

class TrendAnalyzer:
    """Analyze trends and find content inspiration for better LinkedIn posts"""
    
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
    
    def analyze_current_trends(self, topic: str, audience: str = "") -> Dict:
        """
        Analyze current trends related to the topic
        
        Args:
            topic: Main topic to analyze
            audience: Target audience for context
            
        Returns:
            Dictionary with trend analysis
        """
        try:
            prompt = f"""Analyze current trends and hot topics related to "{topic}" in 2025.
            
            Consider:
            1. Recent industry developments and news
            2. Popular discussions on LinkedIn and professional networks
            3. Emerging technologies or methodologies
            4. Common challenges professionals are facing
            5. Popular content formats that are getting engagement
            {f'6. Specific trends relevant to {audience}' if audience else ''}
            
            Provide:
            - Top 3 trending subtopics within this area
            - Current industry challenges people are discussing
            - Popular content angles that get engagement
            - Buzzwords and terminology that are trending
            - Recent developments or news in this space
            
            Format your response clearly with sections."""
            
            response = self.gemini_client.generate_content(prompt)
            if response:
                return {
                    "status": "success",
                    "trends": response,
                    "topic": topic,
                    "audience": audience
                }
            else:
                return {"status": "error", "message": "Could not analyze trends"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error analyzing trends: {str(e)}"}
    
    def find_content_inspiration(self, topic: str, tone: str = "", post_type: str = "") -> Dict:
        """
        Find inspiration from successful LinkedIn content patterns
        
        Args:
            topic: Main topic
            tone: Desired tone
            post_type: Type of post
            
        Returns:
            Dictionary with content inspiration
        """
        try:
            prompt = f"""Analyze successful LinkedIn content patterns for posts about "{topic}".
            
            Based on high-performing LinkedIn posts, identify:
            
            1. SUCCESSFUL CONTENT STRUCTURES:
            - Opening hooks that grab attention
            - Content flow patterns that work
            - Effective storytelling techniques
            - Call-to-action patterns that drive engagement
            
            2. ENGAGEMENT DRIVERS:
            - Question formats that generate comments
            - Story elements that resonate with professionals
            - Data points and statistics that get shared
            - Personal experiences that connect with audiences
            
            3. CONTENT FORMATS THAT WORK:
            - List formats (3 tips, 5 strategies, etc.)
            - Before/after narratives
            - Lesson learned stories
            - Industry insight posts
            - Contrarian viewpoints that spark discussion
            
            4. PROFESSIONAL LANGUAGE PATTERNS:
            - Power words that professionals use
            - Industry-specific terminology
            - Confidence-building language
            - Authentic, relatable expressions
            
            {f'5. Tailor recommendations for {tone} tone' if tone else ''}
            {f'6. Focus on {post_type} format specifically' if post_type else ''}
            
            Provide specific examples and patterns, not just generic advice."""
            
            response = self.gemini_client.generate_content(prompt)
            if response:
                return {
                    "status": "success",
                    "inspiration": response,
                    "topic": topic,
                    "tone": tone,
                    "post_type": post_type
                }
            else:
                return {"status": "error", "message": "Could not find content inspiration"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error finding inspiration: {str(e)}"}
    
    def analyze_audience_interests(self, audience: str, topic: str) -> Dict:
        """
        Analyze what the target audience cares about
        
        Args:
            audience: Target audience description
            topic: Main topic
            
        Returns:
            Dictionary with audience analysis
        """
        if not audience:
            return {"status": "skipped", "message": "No audience specified"}
        
        try:
            prompt = f"""Analyze what {audience} professionals care about regarding "{topic}".
            
            Consider:
            1. Pain points and challenges they face
            2. Goals and aspirations they have
            3. Industry terminology they use
            4. Content formats they prefer
            5. Level of technical detail they want
            6. Time constraints and information consumption habits
            7. Professional development interests
            8. Business impact they care about
            
            Provide insights that will help create more targeted, relevant content."""
            
            response = self.gemini_client.generate_content(prompt)
            if response:
                return {
                    "status": "success",
                    "audience_insights": response,
                    "audience": audience,
                    "topic": topic
                }
            else:
                return {"status": "error", "message": "Could not analyze audience"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error analyzing audience: {str(e)}"}
    
    def generate_content_strategy(self, topic: str, trends: Dict, inspiration: Dict, audience_insights: Dict) -> str:
        """
        Generate a comprehensive content strategy based on all analysis
        
        Args:
            topic: Main topic
            trends: Trend analysis results
            inspiration: Content inspiration results
            audience_insights: Audience analysis results
            
        Returns:
            Content strategy recommendations
        """
        try:
            strategy_prompt = f"""Based on the following research, create a strategic content plan for LinkedIn posts about "{topic}":

TREND ANALYSIS:
{trends.get('trends', 'No trend data available')}

CONTENT INSPIRATION:
{inspiration.get('inspiration', 'No inspiration data available')}

AUDIENCE INSIGHTS:
{audience_insights.get('audience_insights', 'No audience data available')}

Create a strategic content approach that:
1. Leverages current trends and hot topics
2. Uses proven engagement patterns
3. Speaks directly to the target audience's interests
4. Incorporates successful content structures
5. Suggests specific angles and approaches
6. Recommends key messages and themes
7. Identifies unique value propositions

Format this as actionable guidance for content creation."""

            response = self.gemini_client.generate_content(strategy_prompt)
            return response or "Could not generate content strategy"
            
        except Exception as e:
            return f"Error generating strategy: {str(e)}"
