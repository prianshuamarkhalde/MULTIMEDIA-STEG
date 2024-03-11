import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import os

class AudioSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Steganography")

        # Variables
        self.audio_path = tk.StringVar()
        self.message = tk.StringVar()

        # GUI Elements
        self.label_audio = tk.Label(root, text="Select Audio:", font=("Helvetica", 12))
        self.entry_audio = tk.Entry(root, textvariable=self.audio_path, state="readonly", width=30, font=("Helvetica", 10))
        self.button_browse_audio = tk.Button(root, text="Browse Audio", command=self.browse_audio, font=("Helvetica", 10))
        self.label_message = tk.Label(root, text="Enter Message:", font=("Helvetica", 12))
        self.entry_message = tk.Entry(root, textvariable=self.message, width=30, font=("Helvetica", 10))
        self.button_hide = tk.Button(root, text="Hide Message", command=self.hide_message, font=("Helvetica", 10))
        self.button_retrieve = tk.Button(root, text="Retrieve Message", command=self.retrieve_message, font=("Helvetica", 10))

        # Layout
        self.label_audio.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_audio.grid(row=0, column=1, padx=10, pady=5)
        self.button_browse_audio.grid(row=0, column=2, padx=10, pady=5)
        self.label_message.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_message.grid(row=1, column=1, padx=10, pady=5)
        self.button_hide.grid(row=2, column=1, pady=10)
        self.button_retrieve.grid(row=2, column=2, pady=10)

        # Styling
        self.root.configure(bg="#F0F0F0")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg="#4CAF50", fg="white", padx=10, pady=5)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="white", fg="black", relief=tk.GROOVE, font=("Helvetica", 10))
            elif isinstance(widget, tk.Label):
                widget.configure(bg="#F0F0F0", fg="#333333", font=("Helvetica", 12, "bold"))

    def browse_audio(self):
        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio files", "*.mp3;*.wav")])
        if file_path:
            self.audio_path.set(file_path)

    def encode_message(self, audio_path, message):
        audio = AudioSegment.from_file(audio_path)

        # Convert the message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        # Check if the message can fit in the audio file
        if len(binary_message) > len(audio):
            print("Message is too long for the selected audio file.")
            return

        # Encode the message into the audio file
        encoded_audio = audio._spawn(b''.join([bytes([sample & 0xFE | int(bit)]) for sample, bit in zip(audio.raw_data, binary_message)]))
        return encoded_audio

    def hide_message(self):
        audio_path = self.audio_path.get()
        message = self.message.get()

        if audio_path and message:
            encoded_audio = self.encode_message(audio_path, message)

            # Save the new audio file
            encoded_audio_path = "encoded_" + os.path.basename(audio_path)
            encoded_audio.export(encoded_audio_path, format="wav")
            print(f"Message hidden successfully in {encoded_audio_path}")
        else:
            print("Please select an audio file and enter a message.")

    def retrieve_message(self):
        audio_path = self.audio_path.get()

        if audio_path:
            audio = AudioSegment.from_file(audio_path)

            # Retrieve the hidden message from the audio file
            binary_message = ''.join([str(sample & 1) for sample in audio.raw_data])

            # Convert binary to string
            hidden_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
            print(f"Hidden Message: {hidden_message}")

        else:
            print("Please select an audio file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSteganographyApp(root)
    root.mainloop()
