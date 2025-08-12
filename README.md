# Feedback Sentiment Analysis Web Application

This web application analyzes feedback sentiment using Azure Text Analytics, generates responses using Groq LLM, and converts responses to audio using Azure Speech Services.

## Features

RUNNING ON CLOUD ON : https://feedback-basf-westeu-1754964536.azurewebsites.net/

- **Sentiment Analysis**: Uses Azure Text Analytics API to analyze feedback sentiment (Positive, Negative, Neutral)
- **LLM-Generated Responses**: Uses Groq API to generate contextual responses based on sentiment
- **Text-to-Speech**: Converts responses to audio using Azure Speech Services with emotion-adjusted voices
- **Dashboard**: View all feedback submissions with analysis results
- **Audio Playback**: Play and download generated audio responses

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Azure Account** (free tier available)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Update the `.env` file with your Azure credentials:

```bash
# Replace with your actual Azure credentials
AZURE_TEXT_ANALYTICS_KEY=your_azure_text_analytics_key_here
AZURE_TEXT_ANALYTICS_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Application

```bash
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## Usage

### Submit Feedback
1. Open the main page at `http://127.0.0.1:5000`
2. Enter your feedback in the text area
3. Click "Analyze Feedback"
4. View the sentiment analysis results and generated response
5. Play or download the audio response (if available)

### View Dashboard
1. Navigate to `http://127.0.0.1:5000/dashboard`
2. View all submitted feedback with analysis results
3. See statistics for positive, negative, and neutral feedback
4. Play or download audio responses

## API Endpoints

- `GET /` - Main feedback form page
- `POST /submit_feedback` - Submit feedback for analysis
- `GET /dashboard` - Dashboard with all feedback
- `GET /download_audio/<feedback_id>` - Download audio response
- `GET /api/feedback` - JSON API for all feedback data

## File Structure

```
basf/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── templates/
│   ├── index.html        # Main feedback form
│   └── dashboard.html    # Feedback dashboard
└── README.md            # This file
```
