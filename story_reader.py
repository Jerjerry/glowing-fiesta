import tkinter as tk
from tkinter import ttk, scrolledtext
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
        
        # Configure window grid
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Set theme and style
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TLabel', font=('Segoe UI', 10))
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Title label with custom font
        title_label = ttk.Label(
            main_frame, 
            text="Story Reader", 
            font=('Segoe UI', 16, 'bold'),
            padding=(0, 0, 0, 10)
        )
        title_label.grid(row=0, column=0, sticky="n")
        
        # Initialize audio
        pygame.mixer.init()
        self.temp_dir = tempfile.gettempdir()
        self.temp_file = os.path.join(self.temp_dir, "story_speech.mp3")
        self.chunk_size = 6000
        
        # Create text frame with proper padding
        text_frame = ttk.Frame(main_frame, padding=(0, 10))
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        # Story text area with word wrap and scrollbar
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            padx=10,
            pady=10,
            height=25,
            width=80,
            borderwidth=1,
            relief="solid"
        )
        self.text_area.grid(row=0, column=0, sticky="nsew")
        
        # Button frame
        button_frame = ttk.Frame(main_frame, padding=(0, 10))
        button_frame.grid(row=2, column=0)
        
        # Read button with modern styling
        self.read_button = ttk.Button(
            button_frame,
            text="Read Story",
            command=self.read_story,
            style='TButton',
            padding=(20, 5)
        )
        self.read_button.grid(row=0, column=0, pady=5)
        
        # Status label with word wrap
        self.status = ttk.Label(
            main_frame,
            text="Ready to read. Paste your story and click 'Read Story'",
            wraplength=800,
            justify='center',
            style='TLabel'
        )
        self.status.grid(row=3, column=0, pady=10)
        
        # Voice settings
        self.voice = {
            'voice': 'en-US-ChristopherNeural',
            'rate': '+0%',
            'volume': '+0%'
        }
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - 1000) // 2
        y = (screen_height - 800) // 2
        
        # Set window position
        self.window.geometry(f"1000x800+{x}+{y}")
    
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
