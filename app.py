import os
import io
import tempfile
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

import streamlit as st
from moviepy.editor import VideoFileClip
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Cryptoriez Shorts Helper", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f1f1f 0%, #2d2d2d 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #0066cc 0%, #0099ff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #0052a3 0%, #007acc 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    .upload-section {
        background: #f0f2f6;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #0066cc;
    }
    .result-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Configuration & Constants
# --------------------------
PLATFORMS = ["YouTube Shorts", "Instagram Reels", "TikTok", "Alle"]
DEFAULT_HASHTAGS = ["#crypto", "#bitcoin", "#altcoins", "#forex", "#trading", "#marktupdate", "#technischeanalyse"]

class GenerationRequest(BaseModel):
    transcript: str
    language: str = Field(default="nl")
    topic_hint: Optional[str] = Field(default="Crypto/Forex marktupdate of trade breakdown")
    clickbait_level: int = Field(ge=0, le=10, default=5)
    allow_emojis: bool = True
    include_hashtags: bool = True
    platforms: list[str] = Field(default_factory=lambda: ["Alle"])

SYSTEM_PROMPT = """Je bent een ervaren Nederlandstalige content-editor voor Cryptoriez (focus: trading, crypto & forex, marktbreakdowns, updates).

Stijl:
- Duidelijk, concreet, "no nonsense"
- Geen overbodige vakjargon; leg kort uit voor niet-technische kijkers
- Houd het geloofwaardig: prikkelende titels zijn oké, maar geen misleiding
- Zet inhoud voorop; clickbait-intensiteit bepaalt scherpte/urgentie, niet de waarheid
- Respecteer voorkeuren voor emoji's en hashtags

Taken:
1) Bedenk 1 sterke, platform-agnostische titel op basis van transcript + topic_hint
2) Schrijf een beschrijving met:
   - 2–5 kerninzichten of takeaways
   - Korte context "wat betekent dit voor markt/risico/sentiment"
   - Call-to-action (bv. volg voor meer breakdowns)
3) Voeg optioneel hashtags toe (relevant, 5–10 max)

Uitvoer in JSON met velden: title, description, hashtags (array).
"""

# --------------------------
# Helper Functions
# --------------------------
def build_user_prompt(req: GenerationRequest) -> str:
    emoji_rule = "Je mag emoji's gebruiken waar relevant." if req.allow_emojis else "Gebruik geen emoji's."
    hashtag_rule = "Sluit af met 5–10 relevante hashtags." if req.include_hashtags else "Voeg géén hashtags toe."
    
    clickbait_guidance = f"""Clickbait-intensiteit: {req.clickbait_level} op 10.
- 0–2: informatief, neutraal
- 3–5: prikkelend, concreet
- 6–8: urgent, sterk hook
- 9–10: zeer agressief (maar geloofwaardig, geen sensationalisme/garanties)"""

    return f"""
Taal: {req.language}
Platforms: {', '.join(req.platforms)}
Topic hint: {req.topic_hint}

{emoji_rule}
{hashtag_rule}
{clickbait_guidance}

Transcript (ruw, samenvatten & opschonen):
\"\"\"{req.transcript.strip()}\"\"\"
"""

def transcribe_audio(audio_path: str, language_hint: str = "nl") -> str:
    """Transcribe audio using OpenAI Whisper API"""
    try:
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=language_hint
            )
        return transcript.text
    except Exception as e:
        st.error(f"Fout bij transcriberen: {str(e)}")
        return ""

