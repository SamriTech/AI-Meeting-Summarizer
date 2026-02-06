import os
import assemblyai as aai
from dotenv import load_dotenv

def transcribe_audio(file_path):
    """
    Transcribes audio using AssemblyAI with Speaker Diarization enabled.
    """
    try:
        if not os.path.exists(file_path):
            return {"text": "", "error": f"File not found: {file_path}"}

        # 1. Configure the transcription to enable Speaker Labels
        config = aai.TranscriptionConfig(
            speaker_labels=True,
            speech_models=["universal-3-pro", "universal"]
        )
        
        # 2. Upload and transcribe
        transcriber = aai.Transcriber()
        print(f"Uploading and transcribing: {file_path}...")
        transcript = transcriber.transcribe(file_path, config=config)

        # 3. Handle potential errors
        if transcript.status == aai.TranscriptStatus.error:
            return {"text": "", "error": transcript.error}

        # 4. Format the output with Speaker tags
        # Utterances represent blocks of speech from specific speakers
        formatted_transcript = ""
        for utterance in transcript.utterances:
            formatted_transcript += f"Speaker {utterance.speaker}: {utterance.text}\n\n"

        return {
            "text": formatted_transcript.strip(),
            "error": None
        }

    except Exception as e:
        return {"text": "", "error": str(e)}

if __name__ == "__main__":
    # Test with a multi-speaker file if possible!
    test_path = "data/sample.wav" 
    if os.path.exists(test_path):
        response = transcribe_audio(test_path)
        if response["error"]:
            print(f"Error: {response['error']}")
        else:
            print(f"\n--- Final Transcription Result ---\n{response['text']}")
    else:
        print("File not found.")