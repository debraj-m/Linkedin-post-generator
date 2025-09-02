"""
Test script for LinkedIn Post Generator
"""
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import Config
from src.agents.linkedin_post_agent import LinkedInPostAgent, PostRequest

def test_configuration():
    """Test configuration validation"""
    print("Testing configuration...")
    errors = Config.validate_config()
    if errors:
        print(f"❌ Configuration errors: {errors}")
        return False
    print("✅ Configuration valid")
    return True

def test_agent_initialization():
    """Test agent initialization"""
    print("Testing agent initialization...")
    try:
        agent = LinkedInPostAgent()
        health = agent.get_health_status()
        if health["status"] == "healthy":
            print(f"✅ Agent initialized successfully with {health['model_info']['model_name']}")
            return agent
        else:
            print(f"❌ Agent unhealthy: {health['message']}")
            return None
    except Exception as e:
        print(f"❌ Agent initialization failed: {str(e)}")
        return None

def test_post_generation(agent):
    """Test post generation"""
    print("Testing post generation...")
    try:
        request = PostRequest(
            topic="AI in business transformation",
            tone="Professional",
            audience="business leaders",
            post_count=2,
            include_hashtags=True
        )
        
        posts, metadata = agent.generate_posts(request)
        
        if posts and len(posts) > 0:
            print(f"✅ Generated {len(posts)} posts successfully")
            print(f"   Model: {metadata.get('model_used', 'N/A')}")
            print(f"   Time: {metadata.get('generation_time', 0):.2f}s")
            return True
        else:
            print(f"❌ No posts generated. Error: {metadata.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Post generation failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running LinkedIn Post Generator Tests\n")
    
    # Test 1: Configuration
    if not test_configuration():
        print("\n❌ Tests failed at configuration validation")
        return False
    
    # Test 2: Agent initialization
    agent = test_agent_initialization()
    if not agent:
        print("\n❌ Tests failed at agent initialization")
        return False
    
    # Test 3: Post generation
    if not test_post_generation(agent):
        print("\n❌ Tests failed at post generation")
        return False
    
    print("\n✅ All tests passed! Your application is ready to deploy.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
