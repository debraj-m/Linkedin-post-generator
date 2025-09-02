"""
LinkedIn Post Generator - Modular Streamlit Application
A professional AI-powered tool for generating LinkedIn posts with advanced features.
"""

import streamlit as st
import sys
import os
from datetime import datetime
from typing import Dict

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import Config
from src.agents.linkedin_post_agent import LinkedInPostAgent
from src.ui.components import UIComponents

class LinkedInPostGeneratorApp:
    """Main application class"""
    
    def __init__(self):
        self.agent = None
        self._initialize_session_state()
        self._initialize_agent()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state"""
        if 'agent_healthy' not in st.session_state:
            st.session_state.agent_healthy = False
        
        if 'generation_count' not in st.session_state:
            st.session_state.generation_count = 0
    
    def _initialize_agent(self):
        """Initialize the LinkedIn post agent"""
        try:
            # Validate configuration
            config_errors = Config.validate_config()
            if config_errors:
                st.error(f"Configuration Error: {'; '.join(config_errors)}")
                st.stop()
            
            # Initialize agent
            self.agent = LinkedInPostAgent()
            
            # Test agent health
            health_status = self.agent.get_health_status()
            st.session_state.agent_healthy = health_status["status"] == "healthy"
            
            if not st.session_state.agent_healthy:
                st.error("Agent initialization failed: " + health_status['message'])
                st.write("**Troubleshooting:**")
                st.write("1. Check your GEMINI_API_KEY environment variable")
                st.write("2. Ensure you have access to Google's Gemini API")
                st.write("3. Verify your internet connection")
                st.stop()
                
        except Exception as e:
            st.error(f"Failed to initialize AI agent: {str(e)}")
            st.session_state.agent_healthy = False
            st.stop()
    
    def run(self):
        """Main application entry point"""
        # Check for health endpoint
        if self._is_health_check():
            self._handle_health_check()
            return
        
        # Render UI
        UIComponents.render_header()
        UIComponents.render_sidebar()
        
        # Main content area
        self._render_main_content()
        
        # Footer
        self._render_footer()
    
    def _is_health_check(self) -> bool:
        """Check if this is a health check request"""
        try:
            query_params = st.query_params
            return "health" in query_params
        except:
            return False
    
    def _handle_health_check(self):
        """Handle health check endpoint"""
        health_data = {
            "status": "healthy",
            "timestamp": str(datetime.now()),
            "app": "LinkedIn Post Generator",
            "version": "2.0.0",
            "agent_status": "healthy" if st.session_state.agent_healthy else "unhealthy"
        }
        
        if self.agent and st.session_state.agent_healthy:
            try:
                agent_health = self.agent.get_health_status()
                health_data["model_info"] = agent_health.get("model_info", {})
            except Exception as e:
                health_data["agent_error"] = str(e)
                health_data["status"] = "degraded"
        
        st.success("✅ Health Check: Service is healthy")
        st.json(health_data)
    
    def _render_main_content(self):
        """Render main application content"""
        # Input form
        post_request = UIComponents.render_input_form()
        
        # Generate posts if form submitted
        if post_request:
            self._handle_post_generation(post_request)
    
    def _handle_post_generation(self, post_request):
        """Handle post generation request"""
        with st.spinner("AI Agent is analyzing trends and generating your posts..."):
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Trend Analysis
                status_text.text("Step 1/8: Analyzing current trends and discussions...")
                progress_bar.progress(12)
                
                # Step 2: Content Inspiration
                status_text.text("Step 2/8: Researching successful content patterns...")
                progress_bar.progress(25)
                
                # Step 3: Audience Analysis
                status_text.text("Step 3/8: Understanding audience interests...")
                progress_bar.progress(37)
                
                # Step 4: Strategic Planning
                status_text.text("Step 4/8: Creating strategic content plan...")
                progress_bar.progress(50)
                
                # Step 5: Content Generation
                status_text.text("Step 5/8: Generating optimized post content...")
                progress_bar.progress(62)
                
                # Step 6: Quality Control
                status_text.text("Step 6/8: Quality control and content filtering...")
                progress_bar.progress(75)
                
                # Step 7: Hashtag Generation
                status_text.text("Step 7/8: Generating relevant hashtags...")
                progress_bar.progress(87)
                
                # Generate posts
                posts, metadata = self.agent.generate_posts(post_request)
                
                # Step 8: Finalization
                status_text.text("Step 8/8: Finalizing posts and analysis...")
                progress_bar.progress(100)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                if "error" in metadata:
                    st.error(f"Generation failed: {metadata['error']}")
                    return
                
                # Update session state
                st.session_state.generation_count += 1
                
                # Render results
                UIComponents.render_posts(posts, metadata)
                
                # Cost estimation
                self._render_cost_estimation(metadata)
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"An error occurred during generation: {str(e)}")
    
    def _render_cost_estimation(self, metadata: Dict):
        """Render cost estimation information"""
        with st.expander("Cost Estimation", expanded=False):
            # Get cost estimator from the agent
            cost_estimator = self.agent.get_cost_estimator()
            session_summary = cost_estimator.get_session_summary()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Session Requests", session_summary["total_requests"])
                st.metric("Total Cost", session_summary["cost_formatted"])
            
            with col2:
                st.metric("Input Tokens", session_summary["total_input_tokens"])
                st.metric("Output Tokens", session_summary["total_output_tokens"])
            
            with col3:
                st.metric("Session Duration", f"{session_summary['session_duration_minutes']:.1f} min")
                st.metric("Avg Cost/Request", f"${session_summary['avg_cost_per_request']:.6f}")
            
            st.info("**Note:** Cost estimates are approximate and based on token estimation. Actual costs may vary.")
            
            # Debug information
            if session_summary["total_requests"] == 0:
                st.warning("**Debug:** No API requests tracked yet. This might indicate cost tracking isn't properly initialized.")
    
    def _render_footer(self):
        """Render application footer"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**AI Agent Features:**")
            st.markdown("- Multi-step content planning")
            st.markdown("- Trend analysis and research")
            st.markdown("- Content inspiration discovery")
            st.markdown("- Quality control & filtering")
            st.markdown("- Smart hashtag generation")
        
        with col2:
            st.markdown("**Session Stats:**")
            st.markdown(f"- Posts generated: {st.session_state.generation_count}")
            st.markdown(f"- Agent status: {'Healthy' if st.session_state.agent_healthy else 'Unhealthy'}")
        
        with col3:
            st.markdown("**Quick Actions:**")
            if st.button("Restart Session"):
                st.cache_data.clear()
                st.rerun()
        
        # Attribution
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8em; margin-top: 2rem;'>
            LinkedIn Post Generator | Powered by Google Gemini AI | Built with Streamlit
        </div>
        """, unsafe_allow_html=True)

def main():
    """Application entry point"""
    try:
        app = LinkedInPostGeneratorApp()
        app.run()
    except Exception as e:
        st.error(f"Application startup failed: {str(e)}")
        st.write("Please check your configuration and try refreshing the page.")

if __name__ == "__main__":
    main()
