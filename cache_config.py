"""
Caching configuratie voor Cryptoriez Shorts Helper
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime, timedelta

class CacheManager:
    """Cache manager voor de applicatie"""
    
    def __init__(self, cache_dir: str = "cache", max_age_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.max_age_hours = max_age_hours
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, data: str) -> str:
        """Genereer een cache key voor data"""
        return hashlib.md5(data.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Krijg het cache bestand pad"""
        return self.cache_dir / f"{key}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """Haal data op uit cache"""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check of cache nog geldig is
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time > timedelta(hours=self.max_age_hours):
                # Cache is verlopen, verwijder bestand
                cache_path.unlink()
                return None
            
            return cache_data['data']
        
        except Exception:
            # Als er iets mis gaat, verwijder het cache bestand
            if cache_path.exists():
                cache_path.unlink()
            return None
    
    def set(self, key: str, data: Any) -> None:
        """Sla data op in cache"""
        cache_path = self._get_cache_path(key)
        
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
        
        except Exception:
            # Als er iets mis gaat, ga door zonder error
            pass
    
    def clear(self) -> None:
        """Leeg alle cache"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
    
    def clear_expired(self) -> None:
        """Verwijder verlopen cache bestanden"""
        now = datetime.now()
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                if now - cache_time > timedelta(hours=self.max_age_hours):
                    cache_file.unlink()
            
            except Exception:
                # Als er iets mis gaat, verwijder het bestand
                cache_file.unlink()

# Globale cache instance
cache_manager = CacheManager()

def cache_result(func):
    """Decorator voor het cachen van functie resultaten"""
    def wrapper(*args, **kwargs):
        # Genereer cache key op basis van functie naam en argumenten
        cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
        
        # Probeer resultaat uit cache te halen
        cached_result = cache_manager.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Voer functie uit en cache resultaat
        result = func(*args, **kwargs)
        cache_manager.set(cache_key, result)
        
        return result
    
    return wrapper

# Voorbeeld gebruik
if __name__ == "__main__":
    # Test caching
    @cache_result
    def expensive_operation(data: str) -> str:
        """Simuleer een dure operatie"""
        import time
        time.sleep(1)  # Simuleer processing tijd
        return f"Processed: {data}"
    
    # Eerste keer - duurt lang
    print("Eerste keer...")
    result1 = expensive_operation("test data")
    print(f"Result: {result1}")
    
    # Tweede keer - snel uit cache
    print("Tweede keer...")
    result2 = expensive_operation("test data")
    print(f"Result: {result2}")
    
    # Cache stats
    print(f"Cache directory: {cache_manager.cache_dir}")
    print(f"Cache bestanden: {list(cache_manager.cache_dir.glob('*.json'))}")