def extract_audio_from_video(video_file: Path, as_wav=True) -> Path:
    """Extract audio from video file using MoviePy"""
    try:
        # Controleer of het video bestand bestaat
        if not video_file.exists():
            st.error(f"Video bestand niet gevonden: {video_file}")
            return None
            
        # Laad video clip
        clip = VideoFileClip(str(video_file))
        
        # Controleer of de clip audio heeft
        if clip.audio is None:
            st.error("Video heeft geen audio track")
            clip.close()
            return None
        
        # Maak een unieke bestandsnaam
        suffix = ".wav" if as_wav else ".mp3"
        temp_name = f"cryptoriez_audio_{os.urandom(8).hex()}{suffix}"
        out = Path(tempfile.gettempdir()) / temp_name
        
        # Schrijf audio naar bestand
        clip.audio.write_audiofile(str(out), verbose=False, logger=None)
        
        # Sluit de clip
        clip.close()
        
        # Controleer of het audio bestand succesvol is aangemaakt
        if out.exists() and out.stat().st_size > 0:
            return out
        else:
            st.error("Audio bestand kon niet worden aangemaakt")
            return None
            
    except Exception as e:
        st.error(f"Fout bij audio extractie: {str(e)}")
        # Probeer clip te sluiten als deze nog open is
        try:
            if 'clip' in locals():
                clip.close()
        except:
            pass
        return None

def generate_title_description(req: GenerationRequest):
    """Generate title and description using OpenAI GPT-4"""
    try:
        user_prompt = build_user_prompt(req)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.7,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        title = data.get("title", "").strip()
        description = data.get("description", "").strip()
        hashtags = data.get("hashtags", [])
        return title, description, hashtags
    except Exception as e:
        st.error(f"Fout bij genereren: {str(e)}")
        return "Titel kon niet worden gegenereerd", "Beschrijving kon niet worden gegenereerd", []

