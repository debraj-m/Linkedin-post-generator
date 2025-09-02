# LinkedIn Post Generator

An AI-powered web application that generates professional LinkedIn posts using Google's Gemini AI. Built with enhanced agentic capabilities, cost tracking, and production-ready features for assignment submission.

## Requirements Fulfilled

### Core Requirements
- **Topic input** with optional parameters (tone, audience, post count)
- **Multiple post generation** (1-5 LinkedIn posts per request)
- **Public web deployment** (no authentication required)
- **Health endpoint** returns 200 OK at `/?health` parameter
- **Enhanced agentic behavior** with 8-step AI workflow
- **Cost tracking** with real-time token usage and pricing
- **Quality guardrails** with professional content filtering

### 8-Step AI Agent Workflow
1. **Trend Analysis** - Research current industry trends and topics
2. **Content Inspiration** - Study successful LinkedIn post patterns  
3. **Audience Analysis** - Target specific professional demographics
4. **Strategic Planning** - Structure optimized content approach
5. **Content Generation** - AI-powered post creation with personalization
6. **Quality Control** - Professional standards and safety validation
7. **Hashtag Research** - Generate relevant, trending hashtags
8. **Final Assembly** - Polish and deliver ready-to-publish content

## Project Architecture

### Clean Modular Structure
```
nugget-assignment/
├── app_modular.py              # Main Streamlit application
├── src/                        # Source code modules
│   ├── agents/                 # AI agent orchestration
│   │   └── linkedin_post_agent.py
│   ├── utils/                  # Utility functions
│   │   ├── gemini_client.py    # Google Gemini AI client
│   │   ├── cost_estimator.py   # Token usage and cost tracking
│   │   ├── content_filter.py   # Content safety and quality control
│   │   ├── hashtag_generator.py # Smart hashtag generation
│   │   └── trend_analyzer.py   # Industry trend research
│   ├── ui/                     # User interface components
│   │   └── components.py       # Streamlit UI components
│   └── config.py               # Application configuration
├── test_app.py                 # Automated test suite
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # This documentation
```

## Quick Start Guide

### 1. Environment Setup
```bash
# Clone the repository
git clone <your-repository-url>
cd nugget-assignment

# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Google Gemini API key
GEMINI_API_KEY=your_google_gemini_api_key_here
```

**Get API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste into `.env` file

### 3. Run Application
```bash
# Start the Streamlit application
streamlit run app_modular.py

# Application will be available at:
# Local: http://localhost:8501
# Network: http://your-ip:8501
```

### 4. Alternative Port Configuration
```bash
# Run on different port if 8501 is busy
streamlit run app_modular.py --server.port 8502

# Or specify custom port
streamlit run app_modular.py --server.port 8080
```

## Health Endpoint

### Live Application Links
- **Main App**: https://linkedin-post-generator-debraj-m.streamlit.app/
- **Health Check**: https://linkedin-post-generator-debraj-m.streamlit.app/?health

### Production Health Check

#### Browser Access (Recommended)
```
Open: https://linkedin-post-generator-debraj-m.streamlit.app/?health
```

#### Command Line Testing
```bash
# Using curl
curl "https://linkedin-post-generator-debraj-m.streamlit.app/?health"

# Using PowerShell (Windows)
Invoke-RestMethod -Uri "https://linkedin-post-generator-debraj-m.streamlit.app/?health"

# Using Python
python -c "import requests; print(requests.get('https://linkedin-post-generator-debraj-m.streamlit.app/?health').json())"
```

#### Online Testing Tools
Use any HTTP testing tool with:
```
GET https://linkedin-post-generator-debraj-m.streamlit.app/?health
```

### Expected Health Response
```json
{
  "status": "healthy",
  "timestamp": "2025-09-03T10:30:00",
  "app": "LinkedIn Post Generator", 
  "version": "2.0.0",
  "agent_status": "healthy",
  "model_info": {
    "model_name": "gemini-1.5-flash",
    "provider": "Google"
  }
}
```

