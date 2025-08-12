Exercises:
Develop a web application that allows users to submit feedback, analyzes that sentiment, and then
uses a LLM to generate appropriate responses in text and audio based on the sentiment.
Requirements:
Web Application Setup:
• Use Python with Flask or Django to create a basic web application (e.g. react).
• Include a simple form for submitting feedback and a submit button.
Azure Cognitive Services Integration:
• Integrate Azure Text Analytics API for sentiment analysis of submitted feedback.
• Use text to speech services to convert the response into audio. (Bonus- which is adjusted
with the sentiment and emotions)
LLM Integration for Automated Responses:
• Integrate a LLM (e.g. GPT-3 or -4) API to generate responses to the feedback based on its
sentiment.
• Craft concise prompts for the LLM to ensure responses are relevant and appropriate.
Feedback Processing and Display:
• Process the submitted feedback to analyze sentiment.
• Use the sentiment analysis to guide the LLM in generating a contextual response.

Internal

• Display both the sentiment and the LLM-generated response on a simple dashboard.
• Have an option to download the audio file by clicking on a button or play it on UI.

Tips:
• Focus on functionality over design. A clean, minimalistic interface will suffice for the purpose
of this exercise.
• Design the LLM prompts to generate short, straightforward responses.
• Limit the sentiment categories to basic ones like Positive, Negative, and Neutral to simplify
processing.
• Ensure code is well-structured, follows best practices, and is properly documented.
• For frontend some of the frameworks you may use are flask, react, streamlit etc or whichever
technology you prefer.