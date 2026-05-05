import os
import json
import logging
from anthropic import Anthropic
from typing import Dict

logger = logging.getLogger(__name__)

# Model specified by user
MODEL_NAME = "claude-3-5-haiku-20241022" # Using the latest haiku model available

class AITagger:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not found in environment. AI tagging will be disabled.")
            self.client = None
        else:
            self.client = Anthropic(api_key=api_key)

    def tag_opportunity(self, title: str, description: str, organizer: str) -> Dict[str, str]:
        default_tags = {
            "funding_range": "Unknown",
            "startup_stage": "Any",
            "remote_or_onsite": "Unknown"
        }

        if not self.client:
            return default_tags

        prompt = f"""
        Analyze the following startup opportunity and extract specific details in JSON format.
        
        Opportunity Title: {title}
        Organizer: {organizer}
        Description: {description}
        
        Return ONLY a JSON object with these keys:
        - "funding_range": e.g. "$10K–$50K", "Equity-free", or "Unknown"
        - "startup_stage": "Early", "Growth", or "Any"
        - "remote_or_onsite": "Remote", "On-site", or "Hybrid"
        """

        try:
            response = self.client.messages.create(
                model=MODEL_NAME,
                max_tokens=200,
                temperature=0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            # Basic cleanup in case Claude adds markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
        except Exception as e:
            logger.error(f"Error tagging opportunity with Claude: {e}")
            return default_tags

# Singleton instance
tagger = AITagger()
