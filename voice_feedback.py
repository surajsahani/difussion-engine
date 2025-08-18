#!/usr/bin/env python3
"""
Voice Feedback Module for AI Prompt Game
Provides text-to-speech functionality for game feedback
"""

import re
import threading
from typing import Optional, List


class VoiceFeedback:
    """Text-to-speech feedback system for the game"""
    
    def __init__(self, enabled: bool = True, rate: int = 150, volume: float = 0.9):
        """
        Initialize voice feedback system
        
        Args:
            enabled: Whether voice feedback is enabled
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        self.enabled = enabled
        self.rate = rate
        self.volume = volume
        self.engine = None
        
        if self.enabled:
            self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the TTS engine"""
        try:
            import pyttsx3
            
            # Try different initialization methods
            try:
                self.engine = pyttsx3.init('espeak')  # Try espeak driver specifically
            except:
                try:
                    self.engine = pyttsx3.init()  # Try default driver
                except:
                    print("⚠️  Could not initialize any TTS driver")
                    self.enabled = False
                    self.engine = None
                    return
            
            if self.engine:
                # Configure basic properties only
                try:
                    self.engine.setProperty('rate', self.rate)
                    self.engine.setProperty('volume', self.volume)
                except Exception as prop_error:
                    print(f"⚠️  Could not set voice properties: {prop_error}")
                
                print("🔊 Voice feedback initialized successfully!")
            else:
                self.enabled = False
            
        except ImportError:
            print("⚠️  pyttsx3 not available, voice feedback disabled")
            self.enabled = False
            self.engine = None
        except Exception as e:
            print(f"⚠️  Voice feedback initialization failed: {e}")
            print("⚠️  Continuing with text-only feedback")
            self.enabled = False
            self.engine = None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Clean text for better speech synthesis
        
        Args:
            text: Original text with emojis and formatting
            
        Returns:
            Cleaned text suitable for TTS
        """
        # Remove emojis and special characters
        text = re.sub(r'[🎉🌟👍🤔💡💪🏆📊📝🔄💬🎯⭐]+', '', text)
        
        # Replace common abbreviations and symbols
        replacements = {
            '&': 'and',
            '@': 'at',
            '#': 'number',
            '%': 'percent',
            '...': ' pause ',
            '!': '.',
            '!!': '.',
            '!!!': '.',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Clean up extra spaces
        text = ' '.join(text.split())
        
        # Ensure proper sentence ending
        if text and not text.endswith('.'):
            text += '.'
        
        return text.strip()
    
    def speak(self, text: str, async_speech: bool = True):
        """
        Speak the given text
        
        Args:
            text: Text to speak
            async_speech: Whether to speak asynchronously (non-blocking)
        """
        if not self.enabled or not self.engine or not text:
            return
        
        # Clean text for speech
        clean_text = self._clean_text_for_speech(text)
        
        if not clean_text:
            return
        
        def _speak():
            try:
                self.engine.say(clean_text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"⚠️  Voice feedback error: {e}")
        
        if async_speech:
            # Speak in a separate thread to avoid blocking the game
            speech_thread = threading.Thread(target=_speak, daemon=True)
            speech_thread.start()
        else:
            _speak()
    
    def speak_feedback(self, feedback: str, hints: Optional[List[str]] = None, 
                      speak_hints: bool = False):
        """
        Speak game feedback and optionally hints
        
        Args:
            feedback: Main feedback message
            hints: List of hint messages
            speak_hints: Whether to speak hints as well
        """
        if not self.enabled:
            return
        
        # Speak main feedback
        self.speak(feedback)
        
        # Optionally speak hints
        if speak_hints and hints:
            for hint in hints:
                # Small delay between hints
                threading.Timer(2.0, lambda h=hint: self.speak(h)).start()
    
    def speak_score(self, score: float, is_best: bool = False):
        """
        Speak score information
        
        Args:
            score: Similarity score (0.0 to 1.0)
            is_best: Whether this is a new best score
        """
        if not self.enabled:
            return
        
        score_text = f"Similarity score: {score:.1%}"
        
        if is_best:
            score_text = f"New best score! {score_text}"
        
        self.speak(score_text)
    
    def set_enabled(self, enabled: bool):
        """Enable or disable voice feedback"""
        self.enabled = enabled and self.engine is not None
    
    def is_available(self) -> bool:
        """Check if voice feedback is available"""
        return self.engine is not None


# Global instance for easy access
_voice_feedback = None

def get_voice_feedback(enabled: bool = True) -> VoiceFeedback:
    """Get or create the global voice feedback instance"""
    global _voice_feedback
    if _voice_feedback is None:
        _voice_feedback = VoiceFeedback(enabled=enabled)
    return _voice_feedback

def speak_feedback(feedback: str, hints: Optional[List[str]] = None, 
                  enabled: bool = True, speak_hints: bool = False):
    """
    Convenience function to speak feedback
    
    Args:
        feedback: Main feedback message
        hints: Optional list of hints
        enabled: Whether voice feedback is enabled
        speak_hints: Whether to speak hints as well
    """
    if enabled:
        voice = get_voice_feedback(enabled=True)
        voice.speak_feedback(feedback, hints, speak_hints)

def speak_score(score: float, is_best: bool = False, enabled: bool = True):
    """
    Convenience function to speak score
    
    Args:
        score: Similarity score (0.0 to 1.0)
        is_best: Whether this is a new best score  
        enabled: Whether voice feedback is enabled
    """
    if enabled:
        voice = get_voice_feedback(enabled=True)
        voice.speak_score(score, is_best)