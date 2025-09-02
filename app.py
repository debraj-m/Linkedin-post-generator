import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def filter_content(text):
    """Filter content for professional standards"""
    try:
        prompt = f"""Please analyze this text for professional LinkedIn standards. 
        Check for:
        1. Appropriate language
        2. No controversial topics
        3. Professional tone
        4. No personal attacks
        
        Text: {text}
        
        Return only 'PASS' if content is appropriate, or 'FAIL: reason' if not."""
        
        response = model.generate_content(prompt)
        result = response.text.strip()
        return result.startswith('PASS'), result
    except Exception as e:
        return False, f"Error in content filtering: {str(e)}"

def generate_hashtags(topic, audience):
    """Generate relevant hashtags based on topic and audience"""
    try:
        prompt = f"""Generate 3-5 highly relevant and trending LinkedIn hashtags for:
        Topic: {topic}
        Audience: {audience if audience else 'professional audience'}
        
        Format: Return only the hashtags, one per line, starting with #"""
        
        response = model.generate_content(prompt)
        hashtags = response.text.strip().split('\n')
        return [tag.strip() for tag in hashtags if tag.strip().startswith('#')]
    except Exception as e:
        return []

def generate_posts(topic, tone, audience, post_count, include_hashtags):
    """Generate LinkedIn posts using Gemini API with enhanced features"""
    try:
        # First, let's plan the content
        planning_prompt = f"""Plan {post_count} engaging LinkedIn posts about "{topic}".
        Consider:
        1. Key points to cover
        2. Engagement hooks
        3. Professional insights
        4. Value proposition for the reader
        
        {f'Target audience: {audience}' if audience else ''}
        {f'Tone should be: {tone}' if tone else ''}"""
        
        # Get the content plan
        plan_response = model.generate_content(planning_prompt)
        content_plan = plan_response.text
        
        # Generate posts based on the plan
        generation_prompt = f"""Using this content plan:
        {content_plan}
        
        Generate {post_count} LinkedIn posts. For each post:
        1. Start with a strong hook
        2. Include valuable insights
        3. End with a clear call-to-action
        4. Keep it professional and engaging
        {f'Maintain a {tone} tone throughout' if tone else ''}
        
        Format:
        - Start each post with "Post 1:", "Post 2:", etc.
        - Keep each post between 1000-1300 characters
        - Make it skimmable with line breaks
        - End with a clear call-to-action"""
        
        # Generate the posts
        response = model.generate_content(generation_prompt)
        content = response.text
        
        # Split posts and process them
        posts = []
        raw_posts = [post.strip() for post in content.split('Post')[1:]]
        
        for post in raw_posts:
            # Check content quality
            is_safe, filter_result = filter_content(post)
            if not is_safe:
                continue
                
            # Add hashtags if requested
            if include_hashtags:
                hashtags = generate_hashtags(topic, audience)
                post = f"{post}\n\n{' '.join(hashtags)}"
            
            posts.append(post)
            
        return posts if posts else None, None
        
    except Exception as e:
        return None, str(e)

    try:
        response = model.generate_content(prompt)
        content = response.text

        # Split posts by looking for numbered patterns
        posts = [post.strip() for post in content.split('Post')[1:]]
        return posts, None

    except Exception as e:
        return None, str(e)

def check_health():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": str(datetime.now())}

def main():
    # Check if it's a health check request
    if "health" in st.query_params:
        st.json(check_health())
        return

    st.set_page_config(
        page_title="LinkedIn Post Generator",
        page_icon="📝",
        layout="centered"
    )

    st.title("LinkedIn Post Generator")
    st.write("Generate engaging LinkedIn posts using AI")

    # Input form
    with st.form("post_generator_form"):
        topic = st.text_area("Topic (required)", 
            placeholder="e.g., cold-start strategies for marketplaces",
            help="Enter the main topic for your LinkedIn posts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tone = st.selectbox(
                "Tone (optional)",
                options=["", "Professional", "Conversational", "Enthusiastic", "Educational"],
                help="Select the tone for your posts"
            )
            
            post_count = st.slider(
                "Number of posts",
                min_value=1,
                max_value=5,
                value=3,
                help="How many posts to generate"
            )

        with col2:
            audience = st.text_input(
                "Target Audience (optional)",
                placeholder="e.g., startup founders, product managers",
                help="Specify your target audience"
            )
            
            include_hashtags = st.checkbox(
                "Include hashtags",
                value=True,
                help="Add relevant hashtags to your posts"
            )

        submitted = st.form_submit_button("Generate Posts")

    if submitted and topic:
        with st.spinner("Generating posts..."):
            posts, error = generate_posts(
                topic=topic,
                tone=tone,
                audience=audience,
                post_count=post_count,
                include_hashtags=include_hashtags
            )

            if error:
                st.error(f"Error generating posts: {error}")
            else:
                # Show generation metadata
                st.success("Posts generated successfully!")
                
                with st.expander("Generation Details", expanded=False):
                    st.markdown("""
                    **Model**: Gemini Pro  
                    **Generated**: {}  
                    **Features**:
                    - Content Planning
                    - Professional Content Filter
                    - Smart Hashtag Generation
                    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                
                for i, post in enumerate(posts, 1):
                    with st.expander(f"Post {i}", expanded=True):
                        st.markdown(post)
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button(f"Copy Post {i}", key=f"copy_{i}"):
                                st.toast("Post copied to clipboard!")
                        with col2:
                            st.caption(f"Character count: {len(post)}")

def cleanup():
    """Cleanup function to handle graceful shutdown"""
    try:
        # Add a small delay to allow gRPC to shut down gracefully
        import time
        time.sleep(0.1)
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()
