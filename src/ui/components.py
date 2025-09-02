"""
UI components for Streamlit interface
"""
import streamlit as st
from typing import Dict, List
from datetime import datetime
from src.agents.linkedin_post_agent import GeneratedPost, PostRequest
from src.config import Config

class UIComponents:
    """Reusable UI components for the Streamlit app"""
    
    @staticmethod
    def render_header():
        """Render app header"""
        st.set_page_config(
            page_title=Config.APP_TITLE,
            page_icon=Config.APP_ICON,
            layout="centered",
            initial_sidebar_state="expanded"
        )
        
        st.title(Config.APP_TITLE)
        st.markdown("Generate engaging LinkedIn posts using AI with advanced content planning, trend analysis, and quality control")
        
        # Health status indicator
        if hasattr(st.session_state, 'agent_healthy'):
            if st.session_state.agent_healthy:
                st.success("AI Agent Status: Online")
            else:
                st.error("AI Agent Status: Offline")
    
    @staticmethod
    def render_input_form() -> PostRequest:
        """
        Render the input form and return PostRequest
        
        Returns:
            PostRequest object with user inputs
        """
        with st.form("post_generator_form"):
            st.subheader("Post Configuration")
            
            # Required topic input
            topic = st.text_area(
                "Topic* (required)", 
                placeholder="e.g., cold-start strategies for marketplaces, remote work productivity tips, AI in business transformation",
                help="Enter the main topic for your LinkedIn posts. Be specific for better results.",
                height=100
            )
            
            # Optional inputs in columns
            col1, col2 = st.columns(2)
            
            with col1:
                tone = st.selectbox(
                    "Tone",
                    options=Config.TONE_OPTIONS,
                    help="Select the tone for your posts"
                )
                
                post_type = st.selectbox(
                    "Post Type",
                    options=Config.POST_TYPES,
                    help="Choose the type/format of posts"
                )
                
                post_count = st.slider(
                    "Number of posts",
                    min_value=Config.MIN_POSTS,
                    max_value=Config.MAX_POSTS,
                    value=Config.DEFAULT_POSTS,
                    help="How many posts to generate"
                )

            with col2:
                audience = st.text_input(
                    "Target Audience",
                    placeholder="e.g., startup founders, product managers, data scientists",
                    help="Specify your target audience for better personalization"
                )
                
                include_hashtags = st.checkbox(
                    "Include hashtags",
                    value=True,
                    help="Add relevant hashtags to your posts"
                )
                
                include_cta = st.checkbox(
                    "Include Call-to-Action",
                    value=True,
                    help="Add engaging CTAs to encourage interaction"
                )

            # Advanced options in expander
            with st.expander("Advanced Options", expanded=False):
                col3, col4 = st.columns(2)
                
                with col3:
                    character_preference = st.radio(
                        "Post Length Preference",
                        options=["Standard (1000-1300 chars)", "Shorter (800-1000 chars)", "Longer (1300-1500 chars)"],
                        help="Preferred length for generated posts"
                    )
                
                with col4:
                    engagement_focus = st.multiselect(
                        "Engagement Focus",
                        options=["Questions", "Stories", "Tips", "Statistics", "Personal Experience"],
                        default=["Questions", "Tips"],
                        help="Elements to emphasize for better engagement"
                    )

            submitted = st.form_submit_button("Generate Posts", type="primary")

            if submitted and topic:
                return PostRequest(
                    topic=topic,
                    tone=tone,
                    audience=audience,
                    post_type=post_type,
                    post_count=post_count,
                    include_hashtags=include_hashtags,
                    include_cta=include_cta
                )
            elif submitted and not topic:
                st.error("Please enter a topic to generate posts.")
                return None
            
            return None
    
    @staticmethod
    def render_posts(posts: List[GeneratedPost], metadata: Dict):
        """
        Render generated posts with metadata
        
        Args:
            posts: List of generated posts
            metadata: Generation metadata
        """
        if not posts:
            st.error("No posts were generated. Please try again with a different topic or settings.")
            return
        
        st.success(f"Successfully generated {len(posts)} posts!")
        
        # Generation metadata
        UIComponents._render_generation_metadata(metadata)
        
        # Posts
        for i, post in enumerate(posts, 1):
            UIComponents._render_single_post(post, i)
    
    @staticmethod
    def _render_generation_metadata(metadata: Dict):
        """Render generation metadata in an expander"""
        with st.expander("Generation Details", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Generation Time", f"{metadata.get('generation_time', 0):.2f}s")
                st.metric("Posts Generated", metadata.get('posts_generated', 0))
            
            with col2:
                st.metric("Model Used", metadata.get('model_used', 'N/A'))
                st.metric("Avg Characters", metadata.get('avg_char_count', 0))
            
            with col3:
                quality_dist = metadata.get('quality_distribution', {})
                st.write("**Quality Distribution:**")
                st.write(f"High: {quality_dist.get('high', 0)}")
                st.write(f"Medium: {quality_dist.get('medium', 0)}")
                st.write(f"Low: {quality_dist.get('low', 0)}")
            
            # Enhanced metadata display
            if 'agentic_features_used' in metadata:
                st.write("**AI Agent Features Used:**")
                features = metadata['agentic_features_used']
                feature_list = []
                if features.get('trend_analysis'): feature_list.append("Trend Analysis")
                if features.get('content_inspiration'): feature_list.append("Content Inspiration")
                if features.get('audience_analysis'): feature_list.append("Audience Analysis")
                if features.get('tone_optimization'): feature_list.append("Tone Optimization")
                if features.get('quality_filtering'): feature_list.append("Quality Filtering")
                st.write(", ".join(feature_list))
            
            # Tone analysis
            if 'tone_analysis' in metadata:
                tone_info = metadata['tone_analysis']
                st.write("**Tone Analysis:**")
                st.write(f"Effective tone used: {tone_info.get('effective_tone', 'N/A')}")
                if tone_info.get('tone_optimization'):
                    st.write("Tone was automatically optimized based on research")
            
            # Request parameters
            if 'request_params' in metadata:
                st.write("**Request Parameters:**")
                params = metadata['request_params']
                st.json(params)
    
    @staticmethod
    def _render_single_post(post: GeneratedPost, index: int):
        """Render a single post with metrics and actions"""
        with st.expander(f"Post {index} - {post.engagement_potential} Engagement Potential - Tone: {post.tone_used}", expanded=True):
            # Post content
            st.markdown(post.content)
            
            # Post metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Characters", post.char_count)
            
            with col2:
                st.metric("Quality Score", f"{post.quality_score:.1f}/1.0")
            
            with col3:
                st.metric("Engagement", post.engagement_potential)
                
            with col4:
                st.metric("Tone", post.tone_used)
            
            with col5:
                if post.hashtags:
                    st.metric("Hashtags", len(post.hashtags))
            
            # Action buttons
            col_copy, col_edit, col_analyze = st.columns([1, 1, 2])
            
            with col_copy:
                if st.button(f"Copy", key=f"copy_{index}"):
                    st.code(post.content, language=None)
                    st.success("Post copied! Use Ctrl+A, Ctrl+C to copy from the code block above.")
            
            with col_edit:
                if st.button(f"Customize", key=f"edit_{index}"):
                    st.session_state[f'editing_post_{index}'] = True
            
            # Customization area
            if st.session_state.get(f'editing_post_{index}', False):
                with st.container():
                    st.write("**Customize this post:**")
                    edited_content = st.text_area(
                        "Edit content:",
                        value=post.content,
                        height=200,
                        key=f"edit_content_{index}"
                    )
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("Save Changes", key=f"save_{index}"):
                            post.content = edited_content
                            post.char_count = len(edited_content)
                            st.session_state[f'editing_post_{index}'] = False
                            st.rerun()
                    
                    with col_cancel:
                        if st.button("Cancel", key=f"cancel_{index}"):
                            st.session_state[f'editing_post_{index}'] = False
                            st.rerun()
    
    @staticmethod
    def render_sidebar():
        """Render sidebar with additional information and controls"""
        with st.sidebar:
            st.header("About")
            st.markdown("""
            This AI-powered tool generates professional LinkedIn posts using advanced content planning, trend analysis, and quality control.
            
            **Enhanced Features:**
            - Multi-step AI agent approach
            - Current trend analysis
            - Content inspiration research
            - Content safety filtering
            - Quality scoring and optimization
            - Smart hashtag generation
            - Cost estimation and tracking
            """)
            
            st.header("Tips for Better Posts")
            st.markdown("""
            - **Be specific** with your topic for better trend analysis
            - **Define your audience** for targeted content
            - **Choose appropriate tone** or let AI optimize it
            - **Review and customize** generated content
            - **Test different post types** for variety
            - **Use trending topics** for better reach
            """)
            
            st.header("AI Agent Features")
            st.markdown("""
            **Trend Analysis**: Analyzes current industry trends and discussions
            
            **Content Inspiration**: Studies successful LinkedIn post patterns
            
            **Audience Research**: Understands target audience interests
            
            **Quality Control**: Filters content for professional standards
            
            **Tone Optimization**: Selects most effective tone automatically
            """)
            
            st.header("Settings")
            if st.button("Reset Session"):
                for key in list(st.session_state.keys()):
                    if key.startswith('editing_post_'):
                        del st.session_state[key]
                st.rerun()
    
    @staticmethod
    def render_health_endpoint():
        """Render health check endpoint"""
        health_data = {
            "status": "ok",
            "timestamp": str(datetime.now()),
            "app": Config.APP_TITLE,
            "version": "1.0.0"
        }
        st.json(health_data)
