import os
from flask import Flask, render_template, request, jsonify, send_file
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speechsdk
from groq import Groq
from dotenv import load_dotenv
import tempfile
import uuid
from datetime import datetime

load_dotenv()

app = Flask(__name__)

azure_key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
azure_endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
text_analytics_client = TextAnalyticsClient(
    endpoint=azure_endpoint,
    credential=AzureKeyCredential(azure_key)
) if azure_key and azure_endpoint else None

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

groq_api_key = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None

feedback_data = []

def analyze_sentiment(text):
    """Analyze sentiment using Azure Text Analytics"""
    if not text_analytics_client:
        # Fallback simple sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'sad', 'disappointed']
        
        text_lower = text.lower()
        pos_count = sum(word in text_lower for word in positive_words)
        neg_count = sum(word in text_lower for word in negative_words)
        
        if pos_count > neg_count:
            return "Positive", 0.8
        elif neg_count > pos_count:
            return "Negative", 0.8
        else:
            return "Neutral", 0.6
    
    try:
        documents = [text]
        response = text_analytics_client.analyze_sentiment(documents=documents)[0]
        
        sentiment = response.sentiment.capitalize()
        confidence = response.confidence_scores.__dict__[response.sentiment.lower()]
        
        return sentiment, confidence
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Neutral", 0.5

def generate_llm_response(feedback, sentiment):
    """Generate response using Groq LLM"""
    if not groq_client:
        responses = {
            "Positive": "Thank you for your positive feedback! We're delighted to hear about your experience.",
            "Negative": "We apologize for any inconvenience. Your feedback is valuable and we'll work to improve.",
            "Neutral": "Thank you for sharing your feedback. We appreciate your input."
        }
        return responses.get(sentiment, "Thank you for your feedback.")
    
    try:
        prompt_templates = {
            "Positive": f"The customer provided positive feedback: '{feedback}'. Generate a brief, appreciative response (2-3 sentences) acknowledging their positive experience.",
            "Negative": f"The customer provided negative feedback: '{feedback}'. Generate a brief, empathetic response (2-3 sentences) acknowledging their concerns and showing commitment to improvement.",
            "Neutral": f"The customer provided neutral feedback: '{feedback}'. Generate a brief, professional response (2-3 sentences) thanking them and encouraging further engagement."
        }
        
        prompt = prompt_templates.get(sentiment, f"Respond professionally to this feedback: '{feedback}'")
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional customer service representative. Provide concise, empathetic, and appropriate responses to customer feedback."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=150,
            temperature=0.7
        )
        
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        fallback_responses = {
            "Positive": "Thank you for your positive feedback! We're delighted to hear about your experience.",
            "Negative": "We apologize for any inconvenience. Your feedback is valuable and we'll work to improve.",
            "Neutral": "Thank you for sharing your feedback. We appreciate your input."
        }
        return fallback_responses.get(sentiment, "Thank you for your feedback.")

def text_to_speech(text, sentiment):
    """Convert text to speech using Azure Speech Services"""
    if not speech_key or not speech_region:
        return None, "Azure Speech Services not configured"
    
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        
        voice_map = {
            "Positive": "en-US-JennyNeural",  
            "Negative": "en-US-AriaNeural",   
            "Neutral": "en-US-DavisNeural"   
        }
        
        speech_config.speech_synthesis_voice_name = voice_map.get(sentiment, "en-US-AriaNeural")
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()  # Close the file handle so Azure SDK can write to it
        
        audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file.name)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # Clean the text to avoid special characters that might cause issues
        clean_text = text.replace('"', '').replace("'", "").strip()
        
        # Use plain text synthesis for better compatibility
        result = synthesizer.speak_text_async(clean_text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return temp_file.name, None
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speechsdk.CancellationDetails(result)
            error_msg = f"Speech cancelled: {cancellation_details.reason}"
            if cancellation_details.error_details:
                error_msg += f" - {cancellation_details.error_details}"
            return None, error_msg
        else:
            return None, f"Speech synthesis failed: {result.reason}"
            
    except Exception as e:
        # Fallback message for speech issues
        return None, f"Audio generation temporarily unavailable: {str(e)[:100]}..."

@app.route('/')
def index():
    """Main page with feedback form"""
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    """Process submitted feedback"""
    try:
        feedback_text = request.json.get('feedback', '').strip()
        
        if not feedback_text:
            return jsonify({'error': 'Feedback cannot be empty'}), 400
        
        # Analyze sentiment
        sentiment, confidence = analyze_sentiment(feedback_text)
        
        # Generate LLM response
        llm_response = generate_llm_response(feedback_text, sentiment)
        
        # Generate audio
        audio_file, audio_error = text_to_speech(llm_response, sentiment)
        
        # Create feedback record
        feedback_record = {
            'id': str(uuid.uuid4()),
            'feedback': feedback_text,
            'sentiment': sentiment,
            'confidence': round(confidence, 2),
            'llm_response': llm_response,
            'audio_file': audio_file,
            'timestamp': datetime.now().isoformat(),
            'audio_error': audio_error
        }
        
        feedback_data.append(feedback_record)
        
        response_data = {
            'id': feedback_record['id'],
            'sentiment': sentiment,
            'confidence': round(confidence, 2),
            'llm_response': llm_response,
            'has_audio': audio_file is not None,
            'audio_error': audio_error
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/download_audio/<feedback_id>')
def download_audio(feedback_id):
    """Download audio file for a feedback response"""
    try:
        # Find feedback record
        feedback_record = next((f for f in feedback_data if f['id'] == feedback_id), None)
        
        if not feedback_record:
            return jsonify({'error': 'Feedback not found'}), 404
        
        if not feedback_record.get('audio_file'):
            return jsonify({'error': 'Audio file not available'}), 404
        
        return send_file(
            feedback_record['audio_file'],
            as_attachment=True,
            download_name=f'response_{feedback_id}.wav',
            mimetype='audio/wav'
        )
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard showing all feedback"""
    return render_template('dashboard.html', feedback_data=feedback_data)

@app.route('/api/feedback')
def get_feedback():
    """API endpoint to get all feedback data"""
    return jsonify(feedback_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
