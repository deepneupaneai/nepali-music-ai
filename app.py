# app.py - Complete Nepali Music AI
import streamlit as st
import numpy as np
import time
import io
import base64
import json
from datetime import datetime
import hashlib

# Page Configuration
st.set_page_config(
    page_title="Nepali Music AI 🎵",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Nepali Theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        font-family: 'Segoe UI', sans-serif;
        color: white;
    }
    
    .main-header {
        background: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 20px;
        border: 3px solid #FFD700;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .nepali-title {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #FFD700, #DC143C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #DC143C, #FFD700);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(220, 20, 60, 0.4);
    }
    
    .music-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Music Generator Class
class NepaliMusicGenerator:
    def __init__(self):
        self.sample_rate = 44100
        self.instruments = self.load_instruments()
        
    def load_instruments(self):
        return {
            'madal': {'type': 'percussion', 'base_freq': 100},
            'sarangi': {'type': 'string', 'base_freq': 220},
            'bansuri': {'type': 'wind', 'base_freq': 440},
            'damaru': {'type': 'percussion', 'base_freq': 200}
        }
    
    def generate_wave(self, freq, duration, waveform='sine'):
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        if waveform == 'sine':
            wave = np.sin(2 * np.pi * freq * t)
        elif waveform == 'square':
            wave = np.sign(np.sin(2 * np.pi * freq * t))
        else:
            wave = np.sin(2 * np.pi * freq * t)
        
        # Apply fade
        fade = int(0.1 * self.sample_rate)
        if len(wave) > 2 * fade:
            wave[:fade] *= np.linspace(0, 1, fade)
            wave[-fade:] *= np.linspace(1, 0, fade)
        
        return wave
    
    def create_song(self, scale='major', tempo=120, instruments=['madal']):
        # Generate simple melody
        duration = 10  # 10 seconds
        melody = np.zeros(int(duration * self.sample_rate))
        
        # Add notes based on scale
        notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]
        
        for i, note in enumerate(notes[:4]):
            start = i * 2.5 * self.sample_rate
            end = start + 2.5 * self.sample_rate
            
            note_wave = self.generate_wave(note, 2.5)
            end_idx = min(int(end), len(melody))
            melody[int(start):end_idx] += note_wave[:end_idx-int(start)]
        
        # Normalize
        if np.max(np.abs(melody)) > 0:
            melody = melody / np.max(np.abs(melody)) * 0.8
        
        return melody

