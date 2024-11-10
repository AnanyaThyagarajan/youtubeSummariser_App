import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

summarization_prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in key points
within 500 words. Please provide the summary of the text given here:  """


## getting the transcript data from YouTube videos
def get_youtube_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)

        video_transcript = ""
        for i in transcript_data:
            video_transcript += " " + i["text"]

        return video_transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_summary_with_gemini(video_transcript, summarization_prompt):

    model = genai.GenerativeModel("gemini-pro")
    summary_response = model.generate_content(summarization_prompt + video_transcript)
    return summary_response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_video_url = st.text_input("Enter YouTube Video Link:")

if youtube_video_url:
    video_id = youtube_video_url.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    video_transcript = get_youtube_transcript(youtube_video_url)

    if video_transcript:
        video_summary = generate_summary_with_gemini(video_transcript, summarization_prompt)
        st.markdown("## Detailed Notes:")
        st.write(video_summary)
