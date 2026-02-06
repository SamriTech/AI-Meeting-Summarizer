import streamlit as st
import os
import pandas as pd
import plotly.express as px
from utils.transcriber import transcribe_audio
from utils.summarizer import summarize_transcript, extract_action_items
from utils.pdf_generator import generate_pdf

st.set_page_config(page_title="AI Meeting Summarizer", layout="wide")
st.title("🎙️ AI Meeting Summarizer")

# 1. Initialize session state for all our features
if 'transcript' not in st.session_state: st.session_state['transcript'] = ""
if 'summary' not in st.session_state: st.session_state['summary'] = ""
if 'action_items' not in st.session_state: st.session_state['action_items'] = []

# Sidebar for additional info
with st.sidebar:
    st.header("Settings & Info")
    st.info("This version uses AssemblyAI for Speaker Labels and Groq/Gemini for Summarization.")

uploaded_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "aac", "m4a"])

if uploaded_file:
    # Ensure data directory exists
    if not os.path.exists("data"): os.makedirs("data")
    
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("🚀 Transcribe & Summarize"):
        with st.spinner("Step 1: Identifying Speakers & Transcribing..."):
            result = transcribe_audio(file_path)
            
            if not result["error"]:
                st.session_state['transcript'] = result["text"]
                
                with st.spinner("Step 2: Generating Summary & Tasks..."):
                    # Generate the summary
                    summary = summarize_transcript(result["text"])
                    st.session_state['summary'] = summary
                    
                    # Parse the action items for the checklist
                    st.session_state['action_items'] = extract_action_items(summary)
            else:
                st.error(f"Transcription Error: {result['error']}")

# --- Display Results Section ---
if st.session_state['transcript']:
    st.divider()
    col1, col2 = st.columns([1, 1]) # Equal width columns

    with col1:
        # --- New Feature: Talk Time Analytics ---
        st.write("---")
        st.subheader("📊 Speaker Analytics")
        
        # Simple logic to count words per speaker
        lines = st.session_state['transcript'].split('\n\n')
        speaker_counts = {}
        for line in lines:
            if "Speaker " in line:
                parts = line.split(": ", 1)
                speaker = parts[0]
                words = len(parts[1].split()) if len(parts) > 1 else 0
                speaker_counts[speaker] = speaker_counts.get(speaker, 0) + words
        
        if speaker_counts:
            df = pd.DataFrame(list(speaker_counts.items()), columns=['Speaker', 'Word Count'])
            fig = px.pie(df, values='Word Count', names='Speaker', hole=0.4,
                        color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("👥 Speaker-Labeled Transcript")
            # Using a text area with height makes it scrollable
            st.text_area("Full Conversation", st.session_state['transcript'], height=500)

    with col2:
        st.subheader("🧠 Executive Summary")
        st.markdown(st.session_state['summary'])
        
        # 2. Interactive Checklist Feature
        if st.session_state['action_items']:
            st.markdown("### ✅ Interactive Action Items")
            st.write("Track your meeting follow-ups here:")
            for i, item in enumerate(st.session_state['action_items']):
                # Creates a live checkbox for every item found by the AI
                st.checkbox(item, key=f"task_{i}")
        
        st.write("---")
        # 3. PDF Export
        if st.button("📄 Prepare PDF for Download"):
            pdf_path = generate_pdf(st.session_state['summary'])
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download Final Report", f, file_name="Meeting_Summary.pdf")

