#!/usr/bin/env python3
"""
Test script voor Cryptoriez Shorts Helper
Controleert of alle dependencies correct zijn geïnstalleerd
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test of alle benodigde modules kunnen worden geïmporteerd"""
    print("🧪 Testen van imports...")
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError as e:
        print(f"❌ streamlit: {e}")
        return False
    
    try:
        import moviepy
        print("✅ moviepy")
    except ImportError as e:
        print(f"❌ moviepy: {e}")
        return False
    
    try:
        import openai
        print("✅ openai")
    except ImportError as e:
        print(f"❌ openai: {e}")
        return False
    
    try:
        import pydantic
        print("✅ pydantic")
    except ImportError as e:
        print(f"❌ pydantic: {e}")
        return False
    
    try:
        import dotenv
        print("✅ dotenv")
    except ImportError as e:
        print(f"❌ dotenv: {e}")
        return False
    
    return True

def test_ffmpeg():
    """Test of FFmpeg beschikbaar is"""
    print("🎬 Testen van FFmpeg...")
    
    try:
        # Test of FFmpeg command beschikbaar is
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg command beschikbaar")
            return True
        else:
            print("❌ FFmpeg command niet beschikbaar")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg niet geïnstalleerd")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test mislukt: {e}")
        return False

def test_openai_config():
    """Test of OpenAI configuratie correct is"""
    print("🔑 Testen van OpenAI configuratie...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'sk-your-api-key-here':
            print("✅ OpenAI API key gevonden")
            return True
        else:
            print("⚠️  OpenAI API key niet ingesteld of nog default waarde")
            return False
    except Exception as e:
        print(f"❌ OpenAI config test mislukt: {e}")
        return False

def main():
    """Hoofdfunctie voor het uitvoeren van alle tests"""
    print("🚀 Cryptoriez Shorts Helper - Dependency Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test FFmpeg
    ffmpeg_ok = test_ffmpeg()
    
    # Test OpenAI config
    openai_ok = test_openai_config()
    
    print("\n" + "=" * 50)
    
    if all([imports_ok, ffmpeg_ok, openai_ok]):
        print("🎉 Alle tests geslaagd! De app kan worden gestart.")
        return True
    else:
        print("❌ Sommige tests zijn mislukt. Controleer de bovenstaande fouten.")
        print("\n🔧 Mogelijke oplossingen:")
        print("1. Installeer ontbrekende dependencies: pip install -r requirements.txt")
        print("2. Installeer FFmpeg: brew install ffmpeg")
        print("3. Maak .env bestand aan met je OpenAI API key")
        print("4. Gebruik setup.sh voor automatische installatie")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

