"""
UI components for Streamlit interface - Simplified Copy Version
"""
import streamlit as st
from typing import Dict, List
from datetime import datetime
from src.agents.linkedin_post_agent import GeneratedPost, PostRequest
from src.config import Config
from src.utils.clipboard_helper import ClipboardHelper

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

            # Submit button
            submitted = st.form_submit_button("Generate Posts", type="primary")
            
            if submitted:
                if not topic.strip():
                    st.error("Please enter a topic to generate posts.")
                    return None
                
                # Create PostRequest object
                return PostRequest(
                    topic=topic.strip(),
                    tone=tone,
                    post_type=post_type,
                    post_count=post_count,
                    audience=audience,
                    include_hashtags=include_hashtags,
                    include_cta=include_cta
                )
            
            return None
    
    @staticmethod
    def render_posts(posts: List[GeneratedPost], metadata: Dict):
        """
        Render generated posts with simplified copy functionality
        """
        if not posts:
            st.error("No posts were generated. Please try again with a different topic or settings.")
            return
        
        st.success(f"Successfully generated {len(posts)} posts!")
        
        # Store posts in session state for potential future use
        st.session_state['current_posts'] = posts
        
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
        """Render a single post with simplified copy functionality"""
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
            
            # Simple copy section
            st.markdown("---")
            st.markdown("**📋 Copy this post:**")
            
            # Single copy button
            copy_html = ClipboardHelper.create_copy_button_html(
                content=post.content,
                button_id=f"post_{index}",
                button_text="📋 Copy to Clipboard"
            )
            st.components.v1.html(copy_html, height=60)
            
            # Fallback text area
            st.text_area(
                "Or select manually (triple-click to select all):",
                value=post.content,
                height=100,
                key=f"manual_{index}_{hash(post.content) % 10000}",
                help="Triple-click to select all, then Ctrl+C (Windows) or Cmd+C (Mac) to copy"
            )
            
            # Simple download option
            col_dl, col_edit = st.columns(2)
            with col_dl:
                st.download_button(
                    label="💾 Download",
                    data=post.content,
                    file_name=f"post_{index}.txt",
                    mime="text/plain",
                    key=f"dl_{index}_{hash(post.content) % 10000}"
                )
            
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
            
            st.header("Copy Instructions")
            st.markdown("""
            **To copy a post:**
            1. Click the "📋 Copy to Clipboard" button for instant copy
            2. Or triple-click in the text area and press Ctrl+C
            3. Use the download button to save as a file
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
