import os
import google.generativeai as genai
from dotenv import load_dotenv
from schemas import DetectionResponse
import json
import typing

load_dotenv()

class GeminiClient:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def detect_clothing(self, image_path: str, prompt: str) -> DetectionResponse:
        """
        Detects clothing items in an image using Gemini.
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at {image_path}")

            # Upload valid file to Gemini (or pass bytes if small, but let's stick to simple path for now)
            # For 1.5 Flash, we can often pass the PIL image or path directly if using the File API.
            # Let's use the standard way: load bytes/PIL
            
            # Note: For production, we might want to use the File API for caching, 
            # but for single inference, passing the data directly is fine.
            
            sample_file = genai.upload_file(path=image_path, display_name="Clothing Image")
            
            # Configure generation config to enforce JSON
            generation_config = genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=DetectionResponse
            )

            response = self.model.generate_content(
                [prompt, sample_file],
                generation_config=generation_config
            )
            
            # Parse response
            # Since we set response_mime_type="application/json", we can assume valid JSON
            # and since we set response_schema, it should match our Pydantic model structure
            
            # There might be a need to handle "safety ratings" blocking the content
            if not response.parts:
                print("No content returned. Safety ratings:", response.prompt_feedback)
                return DetectionResponse(items=[])

            return DetectionResponse.model_validate_json(response.text)

        except Exception as e:
            print(f"Error communicating with Gemini: {e}")
            raise e
