# Feedback Sentiment Analysis Web Application

This web application analyzes feedback sentiment using Azure Text Analytics, generates responses using Groq LLM, and converts responses to audio using Azure Speech Services.

## Features

- **Sentiment Analysis**: Uses Azure Text Analytics API to analyze feedback sentiment (Positive, Negative, Neutral)
- **LLM-Generated Responses**: Uses Groq API to generate contextual responses based on sentiment
- **Text-to-Speech**: Converts responses to audio using Azure Speech Services with emotion-adjusted voices
- **Dashboard**: View all feedback submissions with analysis results
- **Audio Playback**: Play and download generated audio responses

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Azure Account** (free tier available)
3. **Groq API Key** (already provided)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Azure Services Setup

#### Azure Text Analytics (Free Tier Available)
1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new "Language" (Text Analytics) resource
3. Choose the **Free tier (F0)** - includes 5,000 transactions per month
4. Copy the **Key** and **Endpoint** from the resource
5. Update your `.env` file with the actual values

#### Azure Speech Services (Free Tier Available)
1. In Azure Portal, create a "Speech Services" resource
2. Choose the **Free tier (F0)** - includes 5 hours of speech synthesis per month
3. Copy the **Key** and **Region** from the resource
4. Update your `.env` file with the actual values

**📋 Detailed Setup Guide**: See `AZURE_SETUP.md` for complete step-by-step instructions with screenshots and troubleshooting tips.

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

## Azure Pricing Information

### Text Analytics API
- **Free Tier (F0)**: 5,000 transactions per month
- **Standard Tier**: Pay per transaction
- Perfect for development and testing

### Speech Services
- **Free Tier (F0)**: 5 hours of speech synthesis per month
- **Standard Tier**: Pay per character synthesized
- Sufficient for moderate usage

## Fallback Features

The application includes fallback mechanisms:
- Simple keyword-based sentiment analysis if Azure Text Analytics is unavailable
- Pre-defined responses if Groq API is unavailable
- Graceful handling of audio generation failures

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Sentiment Analysis**: Azure Text Analytics API
- **LLM**: Groq API (Mixtral-8x7B model)
- **Text-to-Speech**: Azure Speech Services
- **Styling**: Modern CSS with responsive design

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

## Customization

### Adding New Sentiment Categories
Modify the sentiment analysis logic in `app.py` to handle additional categories.

### Changing LLM Prompts
Update the prompt templates in the `generate_llm_response()` function.

### Adjusting Audio Voices
Modify the voice mapping in the `text_to_speech()` function to use different Azure voices.

## Troubleshooting

### Audio Issues
- Ensure Azure Speech Services credentials are correct
- Check that the region matches your Azure resource
- Verify you haven't exceeded the free tier limits

### Sentiment Analysis Issues
- Verify Azure Text Analytics credentials
- Check endpoint URL format
- Ensure you have available transactions in your quota

### LLM Issues
- Verify Groq API key is correct
- Check Groq API status and rate limits
