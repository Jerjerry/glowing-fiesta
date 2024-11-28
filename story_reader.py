import tkinter as tk
from tkinter import ttk
import os
import asyncio
import edge_tts
import pygame
import tempfile
import time
import re
import aiohttp
import sys

class StoryReader:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Story Reader")
        self.window.geometry("1000x800")
        
        # Initialize audio
        pygame.mixer.init()
        self.temp_dir = tempfile.gettempdir()
        self.temp_file = os.path.join(self.temp_dir, "story_speech.mp3")
        self.chunk_size = 6000
        
        # Story text area
        self.text_area = tk.Text(self.window, height=35, width=100)
        self.text_area.pack(pady=20, padx=20)
        
        # Read button
        self.read_button = ttk.Button(self.window, text="Read Story", command=self.read_story)
        self.read_button.pack(pady=10)
        
        # Status label with wrapping
        self.status = ttk.Label(self.window, text="", wraplength=700)
        self.status.pack(pady=10)
        
        # Voice settings
        self.voice = {
            'voice': 'en-US-ChristopherNeural',  # Starting with Christopher
            'rate': '+0%',
            'volume': '+0%'
        }
        
        # Show ready status
        self.status.config(text="Ready to read. Paste your story and click 'Read Story'")
    
    async def check_internet(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('http://www.google.com', timeout=5) as response:
                    return response.status == 200
        except:
            return False

    def split_into_chunks(self, text):
        sentences = re.split('([.!?]+)', text)
        chunks = []
        current_chunk = ""
        
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
            if len(current_chunk) + len(sentence) < self.chunk_size:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks

    async def generate_speech(self, text):
        voices = [
            'en-US-ChristopherNeural',
            'en-US-GuyNeural',
            'en-US-EricNeural',
            'en-US-DavisNeural'
        ]
        
        # Try each voice until one works
        for voice in voices:
            try:
                self.voice['voice'] = voice
                communicate = edge_tts.Communicate(
                    text,
                    self.voice['voice'],
                    rate=self.voice['rate'],
                    volume=self.voice['volume']
                )
                await communicate.save(self.temp_file)
                return None
            except edge_tts.exceptions.NoConnectionException:
                continue
            except Exception as e:
                print(f"Error with voice {voice}: {str(e)}", file=sys.stderr)
                continue
        
        return "Could not connect to the voice service. Please check:\n1. Your internet connection\n2. That you're not using a VPN\n3. That you have Microsoft Edge installed"

    def play_audio(self):
        try:
            pygame.mixer.music.load(self.temp_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                self.window.update()
            return True
        except Exception as e:
            print(f"Audio playback error: {str(e)}", file=sys.stderr)
            return False

    async def read_chunk(self, chunk, chunk_num, total_chunks):
        self.status.config(text=f"Reading part {chunk_num} of {total_chunks}...")
        self.window.update()
        
        # Check internet before trying to generate speech
        if not await self.check_internet():
            return "No internet connection detected. Please check your connection and try again."
        
        error = await self.generate_speech(chunk)
        if error is None:
            if self.play_audio():
                # Small pause between chunks
                time.sleep(0.5)
                
                # Cleanup
                pygame.mixer.music.unload()
                try:
                    os.remove(self.temp_file)
                except:
                    pass
                
                return None
            else:
                return "Problem playing the audio. Please try again."
        return error

    def read_story(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            self.status.config(text="Please paste a story first")
            return
        
        self.read_button.config(state='disabled')
        chunks = self.split_into_chunks(text)
        
        async def read_all_chunks():
            for i, chunk in enumerate(chunks, 1):
                error = await self.read_chunk(chunk, i, len(chunks))
                if error:
                    self.status.config(text=error)
                    self.read_button.config(state='normal')
                    return
            self.status.config(text="Ready for another story!")
            self.read_button.config(state='normal')
        
        asyncio.run(read_all_chunks())

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    reader = StoryReader()
    reader.run()
