import json
from typing import Dict, Any
from groq import AsyncGroq
import groq
from app.config.settings import settings
from app.core.logging import logger
from app.exceptions.custom_exceptions import LLMIntegrationError

class GroqClient:
    def __init__(self):
        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
            timeout=settings.GROQ_TIMEOUT,
        )
        self.model = settings.GROQ_MODEL

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Calls the Groq API to generate a JSON response based on the prompts.
        """
        try:
            logger.info(f"Sending request to Groq using model: {self.model}")
            
            completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                model=self.model,
                temperature=0.2, # Low temperature for more deterministic/analytical output
                response_format={"type": "json_object"},
            )
            
            response_content = completion.choices[0].message.content
            logger.debug(f"Groq API raw response: {response_content}")
            
            # Parse the JSON response
            try:
                parsed_json = json.loads(response_content)
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from Groq response: {e}")
                logger.error(f"Raw content: {response_content}")
                raise LLMIntegrationError("Received invalid JSON format from LLM.")
                
        except groq.APIError as e:
            logger.error(f"Groq API Error: {e}")
            raise LLMIntegrationError(f"Groq API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error calling Groq: {e}", exc_info=True)
            raise LLMIntegrationError("An unexpected error occurred while communicating with the LLM.")
