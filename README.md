# LinkedIn Post Generator

A Streamlit web application that generates engaging LinkedIn posts using Google's Gemini Pro AI. The app includes features like content planning, professional tone control, and smart hashtag generation.

## Features

- Generate multiple LinkedIn post variations from a single topic
- Two-step generation process (planning + execution)
- Content quality filters and professional tone control
- Smart hashtag generation
- Character count tracking
- Copy to clipboard functionality
- Mobile-responsive design

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

5. Run the app locally:
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Log in with your GitHub account

4. Deploy your app:
   - Click "New app"
   - Select your repository and branch
   - Set the main file path as `app.py`
   - Add your `GEMINI_API_KEY` to the secrets
   - Click "Deploy"

## Environment Variables

The following environment variables are required:
- `GEMINI_API_KEY`: Your Google Gemini Pro API key

To set these in Streamlit Cloud:
1. Go to your app settings
2. Click on "Secrets"
3. Add your environment variables in the format:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

## Health Check

The application includes a health check endpoint accessible at:
```
https://your-app-url.streamlit.app/?health
```

## Technical Details

- **Framework**: Streamlit
- **Language**: Python
- **AI Integration**: Google Gemini Pro
- **Features**:
  - Two-step content generation
  - Professional content filtering
  - Smart hashtag generation
  - Character count tracking

## Future Improvements

- Save favorite posts
- Integration with LinkedIn API for direct posting
- More customization options
- A/B testing different post styles
