# 🎙️ AI Meeting Summarizer

An intelligent meeting assistant that transforms messy audio recordings into structured, professional summaries, action items, and speaker analytics.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://meeting-summarizer-ethiopian.streamlit.app/)

## 🔗 Live Demo
Access the deployed application here: **[AI Meeting Summarizer - Live](https://meeting-summarizer-ethiopian.streamlit.app/)**

---

## 🚀 The Problem It Solves
Taking notes during a meeting is distracting. Reviewing a 60-minute recording later is time-consuming. This tool bridges that gap by:
* **Saving Time:** Get a high-level executive summary in seconds using Llama 3.3.
* **Ensuring Accountability:** Automatically extracts clear **Action Items** so tasks aren't forgotten.
* **Identifying Participation:** Provides **Speaker Analytics** (Pie Charts) to show who contributed most to the discussion.
* **Professional Reporting:** Generates a downloadable PDF report ready to share with the team.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Transcription:** AssemblyAI (utilizing Speaker Diarization)
* **Summarization:** Groq (Llama-3.3-70B-Versatile)
* **Analytics:** Plotly & Pandas
* **Export:** FPDF2

