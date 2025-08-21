# 🎬 Cryptoriez Shorts Helper

Een lokale Streamlit applicatie voor het automatisch genereren van titels en beschrijvingen voor crypto/forex shorts en reels.

## ✨ Features

- **Video Upload**: Ondersteunt .mp4, .mov, .m4v bestanden
- **Automatische Transcriptie**: Gebruikt OpenAI Whisper API voor audio naar tekst
- **AI-Generated Content**: GPT-4 voor titels en beschrijvingen
- **Clickbait Controle**: Slider van 0-10 voor clickbait intensiteit
- **Platform Optimalisatie**: YouTube Shorts, Instagram Reels, TikTok
- **Hashtag Generatie**: Automatische relevante hashtags
- **Taal Ondersteuning**: Nederlands en Engels
- **Download Functies**: Exporteer resultaten als .txt bestanden

## 🚀 Snelle Start

### 1. Vereisten

- Python 3.10+
- FFmpeg (voor audio extractie)
- OpenAI API key

### 2. FFmpeg Installatie (macOS)

```bash
brew install ffmpeg
```

### 3. Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Kopieer `env.example` naar `.env` en voeg je OpenAI API key toe:

```bash
cp env.example .env
```

Bewerk `.env`:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 5. Start de App

```bash
streamlit run app.py
```

De app opent automatisch in je browser op `http://localhost:8501`

## 📱 Gebruik

### Stap 1: Upload
- Sleep je short/reel bestand naar de upload zone
- Ondersteunde formaten: .mp4, .mov, .m4v

### Stap 2: Voorkeuren Instellen
- **Clickbait Level**: 0 (informatief) tot 10 (zeer agressief)
- **Platforms**: Selecteer je target platforms
- **Taal**: Nederlands of Engels
- **Emoji's**: Aan/uit voor titels en beschrijvingen
- **Hashtags**: Automatische generatie + extra custom hashtags

### Stap 3: Transcriptie
- Klik "Transcribe & Genereer"
- De app extraheert audio en genereert een transcript
- Bewerk het transcript indien nodig

### Stap 4: Content Generatie
- Klik "Genereer Titel & Beschrijving"
- AI genereert een titel, beschrijving en hashtags
- Download resultaten of kopieer naar klembord

## 🎯 Content Stijl

### Titels
- **Clickbait 0-2**: Informatief, neutraal
- **Clickbait 3-5**: Prikkelend, concreet
- **Clickbait 6-8**: Urgent, sterk hook
- **Clickbait 9-10**: Zeer agressief (maar geloofwaardig)

### Beschrijvingen
- 2-5 kerninzichten
- Markt impact uitleg
- Call-to-action
- Eenvoudige taal (geen vakjargon)

## 🔧 Technische Details

### Dependencies
- **Streamlit**: Web UI framework
- **MoviePy**: Video processing en audio extractie
- **OpenAI**: Whisper (transcriptie) + GPT-4 (content generatie)
- **Pydantic**: Data validatie
- **FFmpeg**: Audio/video processing (via MoviePy)

### API Gebruik
- **Whisper-1**: Audio transcriptie
- **GPT-4o-mini**: Titel en beschrijving generatie

### Bestandsverwerking
- Tijdelijke bestanden worden automatisch opgeruimd
- Ondersteunt grote video bestanden
- Audio extractie naar WAV formaat

## 🚀 Uitbreidingen

### Mogelijke Verbeteringen
- Batch processing voor meerdere video's
- Custom templates per platform
- A/B testing voor titels
- Analytics en performance tracking
- Desktop app met Electron
- Web deployment

### API Integraties
- YouTube Data API voor uploads
- Instagram Basic Display API
- TikTok Business API
- Social media scheduling tools

## 🐛 Troubleshooting

### Veelvoorkomende Problemen

**FFmpeg niet gevonden**
```bash
brew install ffmpeg
# Of download van https://ffmpeg.org/
```

**OpenAI API Error**
- Controleer je API key in `.env`
- Zorg dat je credits hebt op je OpenAI account
- Controleer je internetverbinding

**Video Upload Fout**
- Controleer bestandsformaat (.mp4, .mov, .m4v)
- Zorg dat het bestand niet te groot is
- Probeer een andere browser

**Memory Issues**
- Sluit andere applicaties
- Gebruik kleinere video bestanden
- Herstart de Streamlit app

## 📄 Licentie

Dit project is voor persoonlijk gebruik. OpenAI API gebruik valt onder hun terms of service.

## 🤝 Support

Voor vragen of problemen:
1. Controleer de troubleshooting sectie
2. Bekijk de console output voor error messages
3. Zorg dat alle dependencies correct geïnstalleerd zijn

---

**Gemaakt voor Cryptoriez** 🚀
*Automatiseer je social media content workflow*

