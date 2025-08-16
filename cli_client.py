#!/usr/bin/env python3
"""
CLI Client for Prompt Guessing Game API
Demonstrates how to interact with the REST API
"""

import requests
import json
import base64
import os
import sys
from typing import Optional
import argparse
from PIL import Image
from io import BytesIO

class GameAPIClient:
    """Client for interacting with the Prompt Guessing Game API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session_id: Optional[str] = None
    
    def create_session(self, target_image_path: str, model_type: str = "pollinations") -> dict:
        """Create a new game session"""
        url = f"{self.base_url}/game/create"
        
        try:
            with open(target_image_path, 'rb') as f:
                files = {'target_image': f}
                data = {'model_type': model_type}
                
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                
                session_data = response.json()
                self.session_id = session_data['session_id']
                
                print(f"✅ Session created: {self.session_id}")
                print(f"🎨 Model: {model_type}")
                print(f"🎯 Target: {target_image_path}")
                
                return session_data
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to create session: {e}")
            return {}
        except FileNotFoundError:
            print(f"❌ Target image not found: {target_image_path}")
            return {}
    
    def get_target_image(self, save_path: Optional[str] = None) -> bool:
        """Get and optionally save the target image"""
        if not self.session_id:
            print("❌ No active session")
            return False
        
        url = f"{self.base_url}/game/{self.session_id}/target"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"💾 Target image saved: {save_path}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get target image: {e}")
            return False
    
    def make_attempt(self, prompt: str, num_steps: int = 20, guidance: float = 7.5) -> dict:
        """Make a prompt attempt"""
        if not self.session_id:
            print("❌ No active session")
            return {}
        
        url = f"{self.base_url}/game/attempt"
        
        payload = {
            "session_id": self.session_id,
            "prompt": prompt,
            "num_inference_steps": num_steps,
            "guidance_scale": guidance
        }
        
        try:
            print(f"🔄 Generating image for: '{prompt}'")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            print(f"📊 Score: {result['score']:.3f}")
            print(f"💬 {result['feedback']}")
            
            if result['is_best']:
                print("🏆 NEW BEST SCORE!")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to make attempt: {e}")
            return {}
    
    def get_progress(self) -> dict:
        """Get current game progress"""
        if not self.session_id:
            print("❌ No active session")
            return {}
        
        url = f"{self.base_url}/game/{self.session_id}/progress"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            progress = response.json()
            
            print(f"\n📈 PROGRESS:")
            print(f"   Attempts: {progress['attempts']}")
            print(f"   Best Score: {progress['best_score']:.3f}")
            print(f"   Best Prompt: '{progress['best_prompt']}'")
            
            if progress['recent_scores']:
                recent = [f"{s:.3f}" for s in progress['recent_scores']]
                print(f"   Recent: {recent}")
            
            if progress['is_victory']:
                print("🎉 VICTORY ACHIEVED!")
            
            return progress
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get progress: {e}")
            return {}
    
    def get_generated_image(self, attempt_number: int, save_path: Optional[str] = None) -> bool:
        """Get generated image from specific attempt"""
        if not self.session_id:
            print("❌ No active session")
            return False
        
        url = f"{self.base_url}/game/{self.session_id}/attempt/{attempt_number}/image"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"💾 Generated image saved: {save_path}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get generated image: {e}")
            return False
    
    def list_sessions(self) -> list:
        """List all active sessions"""
        url = f"{self.base_url}/game/sessions"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            sessions = data.get('sessions', [])
            
            if sessions:
                print("\n📋 Active Sessions:")
                for session in sessions:
                    print(f"   {session['session_id'][:8]}... - {session['model_type']} - {session['attempts']} attempts")
            else:
                print("📋 No active sessions")
            
            return sessions
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to list sessions: {e}")
            return []
    
    def delete_session(self) -> bool:
        """Delete current session"""
        if not self.session_id:
            print("❌ No active session")
            return False
        
        url = f"{self.base_url}/game/{self.session_id}"
        
        try:
            response = requests.delete(url)
            response.raise_for_status()
            
            print(f"🗑️ Session deleted: {self.session_id}")
            self.session_id = None
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to delete session: {e}")
            return False

def interactive_mode(client: GameAPIClient):
    """Interactive CLI mode"""
    print("🎯 Interactive Prompt Guessing Game")
    print("=" * 50)
    
    # Get target image
    target_path = input("Enter path to target image: ").strip()
    if not target_path:
        print("❌ Target image path required")
        return
    
    # Choose model
    print("\nChoose AI model:")
    print("1. Pollinations.ai (free)")
    print("2. Hugging Face (local)")
    print("3. Replicate (API key required)")
    
    model_choice = input("Enter choice (1-3): ").strip()
    model_map = {"1": "pollinations", "2": "huggingface", "3": "replicate"}
    model_type = model_map.get(model_choice, "pollinations")
    
    # Create session
    session_data = client.create_session(target_path, model_type)
    if not session_data:
        return
    
    # Save target image for reference
    client.get_target_image("current_target.jpg")
    print("💡 Target image saved as 'current_target.jpg' for reference")
    
    print("\n" + "=" * 50)
    print("Enter prompts to match the target image!")
    print("Commands: 'progress', 'quit', 'help'")
    print("=" * 50)
    
    # Game loop
    while True:
        try:
            prompt = input(f"\n[Attempt] Enter prompt: ").strip()
            
            if prompt.lower() == 'quit':
                client.delete_session()
                break
            elif prompt.lower() == 'progress':
                client.get_progress()
                continue
            elif prompt.lower() == 'help':
                print("\n📖 Commands:")
                print("  - Enter any prompt to generate image")
                print("  - 'progress' - Show game statistics")
                print("  - 'quit' - Exit and cleanup")
                continue
            elif not prompt:
                print("⚠️  Please enter a prompt")
                continue
            
            # Make attempt
            result = client.make_attempt(prompt)
            
            if result:
                # Save generated image
                attempt_num = result['attempt_number']
                gen_path = f"generated_{attempt_num:03d}.jpg"
                client.get_generated_image(attempt_num, gen_path)
                
                # Check victory
                progress = client.get_progress()
                if progress.get('is_victory'):
                    print("🎉 Congratulations! You won!")
                    client.delete_session()
                    break
                    
        except KeyboardInterrupt:
            print("\n\n⏸️  Game interrupted")
            client.delete_session()
            break

def batch_mode(client: GameAPIClient, target_path: str, prompts: list, model_type: str = "pollinations"):
    """Batch processing mode"""
    print("🔄 Batch Processing Mode")
    print("=" * 50)
    
    # Create session
    session_data = client.create_session(target_path, model_type)
    if not session_data:
        return
    
    # Process all prompts
    results = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Batch {i}/{len(prompts)} ---")
        result = client.make_attempt(prompt)
        
        if result:
            results.append(result)
            # Save generated image
            gen_path = f"batch_{i:03d}_generated.jpg"
            client.get_generated_image(result['attempt_number'], gen_path)
    
    # Final results
    print("\n" + "=" * 50)
    print("🏁 Batch Results:")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. '{result['prompt'][:50]}...' - Score: {result['score']:.3f}")
    
    # Show final progress
    client.get_progress()
    client.delete_session()

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Prompt Guessing Game CLI Client")
    parser.add_argument("--server", default="http://localhost:8000", help="API server URL")
    parser.add_argument("--target", help="Target image path")
    parser.add_argument("--model", default="pollinations", choices=["pollinations", "huggingface", "replicate"], help="AI model")
    parser.add_argument("--batch", nargs="+", help="Batch mode with prompts")
    parser.add_argument("--list", action="store_true", help="List active sessions")
    
    args = parser.parse_args()
    
    # Initialize client
    client = GameAPIClient(args.server)
    
    # Check server health
    try:
        response = requests.get(f"{args.server}/health")
        response.raise_for_status()
        print(f"✅ Connected to API server: {args.server}")
    except requests.exceptions.RequestException:
        print(f"❌ Cannot connect to API server: {args.server}")
        print("💡 Make sure the server is running: python api_server.py")
        return
    
    # Handle different modes
    if args.list:
        client.list_sessions()
    elif args.batch and args.target:
        batch_mode(client, args.target, args.batch, args.model)
    elif args.target:
        # Quick single session
        session_data = client.create_session(args.target, args.model)
        if session_data:
            client.get_target_image("target_reference.jpg")
            print("💡 Ready for prompts! Use interactive mode for full experience.")
    else:
        # Interactive mode
        interactive_mode(client)

if __name__ == "__main__":
    main()