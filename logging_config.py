"""
Logging configuratie voor Cryptoriez Shorts Helper
"""

import logging
import logging.handlers
import os
from pathlib import Path

def setup_logging(log_level=logging.INFO, log_file=None):
    """Setup logging configuratie"""
    
    # Maak logs directory aan als deze niet bestaat
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Basis logging configuratie
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
        ]
    )
    
    # Voeg file handler toe als log_file is opgegeven
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logging.getLogger().addHandler(file_handler)
    
    # Stel specifieke loggers in
    logging.getLogger('streamlit').setLevel(logging.WARNING)
    logging.getLogger('moviepy').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.INFO)
    
    return logging.getLogger(__name__)

def get_logger(name=None):
    """Krijg een logger instance"""
    if name:
        return logging.getLogger(name)
    return logging.getLogger()

# Standaard logging setup
if __name__ == "__main__":
    # Test logging
    logger = setup_logging(log_file="logs/app.log")
    logger.info("Logging setup voltooid!")
    logger.warning("Dit is een test warning")
    logger.error("Dit is een test error")
