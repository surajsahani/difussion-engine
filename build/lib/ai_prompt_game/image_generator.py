#!/usr/bin/env python3
"""
Image generation module using various AI providers
"""

import requests
import numpy as np
import cv2
from PIL import Image
import io
import urllib.parse

class ImageGenerator:
    """Handles AI image generation from prompts"""
    
    def __init__(self, model_type="pollinations"):
        self.model_type = model_type
        self.setup_generator()
    
    def setup_generator(self):
        """Setup the selected generator"""
        if self.model_type == "pollinations":
            self.base_url = "https://image.pollinations.ai/prompt/"
        elif self.model_type == "huggingface":
            self.setup_huggingface()
        elif self.model_type == "replicate":
            self.setup_replicate()
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def setup_huggingface(self):
        """Setup Hugging Face local generation"""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            model_id = "runwayml/stable-diffusion-v1-5"
            
            if torch.cuda.is_available():
                self.pipe = StableDiffusionPipeline.from_pretrained(
                    model_id, torch_dtype=torch.float16
                ).to("cuda")
            else:
                self.pipe = StableDiffusionPipeline.from_pretrained(model_id)
                
        except ImportError:
            raise ImportError("Install diffusers and torch for Hugging Face support")
    
    def setup_replicate(self):
        """Setup Replicate API"""
        try:
            import replicate
            self.replicate_client = replicate
        except ImportError:
            raise ImportError("Install replicate package for Replicate support")
    
    def generate(self, prompt, width=512, height=512, steps=20, guidance=7.5):
        """Generate image from prompt"""
        if self.model_type == "pollinations":
            return self.generate_pollinations(prompt, width, height)
        elif self.model_type == "huggingface":
            return self.generate_huggingface(prompt, steps, guidance)
        elif self.model_type == "replicate":
            return self.generate_replicate(prompt)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def generate_pollinations(self, prompt, width=512, height=512):
        """Generate image using Pollinations.ai"""
        try:
            # URL encode the prompt
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Build URL with parameters
            url = f"{self.base_url}{encoded_prompt}"
            params = {
                'width': width,
                'height': height,
                'seed': -1,  # Random seed
                'model': 'flux'  # Use Flux model for better quality
            }
            
            # Add parameters to URL
            param_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{url}?{param_string}"
            
            # Make request
            response = requests.get(full_url, timeout=60)
            response.raise_for_status()
            
            # Convert to OpenCV format
            image = Image.open(io.BytesIO(response.content))
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            return image_cv
            
        except requests.exceptions.Timeout:
            raise Exception("AI generation timed out. Try again in a moment.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"AI generation failed: {e}")
        except Exception as e:
            raise Exception(f"Image processing error: {e}")
    
    def generate_huggingface(self, prompt, steps=20, guidance=7.5):
        """Generate image using local Hugging Face model"""
        try:
            import torch
            
            with torch.no_grad():
                image = self.pipe(
                    prompt,
                    num_inference_steps=steps,
                    guidance_scale=guidance,
                    height=512,
                    width=512
                ).images[0]
            
            # Convert to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            return image_cv
            
        except Exception as e:
            raise Exception(f"Local generation failed: {e}")
    
    def generate_replicate(self, prompt):
        """Generate image using Replicate API"""
        try:
            output = self.replicate_client.run(
                "stability-ai/stable-diffusion:27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478",
                input={"prompt": prompt}
            )
            
            # Download image from URL
            response = requests.get(output[0])
            response.raise_for_status()
            
            image = Image.open(io.BytesIO(response.content))
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            return image_cv
            
        except Exception as e:
            raise Exception(f"Replicate generation failed: {e}")
    
    def test_connection(self):
        """Test if the generator is working"""
        try:
            test_image = self.generate("test image", width=64, height=64)
            return test_image is not None
        except:
            return False