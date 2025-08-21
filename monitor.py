#!/usr/bin/env python3
"""
Monitoring script voor Cryptoriez Shorts Helper
Controleert de status van de applicatie en dependencies
"""

import os
import time
import requests
import subprocess
from datetime import datetime

def check_openai_api():
    """Controleer of OpenAI API bereikbaar is"""
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            return False, "Geen API key gevonden"
        
        client = OpenAI(api_key=api_key)
        # Test met een eenvoudige request
        response = client.models.list()
        return True, "API bereikbaar"
    except Exception as e:
        return False, f"API fout: {str(e)}"

def check_ffmpeg():
    """Controleer of FFmpeg beschikbaar is"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True, "FFmpeg beschikbaar"
        else:
            return False, "FFmpeg niet beschikbaar"
    except Exception as e:
        return False, f"FFmpeg fout: {str(e)}"

def check_streamlit_app():
    """Controleer of de Streamlit app draait"""
    try:
        response = requests.get('http://localhost:8501/_stcore/health', timeout=5)
        if response.status_code == 200:
            return True, "App draait op poort 8501"
        else:
            return False, f"App status: {response.status_code}"
    except requests.exceptions.RequestException:
        return False, "App niet bereikbaar"

def main():
    """Hoofdfunctie voor monitoring"""
    print("🔍 Cryptoriez Shorts Helper - Status Monitoring")
    print("=" * 50)
    print(f"Tijd: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check OpenAI API
    print("🔑 OpenAI API:")
    api_ok, api_msg = check_openai_api()
    status_icon = "✅" if api_ok else "❌"
    print(f"   {status_icon} {api_msg}")
    
    # Check FFmpeg
    print("🎬 FFmpeg:")
    ffmpeg_ok, ffmpeg_msg = check_ffmpeg()
    status_icon = "✅" if ffmpeg_ok else "❌"
    print(f"   {status_icon} {ffmpeg_msg}")
    
    # Check Streamlit app
    print("🌐 Streamlit App:")
    app_ok, app_msg = check_streamlit_app()
    status_icon = "✅" if app_ok else "❌"
    print(f"   {status_icon} {app_msg}")
    
    print()
    print("=" * 50)
    
    # Overall status
    all_ok = api_ok and ffmpeg_ok and app_ok
    if all_ok:
        print("🎉 Alle systemen werken correct!")
    else:
        print("⚠️  Er zijn problemen gedetecteerd.")
        print("   Gebruik ./setup.sh om problemen op te lossen.")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
