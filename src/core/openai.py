import base64
from io import BytesIO
import logging
from openai import AsyncOpenAI
from typing import Optional, Union
from PIL import Image
import random
import asyncio

logger = logging.getLogger(__name__)

class OpenAIChatAnalyzer:
    """
    A class to handle chat analysis and translation using OpenAI's vision model.
    This class is specifically designed to process game chat images and return
    translated text.
    """
    
    def __init__(self, api_key: str, dev_mode: bool = False):
        """
        Initialize the OpenAI client with the provided API key.
        
        Args:
            api_key (str): OpenAI API key for authentication
            dev_mode (bool): If True, use mock responses instead of real API calls
        """
        self.dev_mode = dev_mode
        if not dev_mode:
            self.client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
        
        self.system_prompt = """You translate game chat from Portuguese to English. Format: [Team] Name: message
Do not include explanations or original text."""

        # Mock responses for development mode
        self.mock_responses = [
            """[Team] Player1: hi everyone, wanna play?
[Team] Player2: yeah, let's go!
[Team] Player3: wait a moment please""",

            """[Team] TeamLeader: does anyone know how to play Hulk?
[Team] Pro_Gamer: just smash everything lol
[Team] NewPlayer: I need help with the controls""",

            """[Team] Player4: nice play!
[Team] Player5: thanks for the help
[Team] Player6: let's win this match"""
        ]

    def _encode_image_file(self, image_path: str) -> str:
        """
        Encode an image file to base64 string.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _encode_pil_image(self, image: Image.Image) -> str:
        """
        Encode a PIL Image to base64 string.
        
        Args:
            image (PIL.Image.Image): PIL Image object
            
        Returns:
            str: Base64 encoded image string
        """
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def _prepare_image_payload(self, image_data: str) -> dict:
        """
        Prepare the image payload for the OpenAI API.
        
        Args:
            image_data (str): Base64 encoded image or image URL
            
        Returns:
            dict: Formatted image payload for the API
        """
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_data}"
                if "http" not in image_data
                else image_data
            }
        }

    async def _get_mock_response(self) -> str:
        """Get a random mock response for development mode"""
        # Add random delay to simulate API latency
        await asyncio.sleep(random.uniform(0.5, 2.0))
        return random.choice(self.mock_responses)

    async def analyze_chat(
        self,
        image_input: Union[str, Image.Image],
        max_tokens: int = 300,  # Reduced from 1000
        temperature: float = 0.7,
        is_url: bool = False
    ) -> Optional[str]:
        """
        Analyze a chat image and return translated content.
        
        Args:
            image_input: Path to image file, URL, or PIL Image object
            max_tokens (int): Maximum tokens for response
            temperature (float): Temperature for response generation
            is_url (bool): Whether the image_input is a URL
            
        Returns:
            Optional[str]: Translated and processed chat content
            
        Raises:
            Exception: If there's an error in processing the image or API call
        """
        try:
            if self.dev_mode:
                # In development mode, return mock response
                return await self._get_mock_response()

            # Handle different types of image input
            if isinstance(image_input, Image.Image):
                image_data = self._encode_pil_image(image_input)
            elif is_url:
                image_data = image_input
            else:
                image_data = self._encode_image_file(image_input)

            image_payload = self._prepare_image_payload(image_data)
            
            # Make API call
            response = await self.client.chat.completions.create(
                model="openai/gpt-4o-mini-2024-07-18",
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Translate:"
                            },
                            image_payload
                        ]
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            content = response.choices[0].message.content
            return self._clean_response(content)
            
        except Exception as e:
            logger.error(f"Error processing chat image: {str(e)}")
            raise  # Re-raise the exception for better error handling
            
    def update_system_prompt(self, new_prompt: str) -> None:
        """
        Update the system prompt used for chat analysis.
        
        Args:
            new_prompt (str): New system prompt to be used
        """
        self.system_prompt = new_prompt
        
    def _clean_response(self, response: str) -> str:
        """
        Clean the response to remove unwanted elements.
        
        Args:
            response (str): Raw response from API
            
        Returns:
            str: Cleaned response
        """
        # Remove code blocks
        response = response.replace('```', '').strip()
        
        # Remove any introductory text
        if "here's" in response.lower() or "translation" in response.lower():
            # Split by newlines and find where the actual chat starts
            lines = response.split('\n')
            for i, line in enumerate(lines):
                if '[' in line and ']' in line:  # Found a chat message
                    response = '\n'.join(lines[i:])
                    break
        
        return response.strip()

    def add_mock_response(self, response: str) -> None:
        """
        Add a new mock response to the pool of possible responses.
        
        Args:
            response (str): New mock response to add
        """
        self.mock_responses.append(response)
        
    async def analyze_text_only(
        self,
        text: str,
        max_tokens: int = 300,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Test method for analyzing raw text without image processing.
        This can be used to compare token usage with the image-based method.
        
        Args:
            text: Raw text from OCR
            max_tokens: Maximum tokens for response
            temperature: Temperature for response generation
        """
        try:
            # Make API call
            response = await self.client.chat.completions.create(
                model="openai/gpt-4o-mini-2024-07-18",
                messages=[
                    {
                        "role": "system",
                        "content": "You translate game chat from Portuguese to English. Format: [Team] Name: message"
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return self._clean_response(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            raise