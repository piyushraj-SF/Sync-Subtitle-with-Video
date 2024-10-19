import streamlit as st
import os
from backend import process_video_and_subtitles

def main():
    # Title with center alignment
    st.markdown("<h1 style='text-align: center;'>COOK D SUBTITLE</h1>", unsafe_allow_html=True)
    
    # Subtitle with center alignment and smaller size
    st.markdown("<h3 style='text-align: center; font-size: 20px;'>Sync Subtitles Effortlessly :)</h3>", unsafe_allow_html=True)

    # Upload video and subtitle files
    video_file = st.file_uploader("Upload Video File", type=["mp4", "avi", "mov"])
    subtitle_file = st.file_uploader("Upload Subtitle File", type=["srt"])

    if video_file and subtitle_file:
        # Save uploaded files temporarily
        with open(video_file.name, "wb") as f:
            f.write(video_file.getbuffer())
        with open(subtitle_file.name, "wb") as f:
            f.write(subtitle_file.getbuffer())

        # Display the video in the interface
        st.video(video_file)

        # Process the files when user clicks 'Synchronize'
        if st.button("Synchronize Subtitles"):
            result = process_video_and_subtitles(video_file.name, subtitle_file.name)

            # Display the result and download option
            st.success("Subtitles synchronized!")
            st.write("Download the synchronized subtitles:")
            with open(result, "rb") as file:
                st.download_button("Download Corrected Subtitles", file, file_name="corrected_subtitles.srt", mime="text/plain")

            # Show the synchronized subtitles (example with smaller font size)
            st.markdown(f"<h3 style='text-align: center;'>Corrected Subtitles:</h3>", unsafe_allow_html=True)
            with open(result, 'r') as subtitle:
                st.markdown(f"<pre style='font-size: 14px;'>{subtitle.read()}</pre>", unsafe_allow_html=True)

    # Footer with "Made with Heart by DCooks"
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; font-size: 16px;'>Made with ❤️ by <b>DCooks</b> (Piyush, Rajeev, Jay)</p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