### Status Indicators
- **`healthy`** - All systems operational
- **`degraded`** - Some issues but functional
- **`unhealthy`** - Major issues detected

### Health Check Access (Local Development)
The application provides a health monitoring endpoint:

**URL Pattern:**
```
http://localhost:8501/?health
```

**Status Codes:**
- `healthy` - All systems operational
- `degraded` - Some issues but functional
- `unhealthy` - Major issues detected

### Health Check Testing (Local Development)
```bash
# Method 1: Browser
# Open: http://localhost:8501/?health

# Method 2: Command Line (if curl available)
curl "http://localhost:8501/?health"

# Method 3: Python script
python -c "import requests; print(requests.get('http://localhost:8501/?health').json())"
```

## Application Usage

### Basic Usage Flow
1. **Open Application**: Navigate to `http://localhost:8501`
2. **Enter Topic**: Provide a LinkedIn post topic (required)
3. **Configure Options** (optional):
   - **Tone**: Professional, Casual, Thought Leadership
   - **Audience**: Business Leaders, Entrepreneurs, General Professional
   - **Post Count**: 1-5 posts per generation
4. **Generate Posts**: Click "Generate Posts" button
5. **Review Results**: View generated content with cost tracking

### Advanced Features
- **Real-time Cost Tracking**: Monitor API usage and costs
- **Multiple Post Variants**: Generate up to 5 different posts
- **Professional Quality Control**: AI-enforced business standards
- **Smart Hashtag Generation**: Relevant, trending hashtags
- **Progress Indicators**: 8-step workflow visualization

## 💰 Cost Information & Performance

### API Pricing (Google Gemini 1.5 Flash)
- **Input Tokens**: $0.075 per 1M tokens
- **Output Tokens**: $0.30 per 1M tokens
- **Typical Cost per Generation**: $0.002-0.003

### Real Performance Data
Based on actual testing with 7 API requests:
- **Total Cost**: $0.002321
- **Average Input Tokens**: 1,370 per request
- **Average Output Tokens**: 762 per request
- **Response Time**: 5-10 seconds per generation

### Cost Tracking Features
- Real-time token usage display
- Session cost summaries
- Per-request cost breakdown
- Historical usage tracking

## 🧪 Testing & Validation

### Automated Testing
```bash
# Run complete test suite
python -m pytest test_app.py -v

# Test individual components
python -c "from test_app import test_configuration; test_configuration()"
python -c "from test_app import test_agent_initialization; test_agent_initialization()"
python -c "from test_app import test_post_generation; test_post_generation()"
```

### Manual Testing
```bash
# 1. Start application
streamlit run app_modular.py

# 2. Test main functionality
# Navigate to http://localhost:8501
# Generate a test post

# 3. Test health endpoint
# Navigate to http://localhost:8501/?health

# 4. Verify cost tracking
# Check cost information in UI after generation
```

## Deployment Options

### Streamlit Cloud (Recommended)
1. **Push to GitHub**: Commit all code to repository
2. **Connect to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
3. **Deploy Application**:
   - Repository: Select your GitHub repo
   - Main file: `app_modular.py`
   - Python version: 3.12
4. **Add Secrets**: 
   - Go to App Settings → Secrets
   - Add: `GEMINI_API_KEY = "your_api_key"`

### Local Development
```bash
# Standard port
streamlit run app_modular.py

# Custom port
streamlit run app_modular.py --server.port 8080

# External access
streamlit run app_modular.py --server.address 0.0.0.0
```

### Alternative Platforms
- **Render**: Web service with `streamlit run app_modular.py`
- **Railway**: Auto-detection of Streamlit apps
- **Heroku**: Using Procfile with Streamlit commands

## Configuration Options

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_google_gemini_api_key

