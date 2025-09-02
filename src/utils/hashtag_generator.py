"""
Hashtag generation module
"""
from typing import List
from src.utils.gemini_client import GeminiClient

class HashtagGenerator:
    """Generate relevant hashtags for LinkedIn posts"""
    
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client
    
    def generate_hashtags(self, topic: str, audience: str = "", post_type: str = "", count: int = 5) -> List[str]:
        """
        Generate relevant hashtags based on topic and context
        
        Args:
            topic: Main topic of the post
            audience: Target audience
            post_type: Type of post (story, tips, etc.)
            count: Number of hashtags to generate
            
        Returns:
            List of hashtags
        """
        try:
            prompt = f"""Generate {count} highly relevant and trending LinkedIn hashtags for:
            
            Topic: {topic}
            {f'Audience: {audience}' if audience else ''}
            {f'Post Type: {post_type}' if post_type else ''}
            
            Requirements:
            1. Use popular LinkedIn hashtags that actually exist
            2. Mix of broad and specific hashtags
            3. Include industry-relevant tags
            4. Ensure hashtags are professional and appropriate
            5. Focus on discoverability and engagement
            
            Format: Return only the hashtags, one per line, starting with #
            Example:
            #Leadership
            #BusinessStrategy
            #ProfessionalDevelopment"""
            
            response = self.gemini_client.generate_content(prompt)
            if response:
                hashtags = []
                lines = response.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('#') and len(line) > 1:
                        # Clean up the hashtag
                        hashtag = line.split()[0]  # Take only the first word if there are spaces
                        if hashtag not in hashtags:  # Avoid duplicates
                            hashtags.append(hashtag)
                
                return hashtags[:count]  # Return only requested count
            else:
                return self._get_fallback_hashtags(topic)
                
        except Exception as e:
            print(f"Error generating hashtags: {str(e)}")
            return self._get_fallback_hashtags(topic)
    
    def _get_fallback_hashtags(self, topic: str) -> List[str]:
        """
        Generate fallback hashtags when AI generation fails
        
        Args:
            topic: Main topic
            
        Returns:
            List of basic hashtags
        """
        # Basic professional hashtags
        fallback_tags = ["#LinkedIn", "#Professional", "#Career", "#Business", "#Leadership"]
        
        # Try to create a topic-specific hashtag
        topic_words = topic.replace(" ", "").replace("-", "")
        if len(topic_words) > 3:
            topic_tag = f"#{topic_words.title()}"
            fallback_tags.insert(1, topic_tag)
        
        return fallback_tags[:5]
    
    def analyze_hashtag_performance(self, hashtags: List[str]) -> dict:
        """
        Analyze potential performance of hashtags
        
        Args:
            hashtags: List of hashtags to analyze
            
        Returns:
            Dictionary with analysis results
        """
        try:
            hashtag_text = " ".join(hashtags)
            prompt = f"""Analyze these LinkedIn hashtags for performance potential:
            
            Hashtags: {hashtag_text}
            
            Evaluate:
            1. Popularity level (High/Medium/Low) for each
            2. Competition level (High/Medium/Low) for each
            3. Relevance score (1-10) for each
            4. Overall hashtag strategy rating (1-10)
            
            Provide a brief analysis of the hashtag mix and suggestions for improvement."""
            
            response = self.gemini_client.generate_content(prompt)
            if response:
                return {
                    "analysis": response,
                    "hashtag_count": len(hashtags),
                    "hashtags": hashtags
                }
            else:
                return {"analysis": "Could not analyze hashtags", "hashtag_count": len(hashtags), "hashtags": hashtags}
                
        except Exception as e:
            return {"analysis": f"Error analyzing hashtags: {str(e)}", "hashtag_count": len(hashtags), "hashtags": hashtags}