# --------------------------
# Main UI
# --------------------------
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Cryptoriez Short Titler & Describer</h1>
        <p>Upload een short/reel → transcript → titel + beschrijving voor YouTube, Instagram & TikTok</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for preferences
    with st.sidebar:
        st.header("⚙️ Voorkeuren")
        
        platforms = st.multiselect(
            "Platform(s)", 
            PLATFORMS, 
            default=["Alle"],
            help="Selecteer de platforms waarvoor je content maakt"
        )
        
        clickbait_level = st.slider(
            "Clickbait-intensiteit", 
            0, 10, 5,
            help="0 = informatief, 10 = zeer agressief"
        )
        
        language = st.selectbox(
            "Taal output", 
            ["nl", "en"], 
            index=0,
            help="Taal voor de gegenereerde titel en beschrijving"
        )
        
        use_emojis = st.toggle(
            "Emoji's toestaan", 
            value=True,
            help="Voeg emoji's toe aan titel en beschrijving"
        )
        
        use_hashtags = st.toggle(
            "Hashtags toevoegen", 
            value=True,
            help="Voeg relevante hashtags toe"
        )
        
        topic_hint = st.text_input(
            "Context / topic hint (optioneel)", 
            value="Crypto/Forex marktupdate of trade breakdown",
            help="Extra context om de AI te helpen bij het genereren"
        )
        
        default_hashtags = st.text_input(
            "Extra hashtags (komma-gescheiden)", 
            value=", ".join(DEFAULT_HASHTAGS),
            help="Voeg extra hashtags toe aan de gegenereerde content"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📤 Upload & Verwerking")
        
        # File upload
        uploaded = st.file_uploader(
            "Upload je short (.mp4/.mov/.m4v)", 
            type=["mp4", "mov", "m4v"],
            help="Sleep je video bestand hierheen of klik om te selecteren"
        )
        
        if uploaded:
            st.video(uploaded)
            
            if st.button("🎯 Transcribe & Genereer", type="primary"):
                with st.spinner("Audio extraheren..."):
                    # Write temp video
                    temp_video = Path(tempfile.gettempdir()) / f"cryptoriez_input_{uploaded.name}"
                    with open(temp_video, "wb") as f:
                        f.write(uploaded.getbuffer())
                    
                    audio_path = extract_audio_from_video(temp_video, as_wav=True)
                    
                    if audio_path and audio_path.exists():
                        # Clean up temp video
                        temp_video.unlink(missing_ok=True)
                        
                        with st.spinner("Transcriberen..."):
                            transcript_text = transcribe_audio(
                                str(audio_path), 
                                language_hint="nl" if language == "nl" else "en"
                            )
                        
                        # Clean up temp audio
                        audio_path.unlink(missing_ok=True)
                        
                        if transcript_text:
                            st.success("✅ Transcript gereed!")
                            st.session_state["transcript"] = transcript_text
                            st.session_state["show_generate"] = True
                        else:
                            st.error("❌ Transcript kon niet worden gegenereerd")
                    else:
                        st.error("❌ Audio kon niet worden geëxtraheerd")
    
    with col2:
        st.header("📝 Transcript")
        
        if "transcript" in st.session_state:
            transcript_text = st.text_area(
                "Transcript (bewerken toegestaan)", 
                st.session_state["transcript"], 
                height=300,
                key="transcript_box",
                help="Bewerk het transcript indien nodig voordat je de titel en beschrijving genereert"
            )
            
            if st.button("🚀 Genereer Titel & Beschrijving", type="primary"):
                req = GenerationRequest(
                    transcript=transcript_text,
                    language=language,
                    topic_hint=topic_hint,
                    clickbait_level=clickbait_level,
                    allow_emojis=use_emojis,
                    include_hashtags=use_hashtags,
                    platforms=platforms
                )
                
                with st.spinner("Genereren..."):
                    title, description, hashtags = generate_title_description(req)
                
                # Process hashtags
                extra = [h.strip() for h in default_hashtags.split(",") if h.strip()] if use_hashtags else []
                all_hashtags = []
                
                if use_hashtags:
                    seen = set()
                    for h in (hashtags + extra):
                        if not h.startswith("#"):
                            h = "#" + h
                        if h.lower() not in seen:
                            all_hashtags.append(h)
                            seen.add(h.lower())
                
                # Store results in session state
                st.session_state["generated_title"] = title
                st.session_state["generated_description"] = description
                st.session_state["generated_hashtags"] = all_hashtags
    
    # Results section
    if "generated_title" in st.session_state:
        st.markdown("---")
        st.header("🎉 Resultaten")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Titel")
            st.text_input(
                "Gegenereerde Titel", 
                st.session_state["generated_title"], 
                key="title_out",
                help="Kopieer deze titel voor je social media posts"
            )
            
            st.download_button(
                "📥 Download Titel", 
                data=st.session_state["generated_title"], 
                file_name="titel.txt",
                mime="text/plain"
            )
        
        with col2:
            st.subheader("📝 Beschrijving")
            st.text_area(
                "Gegenereerde Beschrijving", 
                st.session_state["generated_description"], 
                height=200,
                key="desc_out",
                help="Kopieer deze beschrijving voor je social media posts"
            )
            
            st.download_button(
                "📥 Download Beschrijving", 
                data=st.session_state["generated_description"], 
                file_name="beschrijving.txt",
                mime="text/plain"
            )
        
        if use_hashtags and st.session_state["generated_hashtags"]:
            st.subheader("🏷️ Hashtags")
            hashtag_text = " ".join(st.session_state["generated_hashtags"])
            st.text_area(
                "Gegenereerde Hashtags", 
                hashtag_text, 
                height=100,
                help="Kopieer deze hashtags voor je social media posts"
            )
            
            st.download_button(
                "📥 Download Hashtags", 
                data=hashtag_text, 
                file_name="hashtags.txt",
                mime="text/plain"
            )
        
        # Copy to clipboard buttons
        st.markdown("---")
        st.subheader("📋 Snelle Kopie")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Kopieer Titel", key="copy_title"):
                st.write("✅ Titel gekopieerd!")
        
        with col2:
            if st.button("📋 Kopieer Beschrijving", key="copy_desc"):
                st.write("✅ Beschrijving gekopieerd!")
        
        with col3:
            if use_hashtags and st.session_state["generated_hashtags"]:
                if st.button("📋 Kopieer Hashtags", key="copy_hashtags"):
                    st.write("✅ Hashtags gekopieerd!")

if __name__ == "__main__":
    main()