# Optional
APP_ENV=production          # Environment setting
DEBUG=false                 # Debug mode toggle
STREAMLIT_PORT=8501        # Custom port setting
```

### Application Settings
Edit `src/config.py` to customize:
- Model preferences and parameters
- Post generation limits and defaults
- Available tone and audience options
- UI component configurations

## Content Safety & Quality

### Multi-Layer Content Filtering
1. **Input Validation**: Topic and parameter sanitization
2. **AI Safety Guidelines**: Professional business communication standards
3. **Content Quality Scoring**: Engagement potential analysis
4. **Length Optimization**: Ideal character count for LinkedIn
5. **Hashtag Validation**: Relevant, professional hashtag selection
6. **Final Review**: Automated quality assurance checks

### Professional Standards
- Business-appropriate language enforcement
- LinkedIn platform guidelines compliance
- Corporate communication best practices
- Brand-safe content generation

## 🆘 Troubleshooting

### Common Issues & Solutions

#### API Key Errors
```bash
# Problem: Invalid or missing API key
# Solution: Verify .env file configuration
cat .env  # Check if GEMINI_API_KEY is set
```

#### Port Conflicts
```bash
# Problem: Port 8501 already in use
# Solution: Use alternative port
streamlit run app_modular.py --server.port 8502
```

#### Import Errors
```bash
# Problem: Module not found errors
# Solution: Ensure virtual environment is activated
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

#### Performance Issues
```bash
# Problem: Slow response times
# Solution: Check internet connection and API limits
python -c "from test_app import test_agent_initialization; test_agent_initialization()"
```

### Diagnostic Commands
```bash
# Test configuration
python -c "from src.config import Config; print(Config.validate_config())"

# Test API connection
python -c "from src.agents.linkedin_post_agent import LinkedInPostAgent; agent = LinkedInPostAgent(); print(agent.get_health_status())"

# Test health endpoint
# Visit: http://localhost:8501/?health
```

## Compliance Checklist

### Required Features
- [x] **Topic input field** with validation
- [x] **Optional parameters** (tone, audience, post count)
- [x] **Multiple post generation** (1-5 posts configurable)
- [x] **Public web application** (no authentication required)
- [x] **Health endpoint** returning 200 OK status

### Enhanced Features  
- [x] **Advanced agentic behavior** (8-step AI workflow)
- [x] **Quality guardrails** and content filtering
- [x] **Cost estimation** with real-time tracking
- [x] **Professional UI** with progress indicators
- [x] **Comprehensive testing** and validation
- [x] **Production deployment** readiness

### Technical Excellence
- [x] **Modular architecture** for maintainability
- [x] **Error handling** and user feedback
- [x] **Performance optimization** for cost efficiency
- [x] **Security best practices** for API key management
- [x] **Documentation** and code comments

## Dependencies

```txt
streamlit>=1.27.0           # Web application framework
google-generativeai>=0.8.0 # Google Gemini AI integration  
python-dotenv>=1.0.0        # Environment variable management
protobuf>=4.25.1           # Protocol buffer support
typing-extensions>=4.5.0   # Enhanced type hints
pytest>=8.4.0              # Testing framework
```

**Python Version Requirements:**
- Minimum: Python 3.8+
- Recommended: Python 3.12+
- Tested: Python 3.12.1

## 📄 License & Credits

**MIT License** - Open source and free to use, modify, and distribute.

### Built With
- **[Streamlit](https://streamlit.io)** - Interactive web application framework
- **[Google Gemini AI](https://ai.google.dev)** - Advanced language model for content generation
- **[Python](https://python.org)** - Core programming language

### Project Information
- **Version**: 2.0.0 (Assignment Submission)
- **Author**: AI Application Development
- **Last Updated**: January 2025
- **Repository**: Linkedin-post-generator

---

**🎯 Assignment-ready LinkedIn Post Generator with enterprise-grade features, comprehensive documentation, and production deployment capabilities.**