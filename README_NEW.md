# 🚀 LinkedIn Post Generator

An AI-powered web application that generates professional LinkedIn posts using Google's Gemini AI with advanced multi-step agent approach.

## ✨ Features

### 🧠 Advanced AI Agent
- **Multi-step content planning**: Strategic content planning → Generation → Quality control → Hashtag generation
- **Content safety filtering**: Professional standards validation
- **Quality scoring**: Engagement potential analysis
- **Smart hashtag generation**: Relevant, trending hashtags

### 📊 Professional Features
- **Cost estimation**: Track API usage and costs
- **Generation analytics**: Performance metrics and timing
- **Customizable inputs**: Tone, audience, post type, length
- **Real-time editing**: Customize generated posts
- **Health monitoring**: System status and diagnostics

### 🎯 Assignment Requirements Compliance
- ✅ **Public web app** with no password requirements
- ✅ **Topic input** (required) + optional parameters
- ✅ **Generate ≥3 LinkedIn posts** (configurable 1-5)
- ✅ **Multi-step agent behavior**: Planning → Generation → Filtering → Hashtag generation
- ✅ **Quality guardrails**: Content filtering and safety checks
- ✅ **Cost/latency info**: Token usage and time tracking
- ✅ **/health endpoint**: Status monitoring
- ✅ **Free tier compatible**: Uses Gemini Flash model

## 🏗️ Architecture

```
📁 src/
├── 📁 agents/
│   └── linkedin_post_agent.py    # Main AI agent with multi-step approach
├── 📁 utils/
│   ├── gemini_client.py          # Gemini AI client wrapper
│   ├── content_filter.py         # Content safety & quality control
│   ├── hashtag_generator.py      # Smart hashtag generation
│   └── cost_estimator.py         # API usage tracking
├── 📁 ui/
│   └── components.py             # Streamlit UI components
└── config.py                     # Application configuration

📄 app_modular.py                 # Main modular application
📄 app.py                         # Legacy monolithic version
📄 test_app.py                    # Automated testing script
```

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repository-url>
cd nugget-assignment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run Application
```bash
streamlit run app_modular.py
```

### 4. Test Everything Works
```bash
python test_app.py
```

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Add `GEMINI_API_KEY` to secrets
4. Deploy `app_modular.py`

### Option 2: Render
1. Create new Web Service on [render.com](https://render.com)
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `streamlit run app_modular.py --server.port $PORT --server.address 0.0.0.0`
4. Add environment variable: `GEMINI_API_KEY`

### Option 3: Railway
1. Deploy to [railway.app](https://railway.app)
2. Add `GEMINI_API_KEY` environment variable
3. Railway will auto-detect Streamlit app

### Option 4: Hugging Face Spaces
1. Create new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose Streamlit SDK
3. Upload files and add secrets

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY` (required): Your Google Gemini API key
- `APP_ENV` (optional): Application environment (production/development)
- `DEBUG` (optional): Enable debug mode

### Application Settings
Edit `src/config.py` to customize:
- Model preferences
- Post length limits
- Tone options
- Default settings

## 🧪 Testing

```bash
# Run automated tests
python test_app.py

# Test individual components
python -m pytest tests/  # If you add pytest

# Manual testing
streamlit run app_modular.py
# Navigate to http://localhost:8501/health for health check
```

## 📊 API Usage & Costs

The app uses **Gemini 1.5 Flash** model by default (most cost-effective):
- **Input**: ~$0.075 per 1M tokens
- **Output**: ~$0.30 per 1M tokens
- **Typical cost per generation**: $0.001-0.005

Cost tracking is built-in and displayed in the UI.

## 🛡️ Content Safety

Multi-layer content filtering:
1. **Professional standards check**: Language, tone, appropriateness
2. **Quality scoring**: Engagement potential analysis
3. **Length validation**: Character count limits
4. **Hashtag validation**: Relevant, professional hashtags

## 🎯 Assignment Features Implemented

### Core Requirements ✅
- **Topic input** + optional parameters (tone, audience, type, count)
- **≥3 LinkedIn post options** (configurable 1-5 posts)
- **Live public URL** (deployment ready)
- **Health endpoint** (`/health`)

### Advanced Agent Features ✅
- **Multi-step approach**: Planning → Generation → Quality Control → Hashtag Generation
- **Content filtering**: Professional standards validation
- **Smart hashtag generation**: Separate AI function for relevant hashtags
- **Quality guardrails**: Safety and engagement scoring

### Technical Features ✅
- **Cost estimation**: Token usage and pricing
- **Generation metadata**: Model info, timing, quality metrics
- **Error handling**: Robust error recovery
- **Modular architecture**: Clean, maintainable code

## 🔮 Future Enhancements

With more time, I would add:
- **Web search integration**: Real-time trend analysis
- **A/B testing**: Multiple tone variations
- **Analytics dashboard**: Usage patterns and performance
- **Template library**: Pre-built post templates
- **Scheduling integration**: Direct LinkedIn posting
- **Multi-language support**: Global content generation

## 📞 Support

For issues or questions:
1. Check the `/health` endpoint for system status
2. Review logs in the Streamlit interface
3. Verify your `GEMINI_API_KEY` is valid
4. Run `python test_app.py` for diagnostics

## 📄 License

MIT License - Feel free to use and modify as needed.

---

**Built with ❤️ using Streamlit, Google Gemini AI, and Python**
