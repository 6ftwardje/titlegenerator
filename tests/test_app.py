"""
Tests voor Cryptoriez Shorts Helper
"""

import pytest
import sys
from pathlib import Path

# Voeg project root toe aan Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import GenerationRequest, build_user_prompt, SYSTEM_PROMPT

class TestGenerationRequest:
    """Tests voor GenerationRequest model"""
    
    def test_valid_request(self):
        """Test een geldige request"""
        req = GenerationRequest(
            transcript="Test transcript",
            clickbait_level=5,
            allow_emojis=True,
            include_hashtags=True
        )
        
        assert req.transcript == "Test transcript"
        assert req.clickbait_level == 5
        assert req.allow_emojis is True
        assert req.include_hashtags is True
        assert req.language == "nl"  # default waarde
    
    def test_clickbait_level_validation(self):
        """Test clickbait level validatie"""
        # Test ondergrens
        with pytest.raises(ValueError):
            GenerationRequest(
                transcript="Test",
                clickbait_level=-1
            )
        
        # Test bovengrens
        with pytest.raises(ValueError):
            GenerationRequest(
                transcript="Test",
                clickbait_level=11
            )
    
    def test_default_values(self):
        """Test default waarden"""
        req = GenerationRequest(transcript="Test")
        
        assert req.language == "nl"
        assert req.clickbait_level == 5
        assert req.allow_emojis is True
        assert req.include_hashtags is True
        assert req.platforms == ["Alle"]

class TestPromptBuilding:
    """Tests voor prompt building"""
    
    def test_basic_prompt(self):
        """Test basis prompt building"""
        req = GenerationRequest(
            transcript="Test transcript",
            clickbait_level=7,
            allow_emojis=True,
            include_hashtags=True
        )
        
        prompt = build_user_prompt(req)
        
        assert "Test transcript" in prompt
        assert "Clickbait-intensiteit: 7 op 10" in prompt
        assert "Je mag emoji's gebruiken" in prompt
        assert "Sluit af met 5–10 relevante hashtags" in prompt
    
    def test_no_emojis_prompt(self):
        """Test prompt zonder emoji's"""
        req = GenerationRequest(
            transcript="Test transcript",
            allow_emojis=False
        )
        
        prompt = build_user_prompt(req)
        
        assert "Gebruik geen emoji's" in prompt
    
    def test_no_hashtags_prompt(self):
        """Test prompt zonder hashtags"""
        req = GenerationRequest(
            transcript="Test transcript",
            include_hashtags=False
        )
        
        prompt = build_user_prompt(req)
        
        assert "Voeg géén hashtags toe" in prompt

class TestSystemPrompt:
    """Tests voor system prompt"""
    
    def test_system_prompt_content(self):
        """Test of system prompt de juiste content bevat"""
        assert "Nederlandstalige content-editor" in SYSTEM_PROMPT
        assert "Cryptoriez" in SYSTEM_PROMPT
        assert "trading, crypto & forex" in SYSTEM_PROMPT
        assert "JSON" in SYSTEM_PROMPT

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__])
