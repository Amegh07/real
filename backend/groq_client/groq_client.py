"""
Groq Integration Layer (Phase 4)
---------------------------------
Clean wrapper around the Groq API.
- Single function for prompts
- Validation and graceful failure
- Caching to avoid redundant API calls
- Graceful fallback to rule-based decisions if API fails
"""

import time
import json
from typing import Optional, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class GroqClient:
    """
    Handles communication with the Groq LLM API.
    Used by DecisionEngine and MemoryBank for complex logic.
    """

    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get("use_groq", False)
        self.model = config.get("groq_model", "llama3-8b-8192")
        self.max_tokens = config.get("groq_max_tokens", 250)
        self.client = None
        
        self._cache: Dict[str, str] = {}

        if self.enabled:
            if not GROQ_AVAILABLE:
                logger.warning("Groq enabled in config, but 'groq' package not installed. Falling back to rule-based.")
                self.enabled = False
            else:
                import os
                from dotenv import load_dotenv
                
                # Load env vars from .env file if present
                load_dotenv()
                
                api_key = os.environ.get("GROQ_API_KEY")
                if not api_key or api_key == "your_groq_api_key_here":
                    logger.warning("Valid GROQ_API_KEY not found in environment. Groq disabled.")
                    self.enabled = False
                else:
                    self.client = Groq(api_key=api_key)
                    logger.info(f"Groq API client initialized ({self.model}).")

    def complete(self, prompt: str, cache_key: Optional[str] = None) -> str:
        """
        Sends a prompt to the Groq API.
        Returns the text response. Raises ValueError if disabled or failed.
        """
        if not self.enabled or not self.client:
            raise ValueError("Groq is disabled or unavailable.")

        if cache_key and cache_key in self._cache:
            return self._cache[cache_key]

        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are the cognitive logic core for a simulation agent. You must analyze the situation and respond EXACTLY in the requested JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            result = response.choices[0].message.content.strip()
            
            elapsed = time.time() - start_time
            logger.debug(f"Groq API call succeeded in {elapsed:.2f}s")
            
            if cache_key:
                # Keep cache small to avoid memory leak
                if len(self._cache) > 500:
                    self._cache.clear()
                self._cache[cache_key] = result
                
            return result
            
        except Exception as e:
            logger.error(f"Groq API error: {e}")
            raise ValueError(f"Groq API call failed: {e}")
