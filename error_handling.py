"""
Error handling configuratie voor Cryptoriez Shorts Helper
"""

import traceback
import logging
from typing import Optional, Any, Callable
from functools import wraps

logger = logging.getLogger(__name__)

class CryptoriezError(Exception):
    """Basis exception class voor Cryptoriez applicatie"""
    pass

class VideoProcessingError(CryptoriezError):
    """Exception voor video processing fouten"""
    pass

class TranscriptionError(CryptoriezError):
    """Exception voor transcriptie fouten"""
    pass

class ContentGenerationError(CryptoriezError):
    """Exception voor content generatie fouten"""
    pass

def handle_errors(func: Callable) -> Callable:
    """Decorator voor error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except VideoProcessingError as e:
            logger.error(f"Video processing fout: {e}")
            raise
        except TranscriptionError as e:
            logger.error(f"Transcriptie fout: {e}")
            raise
        except ContentGenerationError as e:
            logger.error(f"Content generatie fout: {e}")
            raise
        except Exception as e:
            logger.error(f"Onverwachte fout in {func.__name__}: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise CryptoriezError(f"Onverwachte fout: {e}")
    return wrapper

def safe_execute(func: Callable, *args, **kwargs) -> tuple[bool, Any, Optional[str]]:
    """
    Voer een functie veilig uit en retourneer (success, result, error_message)
    """
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except Exception as e:
        error_msg = f"Fout in {func.__name__}: {str(e)}"
        logger.error(error_msg)
        return False, None, error_msg

def format_error_message(error: Exception) -> str:
    """Format een error message voor gebruikers"""
    if isinstance(error, VideoProcessingError):
        return f"Video verwerking fout: {error}"
    elif isinstance(error, TranscriptionError):
        return f"Transcriptie fout: {error}"
    elif isinstance(error, ContentGenerationError):
        return f"Content generatie fout: {error}"
    else:
        return f"Er is een fout opgetreden: {error}"

# Error codes
ERROR_CODES = {
    'VIDEO_UPLOAD_FAILED': 'VID001',
    'VIDEO_PROCESSING_FAILED': 'VID002',
    'AUDIO_EXTRACTION_FAILED': 'AUD001',
    'TRANSCRIPTION_FAILED': 'TRN001',
    'CONTENT_GENERATION_FAILED': 'GEN001',
    'API_ERROR': 'API001',
    'FILE_ERROR': 'FIL001',
}

def get_error_code(error_type: str) -> str:
    """Krijg error code voor een error type"""
    return ERROR_CODES.get(error_type, 'UNK001')
