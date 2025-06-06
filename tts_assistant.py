import tkinter as tk
from tkinter import scrolledtext, messagebox
import pyttsx3
import threading
import os
import tempfile
from gtts import gTTS # type: ignore
import pygame



class TTSAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant with Text-to-Speech")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize TTS engines
        self.pyttsx3_engine = pyttsx3.init()
        self.setup_pyttsx3()
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize audio: {e}")
        
        # Variables
        self.is_speaking = False
        self.current_thread = None
        
        self.setup_ui()
    
    def setup_pyttsx3(self):
        """Configure pyttsx3 engine settings"""
        voices = self.pyttsx3_engine.getProperty('voices')
        if voices:
            # Set to female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.pyttsx3_engine.setProperty('voice', voice.id)
                    break
        
        # Set speech rate and volume
        self.pyttsx3_engine.setProperty('rate', 180)  # Speed of speech
        self.pyttsx3_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
    
    def setup_ui(self):
        """Create the user interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🤖 AI Assistant with Text-to-Speech", 
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Text input section
        input_label = tk.Label(
            main_frame, 
            text="Enter text to speak:", 
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        input_label.pack(anchor='w', pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            font=("Arial", 11),
            wrap=tk.WORD,
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # TTS Engine selection
        engine_frame = tk.Frame(main_frame, bg='#2c3e50')
        engine_frame.pack(fill='x', pady=(0, 15))
        
        engine_label = tk.Label(
            engine_frame,
            text="TTS Engine:",
            font=("Arial", 10, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        engine_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.engine_var = tk.StringVar(value="pyttsx3")
        engines = [("Offline (pyttsx3)", "pyttsx3"), ("Google TTS", "gtts")]
        
        for text, value in engines:
            rb = tk.Radiobutton(
                engine_frame,
                text=text,
                variable=self.engine_var,
                value=value,
                bg='#2c3e50',
                fg='#ecf0f1',
                selectcolor='#34495e',
                font=("Arial", 10)
            )
            rb.pack(side=tk.LEFT, padx=(0, 15))
        
        # Voice settings frame
        settings_frame = tk.Frame(main_frame, bg='#2c3e50')
        settings_frame.pack(fill='x', pady=(0, 20))
        
        # Speed control
        speed_label = tk.Label(
            settings_frame,
            text="Speed:",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        speed_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.speed_var = tk.IntVar(value=180)
        self.speed_scale = tk.Scale(
            settings_frame,
            from_=100,
            to=300,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg='#34495e',
            fg='#ecf0f1',
            highlightbackground='#2c3e50',
            troughcolor='#34495e',
            command=self.update_speed
        )
        self.speed_scale.pack(side=tk.LEFT, padx=(0, 20))
        
        # Volume control
        volume_label = tk.Label(
            settings_frame,
            text="Volume:",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        volume_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.volume_var = tk.DoubleVar(value=0.9)
        self.volume_scale = tk.Scale(
            settings_frame,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            bg='#34495e',
            fg='#ecf0f1',
            highlightbackground='#2c3e50',
            troughcolor='#34495e',
            command=self.update_volume
        )
        self.volume_scale.pack(side=tk.LEFT)
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(fill='x', pady=10)
        
        # Speak button
        self.speak_button = tk.Button(
            button_frame,
            text="🔊 Speak Text",
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.speak_text
        )
        self.speak_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ Stop",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.stop_speech,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=("Arial", 12, "bold"),
            bg='#95a5a6',
            fg='white',
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.clear_text
        )
        clear_button.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to speak!",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        self.status_label.pack(pady=10)
        
        # Sample texts
        samples_frame = tk.LabelFrame(
            main_frame,
            text="Sample Texts",
            font=("Arial", 10, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1',
            labelanchor='n'
        )
        samples_frame.pack(fill='x', pady=(20, 0))
        
        sample_texts = [
            "Hello! I am your AI assistant. How can I help you today?",
            "The weather is beautiful today. Perfect for a walk in the park!",
            "Technology continues to amaze us with new possibilities every day."
        ]
        
        for i, sample in enumerate(sample_texts):
            btn = tk.Button(
                samples_frame,
                text=f"Sample {i+1}",
                font=("Arial", 9),
                bg='#3498db',
                fg='white',
                relief=tk.FLAT,
                command=lambda s=sample: self.load_sample(s)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def load_sample(self, text):
        """Load sample text into the input field"""
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', text)
    
    def update_speed(self, value):
        """Update TTS speed"""
        self.pyttsx3_engine.setProperty('rate', int(value))
    
    def update_volume(self, value):
        """Update TTS volume"""
        self.pyttsx3_engine.setProperty('volume', float(value))
    
    def clear_text(self):
        """Clear the text input"""
        self.text_input.delete('1.0', tk.END)
        self.status_label.config(text="Text cleared. Ready to speak!")
    
    def speak_with_pyttsx3(self, text):
        """Speak text using pyttsx3 (offline)"""
        try:
            self.pyttsx3_engine.say(text)
            self.pyttsx3_engine.runAndWait()
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"pyttsx3 error: {str(e)}"))
        finally:
            self.root.after(0, self.speech_finished)
    
    def speak_with_gtts(self, text):
        """Speak text using Google TTS (online)"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_filename = tmp_file.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(tmp_filename)
            
            # Play audio
            pygame.mixer.music.load(tmp_filename)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Clean up
            os.unlink(tmp_filename)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Google TTS error: {str(e)}"))
        finally:
            self.root.after(0, self.speech_finished)
    
    def speak_text(self):
        """Main function to speak text"""
        text = self.text_input.get('1.0', tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to speak!")
            return
        
        if self.is_speaking:
            messagebox.showinfo("Info", "Already speaking! Please wait or stop current speech.")
            return
        
        # Update UI
        self.is_speaking = True
        self.speak_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"Speaking with {self.engine_var.get()}...")
        
        # Start speech in separate thread
        engine = self.engine_var.get()
        if engine == "pyttsx3":
            self.current_thread = threading.Thread(target=self.speak_with_pyttsx3, args=(text,))
        else:  # gtts
            self.current_thread = threading.Thread(target=self.speak_with_gtts, args=(text,))
        
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def stop_speech(self):
        """Stop current speech"""
        if self.engine_var.get() == "pyttsx3":
            self.pyttsx3_engine.stop()
        else:
            pygame.mixer.music.stop()
        
        self.speech_finished()
    
    def speech_finished(self):
        """Called when speech is finished"""
        self.is_speaking = False
        self.speak_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Speech finished. Ready for next text!")
    
    def show_error(self, error_msg):
        """Show error message"""
        messagebox.showerror("Error", error_msg)
        self.speech_finished()

def main():
    # Create and run the application
    root = tk.Tk()
    app = TTSAssistant(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()