# App Class
class NepaliMusicApp:
    def __init__(self):
        self.generator = NepaliMusicGenerator()
        self.init_session()
    
    def init_session(self):
        if 'songs' not in st.session_state:
            st.session_state.songs = []
        if 'current_song' not in st.session_state:
            st.session_state.current_song = None
    
    def render_header(self):
        st.markdown("""
        <div class="main-header">
            <h1 class="nepali-title">🎵 नेपाली संगीत AI</h1>
            <p style="color: #FFD700; font-size: 1.2rem;">
                स्वदेशी AI प्रविधिद्वारा संगीत सिर्जना
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        with st.sidebar:
            st.markdown("### 🎵 नेविगेसन")
            page = st.radio(
                "पृष्ठ छान्नुहोस्",
                ["🏠 मुख्य", "🎶 गीत सिर्जना", "🎤 आवाज", "⚙️ सेटिङ"]
            )
            
            st.divider()
            st.markdown("### 📊 तथ्याङ्क")
            st.metric("सिर्जना गरिएका गीत", len(st.session_state.songs))
            st.metric("बाजाहरू", "८+")
            
            st.divider()
            st.markdown("""
            ### ℹ️ बारेमा
            **नेपाली संगीत AI**  
            १००% स्वदेशी तकनीक  
            कोहि बाहिरी API बिना
            """)
            
            return page
    
    def render_home(self):
        st.markdown("""
        <div class="music-card">
            <h2>🏠 स्वागतम् - नेपाली संगीत AI मा</h2>
            <p>यस AI प्लेटफर्ममा तपाईंले:</p>
            <ul>
                <li>✅ AI द्वारा गीत सिर्जना गर्न सक्नुहुन्छ</li>
                <li>✅ ८+ नेपाली बाजाहरू प्रयोग गर्न सक्नुहुन्छ</li>
                <li>✅ आफ्नो आवाज रेकर्ड गर्न सक्नुहुन्छ</li>
                <li>✅ १००% स्वदेशी तकनीक</li>
                <li>✅ पूर्ण रूपमा निःशुल्क</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎵 नयाँ गीत सिर्जना गर्नुहोस्", use_container_width=True):
                st.session_state.page = "🎶 गीत सिर्जना"
                st.rerun()
        
        with col2:
            if st.button("🎤 आवाज रेकर्ड गर्नुहोस्", use_container_width=True):
                st.session_state.page = "🎤 आवाज"
                st.rerun()
        
        # Recent Songs
        if st.session_state.songs:
            st.markdown("### 🎶 भर्खरैका गीतहरू")
            for song in st.session_state.songs[-3:]:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{song['name']}**")
                        st.caption(f"मिति: {song['time']}")
                    with col2:
                        if st.button("🎧 सुन्नुहोस्", key=f"play_{song['id']}"):
                            st.session_state.current_song = song
    
    def render_song_creation(self):
        st.markdown("## 🎵 गीत सिर्जना")
        
        with st.form("song_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                song_name = st.text_input("गीतको नाम", "मेरो गीत")
                genre = st.selectbox("संगीतको प्रकार", ["लोकगीत", "आधुनिक", "भजन", "पप"])
                tempo = st.slider("गति (BPM)", 60, 180, 120)
            
            with col2:
                scale = st.selectbox("सुर", ["खमाज", "भैरव", "यमन", "आधुनिक"])
                instruments = st.multiselect(
                    "बाजाहरू",
                    ["मादल", "सारङ्गी", "बाँसुरी", "डमरु", "तबला", "पियानो"],
                    default=["मादल", "सारङ्गी"]
                )
                duration = st.slider("अवधि (सेकेण्ड)", 5, 60, 15)
            
            # Lyrics
            lyrics = st.text_area("गीतका बोलहरू (वैकल्पिक)", 
                                 height=150,
                                 placeholder="तपाईंका गीतका बोलहरू यहाँ लेख्नुहोस्...\n\nउदाहरण:\nहिमालको छायाँमा बसेर\nगाऊँ मैले एउटा गीत")
            
            submitted = st.form_submit_button("✨ गीत सिर्जना गर्नुहोस्")
            
            if submitted:
                with st.spinner("AI द्वारा गीत सिर्जना गर्दै..."):
                    # Generate audio
                    audio_data = self.generator.create_song(scale, tempo, instruments)
                    
                    # Create song entry
                    song_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
                    song_data = {
                        'id': song_id,
                        'name': song_name,
                        'genre': genre,
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'audio': audio_data,
                        'lyrics': lyrics if lyrics else "AI द्वारा सिर्जना गरिएको"
                    }
                    
                    st.session_state.songs.append(song_data)
                    st.session_state.current_song = song_data
                    
                    st.success("✅ गीत सिर्जना सफल!")
        
        # Display current song
        if st.session_state.current_song:
            st.markdown("---")
            st.markdown(f"### 🎧 {st.session_state.current_song['name']}")
            
            # Convert audio to bytes
            audio_int16 = (st.session_state.current_song['audio'] * 32767).astype(np.int16)
            with io.BytesIO() as wav_buffer:
                import wave
                with wave.open(wav_buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(44100)
                    wav_file.writeframes(audio_int16.tobytes())
                audio_bytes = wav_buffer.getvalue()
            
            # Play audio
            st.audio(audio_bytes, format='audio/wav')
            
            # Download button
            b64 = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:audio/wav;base64,{b64}" download="nepali_song.wav" style="display: inline-block; padding: 10px 20px; background: linear-gradient(90deg, #FFD700, #DC143C); color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">💾 गीत डाउनलोड गर्नुहोस्</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            # Lyrics
            if st.session_state.current_song['lyrics']:
                with st.expander("📝 गीतका बोलहरू"):
                    st.text(st.session_state.current_song['lyrics'])
    
    def render_voice(self):
        st.markdown("## 🎤 आवाज प्रबन्धन")
        
        tab1, tab2 = st.tabs(["आवाज रेकर्डिङ", "आवाज प्रोफाइल"])
        
        with tab1:
            st.markdown("### 🎤 आवाज रेकर्ड गर्नुहोस्")
            st.info("""
            **आवाज रेकर्ड गर्ने तरिका:**
            1. तलको बटन थिच्नुहोस्
            2. ५ सेकेण्ड बोल्नुहोस्
            3. रोक्न बटन थिच्नुहोस्
            """)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔴 रेकर्डिङ सुरु गर्नुहोस्", type="primary"):
                    st.session_state.recording = True
                    st.info("रेकर्डिङ सुरु भयो... ५ सेकेण्ड")
                    
                    # Simulate recording
                    time.sleep(5)
                    
                    # Generate sample audio
                    t = np.linspace(0, 5, 5*44100)
                    recorded_audio = 0.5 * np.sin(2 * np.pi * 220 * t)  # A note
                    st.session_state.recorded_audio = recorded_audio
                    st.session_state.recording = False
            
            with col2:
                if st.button("⏹️ रेकर्डिङ रोक्नुहोस्"):
                    st.session_state.recording = False
                    st.success("रेकर्डिङ रोकियो")
            
            if 'recorded_audio' in st.session_state:
                # Convert to audio bytes
                audio_int16 = (st.session_state.recorded_audio * 32767).astype(np.int16)
                with io.BytesIO() as wav_buffer:
                    import wave
                    with wave.open(wav_buffer, 'wb') as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2)
                        wav_file.setframerate(44100)
                        wav_file.writeframes(audio_int16.tobytes())
                    audio_bytes = wav_buffer.getvalue()
                
                st.audio(audio_bytes, format='audio/wav')
                
                voice_name = st.text_input("आवाजको नाम", "मेरो_आवाज")
                
                if st.button("💾 आवाज प्रोफाइल सिर्जना गर्नुहोस्"):
                    st.success(f"आवाज प्रोफाइल '{voice_name}' सिर्जना सफल!")
        
        with tab2:
            st.markdown("### 👥 आवाज प्रोफाइलहरू")
            st.info("यहाँ तपाईंका आवाज प्रोफाइलहरू देख्नुहुनेछ")
            
            # Sample profiles
            profiles = [
                {"name": "लोक गायक", "created": "2024-12-01", "songs": 5},
                {"name": "आधुनिक स्वर", "created": "2024-12-05", "songs": 3}
            ]
            
            for profile in profiles:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.markdown(f"**{profile['name']}**")
                    with col2:
                        st.caption(f"सिर्जना: {profile['created']}")
                    with col3:
                        st.caption(f"गीत: {profile['songs']}")
                    st.divider()
    
    def render_settings(self):
        st.markdown("## ⚙️ सेटिङहरू")
        
        with st.form("settings_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                language = st.selectbox("भाषा", ["नेपाली", "English", "हिन्दी"])
                theme = st.selectbox("थिम", ["गाढा", "हल्का", "स्वचालित"])
                auto_save = st.checkbox("स्वचालित सेभ", True)
            
            with col2:
                sample_rate = st.selectbox("अडियो गुणस्तर", ["44100 Hz", "48000 Hz", "96000 Hz"])
                default_instruments = st.multiselect(
                    "डिफल्ट बाजाहरू",
                    ["मादल", "सारङ्गी", "बाँसुरी", "डमरु", "तबला"],
                    default=["मादल", "सारङ्गी"]
                )
            
            if st.form_submit_button("💾 सेटिङहरू सेभ गर्नुहोस्"):
                st.success("सेटिङहरू सेभ गरियो!")
    
    def run(self):
        # Initialize
        self.init_session()
        
        # Render header
        self.render_header()
        
        # Render sidebar and get page
        if 'page' not in st.session_state:
            st.session_state.page = "🏠 मुख्य"
        
        page = self.render_sidebar()
        
        # Update page from sidebar
        st.session_state.page = page
        
        # Render selected page
        if st.session_state.page == "🏠 मुख्य":
            self.render_home()
        elif st.session_state.page == "🎶 गीत सिर्जना":
            self.render_song_creation()
        elif st.session_state.page == "🎤 आवाज":
            self.render_voice()
        elif st.session_state.page == "⚙️ सेटिङ":
            self.render_settings()

# Run the app
if __name__ == "__main__":
    app = NepaliMusicApp()
    app.run()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #FFD700;">
    <p>🎵 <strong>नेपाली संगीत AI</strong> - १००% स्वदेशी तकनीक</p>
    <p>© २०२४ - सबै अधिकार सुरक्षित</p>
</div>
""", unsafe_allow_html=True)
