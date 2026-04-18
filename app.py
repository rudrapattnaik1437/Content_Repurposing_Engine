import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import tempfile

st.set_page_config(page_title="AttentionX", layout="centered")

st.title("🎬 AttentionX - Video to Shorts (Fast Demo)")
st.write("Upload a video and instantly generate short clips with captions!")

# -------- FUNCTIONS -------- #

def cut_fixed_clips(video_path):
    video = VideoFileClip(video_path)
    duration = int(video.duration)

    clips = []
    clip_length = 10  # seconds per clip

    for i in range(0, min(duration, 30), clip_length):
        start = i
        end = min(i + clip_length, duration)

        clip = video.subclip(start, end)
        output = f"clip_{i}.mp4"
        clip.write_videofile(output, codec="libx264", audio_codec="aac")

        clips.append((output, f"Clip from {start}s to {end}s"))

    return clips


def add_caption(video_path, text):
    video = VideoFileClip(video_path)

    caption = TextClip(
        text,
        fontsize=40,
        color='white',
        method='caption',
        size=(video.w * 0.8, None)
    )

    caption = caption.set_position(('center', 'bottom')).set_duration(video.duration)

    final = CompositeVideoClip([video, caption])

    output = "captioned_" + video_path
    final.write_videofile(output, codec="libx264", audio_codec="aac")

    return output


# -------- MAIN -------- #

video_file = st.file_uploader("Upload Video", type=["mp4"])

if video_file:
    st.video(video_file)

    if st.button("🚀 Generate Clips"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(video_file.read())
            video_path = tmp.name

        st.write("⚡ Processing quickly...")

        try:
            clips = cut_fixed_clips(video_path)

            st.subheader("🎉 Generated Clips")

            for clip_path, text in clips:
                captioned = add_caption(clip_path, text)
                st.video(captioned)

        except Exception as e:
            st.error(f"Error: {e}")
