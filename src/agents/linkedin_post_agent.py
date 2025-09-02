"""
Main LinkedIn Post Generation Agent
Enhanced with trend analysis and content inspiration for better agentic behavior
"""
from typing import List, Dict, Optional, Tuple
import time
from dataclasses import dataclass
from src.utils.gemini_client import GeminiClient
from src.utils.content_filter import ContentFilter
from src.utils.hashtag_generator import HashtagGenerator
from src.utils.trend_analyzer import TrendAnalyzer
from src.config import Config

@dataclass
class PostRequest:
    """Data class for post generation request"""
    topic: str
    tone: str = ""
    audience: str = ""
    post_type: str = ""
    post_count: int = 3
    include_hashtags: bool = True
    include_cta: bool = True

@dataclass
class GeneratedPost:
    """Data class for a generated post"""
    content: str
    hashtags: List[str]
    char_count: int
    quality_score: float
    engagement_potential: str
    generation_time: float
    tone_used: str
    inspiration_source: str

class LinkedInPostAgent:
    """
    Enhanced agent for generating LinkedIn posts with advanced agentic capabilities:
    1. Trend Analysis
    2. Content Inspiration Research
    3. Audience Interest Analysis
    4. Strategic Content Planning
    5. Post Generation
    6. Quality Control
    7. Hashtag Generation
    8. Final Assembly
    """
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.content_filter = ContentFilter(self.gemini_client)
        self.hashtag_generator = HashtagGenerator(self.gemini_client)
        self.trend_analyzer = TrendAnalyzer(self.gemini_client)
        self.generation_stats = {
            "total_generated": 0,
            "total_filtered": 0,
            "avg_generation_time": 0
        }
    
    def generate_posts(self, request: PostRequest) -> Tuple[List[GeneratedPost], Dict]:
        """
        Enhanced method to generate LinkedIn posts using advanced multi-step agent approach
        
        Args:
            request: PostRequest with generation parameters
            
        Returns:
            Tuple of (list of generated posts, generation metadata)
        """
        start_time = time.time()
        
        try:
            # Step 1: Trend Analysis (Enhanced Agentic Behavior)
            trends = self._analyze_trends(request)
            
            # Step 2: Content Inspiration Research (Enhanced Agentic Behavior)
            inspiration = self._research_content_inspiration(request)
            
            # Step 3: Audience Interest Analysis (Enhanced Agentic Behavior)
            audience_insights = self._analyze_audience_interests(request)
            
            # Step 4: Strategic Content Planning
            content_strategy = self._create_enhanced_content_plan(request, trends, inspiration, audience_insights)
            
            # Step 5: Generate raw posts with enhanced context
            raw_posts = self._generate_enhanced_posts(request, content_strategy, trends, inspiration)
            
            # Step 6: Filter and quality check
            filtered_posts = self._filter_and_validate_posts(raw_posts)
            
            # Step 7: Generate hashtags if requested
            if request.include_hashtags:
                hashtags = self.hashtag_generator.generate_hashtags(
                    request.topic, 
                    request.audience, 
                    request.post_type
                )
            else:
                hashtags = []
            
            # Step 8: Assemble final posts with enhanced metadata
            final_posts = self._assemble_enhanced_final_posts(filtered_posts, hashtags, request, inspiration)
            
            # Generate metadata
            generation_time = time.time() - start_time
            metadata = self._create_enhanced_metadata(final_posts, generation_time, request, trends, inspiration)
            
            # Update stats
            self._update_stats(len(final_posts), generation_time)
            
            return final_posts, metadata
            
        except Exception as e:
            return [], {"error": str(e), "generation_time": time.time() - start_time}
    
    def _analyze_trends(self, request: PostRequest) -> Dict:
        """Step 1: Analyze current trends (Enhanced Agentic Behavior)"""
        if Config.ENABLE_TREND_ANALYSIS:
            return self.trend_analyzer.analyze_current_trends(request.topic, request.audience)
        return {"status": "disabled"}
    
    def _research_content_inspiration(self, request: PostRequest) -> Dict:
        """Step 2: Research successful content patterns (Enhanced Agentic Behavior)"""
        if Config.ENABLE_INSPIRATION_SEARCH:
            return self.trend_analyzer.find_content_inspiration(request.topic, request.tone, request.post_type)
        return {"status": "disabled"}
    
    def _analyze_audience_interests(self, request: PostRequest) -> Dict:
        """Step 3: Analyze target audience interests (Enhanced Agentic Behavior)"""
        if request.audience and Config.ENABLE_TREND_ANALYSIS:
            return self.trend_analyzer.analyze_audience_interests(request.audience, request.topic)
        return {"status": "skipped", "message": "No audience specified"}
    
    def _create_enhanced_content_plan(self, request: PostRequest, trends: Dict, inspiration: Dict, audience_insights: Dict) -> str:
        """Step 4: Create enhanced strategic content plan"""
        # Generate comprehensive strategy based on all research
        strategy = self.trend_analyzer.generate_content_strategy(
            request.topic, trends, inspiration, audience_insights
        )
        
        # Create detailed content plan
        prompt = f"""Based on this comprehensive research and strategy:

CONTENT STRATEGY:
{strategy}

Create a detailed content plan for {request.post_count} LinkedIn posts about "{request.topic}".

Requirements:
- Leverage trending topics and current discussions
- Use proven engagement patterns from successful content
- Address specific audience interests and pain points
- Ensure each post has a unique angle and value proposition
- Plan for variety in content types and approaches
{f'- Target tone: {request.tone}' if request.tone else '- Determine most effective tone for each post'}
{f'- Audience focus: {request.audience}' if request.audience else ''}
{f'- Post type preference: {request.post_type}' if request.post_type else ''}

Provide a strategic outline with:
1. Main angle/hook for each post
2. Key value proposition
3. Engagement strategy
4. Target outcome (shares, comments, etc.)"""
        
        return self.gemini_client.generate_content(prompt) or strategy
    
    def _generate_enhanced_posts(self, request: PostRequest, content_strategy: str, trends: Dict, inspiration: Dict) -> List[str]:
        """Step 5: Generate enhanced posts with trend and inspiration context"""
        # Determine effective tone if not specified
        effective_tone = self._determine_effective_tone(request, trends, inspiration)
        
        prompt = f"""Based on this strategic content plan and research:

CONTENT STRATEGY:
{content_strategy}

CURRENT TRENDS:
{trends.get('trends', 'No trend data available')}

SUCCESSFUL CONTENT PATTERNS:
{inspiration.get('inspiration', 'No inspiration data available')}

Generate {request.post_count} professional LinkedIn posts about "{request.topic}".

ENHANCED REQUIREMENTS:
1. HOOKS: Start each post with a compelling hook based on successful patterns
   - Use trending angles and current discussions
   - Address real professional challenges
   - Create curiosity or emotional connection

2. VALUE DELIVERY: Provide genuine professional value
   - Actionable insights professionals can use immediately
   - Real-world examples and case studies
   - Industry-specific knowledge and expertise
   - Personal experiences that teach lessons

3. ENGAGEMENT OPTIMIZATION: Structure for maximum engagement
   - Use proven content formats that drive comments
   - Include thought-provoking questions
   - Create shareable moments and quotable insights
   - End with clear, compelling calls-to-action

4. PROFESSIONAL TONE: 
   - Use tone: {effective_tone}
   - Maintain professional credibility
   - Use industry-appropriate language
   - Balance authenticity with expertise

5. CONTENT STRUCTURE:
   - Opening hook (1-2 lines)
   - Value delivery (main content)
   - Personal insight or example
   - Clear call-to-action
   - Optimal length: {Config.MIN_POST_LENGTH}-{Config.MAX_POST_LENGTH} characters

6. AUDIENCE TARGETING:
   {f'- Speak directly to {request.audience}' if request.audience else '- Address general professional audience'}
   - Use language and examples they relate to
   - Address their specific challenges and goals

Format each post clearly and ensure they feel authentic, valuable, and engaging.

Post 1:
[Content focused on trending angle #1]

Post 2:
[Content focused on different successful pattern]

Continue for all {request.post_count} posts, ensuring variety and unique value in each."""
        
        response = self.gemini_client.generate_content(prompt)
        if not response:
            return []
        
        # Parse posts with better extraction
        posts = []
        sections = response.split('Post ')
        for section in sections[1:]:
            lines = section.strip().split('\n')
            if len(lines) > 1:
                # Extract content after the post number
                post_content = '\n'.join(lines[1:]).strip()
                # Remove any metadata or formatting
                post_content = post_content.replace('[Content focused on', '').replace(']', '').strip()
                if post_content and len(post_content) > 50:
                    posts.append(post_content)
        
        return posts
    
    def _determine_effective_tone(self, request: PostRequest, trends: Dict, inspiration: Dict) -> str:
        """Determine the most effective tone if not specified"""
        if request.tone:
            return request.tone
        
        # Use AI to determine best tone based on research
        prompt = f"""Based on this research about "{request.topic}":

TRENDS: {trends.get('trends', 'No data')}
INSPIRATION: {inspiration.get('inspiration', 'No data')}
AUDIENCE: {request.audience or 'General professional audience'}

What tone would be most effective for LinkedIn posts? Choose from:
{', '.join(Config.TONE_OPTIONS[1:])}

Respond with just the tone name and brief reasoning."""
        
        response = self.gemini_client.generate_content(prompt)
        if response:
            # Extract the tone from the response
            for tone in Config.TONE_OPTIONS[1:]:
                if tone.lower() in response.lower():
                    return tone
        
        return "Professional"  # Default fallback
    
    def _filter_and_validate_posts(self, raw_posts: List[str]) -> List[str]:
        """Step 6: Filter content and validate quality"""
        filtered_posts = []
        
        for post in raw_posts:
            # Content safety filter
            is_safe, filter_result = self.content_filter.filter_content(post)
            if not is_safe:
                print(f"Post filtered out: {filter_result}")
                self.generation_stats["total_filtered"] += 1
                continue
            
            # Length validation
            if len(post) < 100:  # Too short
                continue
            
            filtered_posts.append(post)
        
        return filtered_posts
    
    def _assemble_enhanced_final_posts(self, filtered_posts: List[str], hashtags: List[str], request: PostRequest, inspiration: Dict) -> List[GeneratedPost]:
        """Step 8: Assemble final posts with enhanced metadata"""
        final_posts = []
        effective_tone = self._determine_effective_tone(request, {}, inspiration)
        
        for i, post_content in enumerate(filtered_posts):
            # Add hashtags if requested
            if request.include_hashtags and hashtags:
                content_with_hashtags = f"{post_content}\n\n{' '.join(hashtags)}"
            else:
                content_with_hashtags = post_content
            
            # Get quality metrics
            _, feedback, metrics = self.content_filter.check_post_quality(post_content)
            
            # Create GeneratedPost object with enhanced metadata
            generated_post = GeneratedPost(
                content=content_with_hashtags,
                hashtags=hashtags if request.include_hashtags else [],
                char_count=len(content_with_hashtags),
                quality_score=metrics.get('engagement', 0) / 10.0 if metrics else 0.5,
                engagement_potential=self._calculate_engagement_potential(metrics),
                generation_time=0.0,  # Will be set in metadata
                tone_used=effective_tone,
                inspiration_source="trend analysis and successful content patterns"
            )
            
            final_posts.append(generated_post)
        
        return final_posts
    
    def _calculate_engagement_potential(self, metrics: Dict) -> str:
        """Calculate engagement potential based on quality metrics"""
        if not metrics:
            return "Medium"
        
        avg_score = sum(metrics.values()) / len(metrics)
        if avg_score >= 8:
            return "High"
        elif avg_score >= 6:
            return "Medium"
        else:
            return "Low"
    
    def _create_enhanced_metadata(self, posts: List[GeneratedPost], generation_time: float, request: PostRequest, trends: Dict, inspiration: Dict) -> Dict:
        """Create enhanced generation metadata"""
        return {
            "generation_time": round(generation_time, 2),
            "posts_generated": len(posts),
            "model_used": self.gemini_client.model_name,
            "agentic_features_used": {
                "trend_analysis": trends.get("status") == "success",
                "content_inspiration": inspiration.get("status") == "success",
                "audience_analysis": bool(request.audience),
                "tone_optimization": True,
                "quality_filtering": True
            },
            "request_params": {
                "topic": request.topic,
                "tone": request.tone,
                "audience": request.audience,
                "post_type": request.post_type,
                "requested_count": request.post_count,
                "include_hashtags": request.include_hashtags
            },
            "avg_char_count": sum(p.char_count for p in posts) // len(posts) if posts else 0,
            "quality_distribution": {
                "high": len([p for p in posts if p.engagement_potential == "High"]),
                "medium": len([p for p in posts if p.engagement_potential == "Medium"]),
                "low": len([p for p in posts if p.engagement_potential == "Low"])
            },
            "tone_analysis": {
                "effective_tone": posts[0].tone_used if posts else "Professional",
                "tone_specified": bool(request.tone),
                "tone_optimization": not bool(request.tone)
            },
            "research_summary": {
                "trends_analyzed": trends.get("status") == "success",
                "inspiration_found": inspiration.get("status") == "success",
                "audience_insights": bool(request.audience)
            }
        }
    
    def _update_stats(self, posts_generated: int, generation_time: float):
        """Update generation statistics"""
        self.generation_stats["total_generated"] += posts_generated
        
        # Update average generation time
        if self.generation_stats["avg_generation_time"] == 0:
            self.generation_stats["avg_generation_time"] = generation_time
        else:
            self.generation_stats["avg_generation_time"] = (
                self.generation_stats["avg_generation_time"] + generation_time
            ) / 2
    
    def get_health_status(self) -> Dict:
        """Get agent health status"""
        is_connected, message = self.gemini_client.test_connection()
        
        return {
            "status": "healthy" if is_connected else "unhealthy",
            "gemini_connection": is_connected,
            "message": message,
            "model_info": self.gemini_client.get_model_info(),
            "generation_stats": self.generation_stats
        }
