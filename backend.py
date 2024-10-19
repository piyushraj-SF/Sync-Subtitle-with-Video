import subprocess
import os
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import pysrt

# Function to extract audio using ffmpeg
def extract_audio_from_video(video_path, output_audio_path="audio.wav"):
    command = ['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', output_audio_path]
    subprocess.run(command, check=True)
    return output_audio_path

# Function to process video and subtitle
def process_video_and_subtitles(video_path, subtitle_path):
    # Step 1: Extract audio from the video file
    audio_path = extract_audio_from_video(video_path)

    # Load Whisper model and processor with timestamps enabled
    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")

    # Load the audio file
    audio, rate = librosa.load(audio_path, sr=16000)
    input_features = processor(audio, sampling_rate=16000, return_tensors="pt", padding="longest")

    # Generate transcription
    generated_output = model.generate(input_features.input_features, return_dict_in_generate=True)
    transcription = processor.batch_decode(generated_output.sequences, skip_special_tokens=True)[0]

    # Estimate segment start time
    estimated_first_segment_start_time = 1.0

    # Load the subtitle file
    subs = pysrt.open(subtitle_path)

    # Calculate the offset
    first_sub = subs[0]
    offset = calculate_offset(estimated_first_segment_start_time, first_sub)

    # Apply the offset to all subtitles
    for sub in subs:
        sub.shift(seconds=offset)

    # Save corrected subtitles
    corrected_subtitle_path = 'corrected_subtitles.srt'
    subs.save(corrected_subtitle_path)

    return corrected_subtitle_path

# Function to calculate the offset
def calculate_offset(asr_start_time, first_subtitle):
    subtitle_start_time = first_subtitle.start.seconds + first_subtitle.start.milliseconds / 1000.0
    offset = asr_start_time - subtitle_start_time
    return offset
