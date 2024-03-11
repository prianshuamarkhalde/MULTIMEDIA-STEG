import tkinter as tk
from tkinter import filedialog

class TextFileSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Steganography")

        # Variables
        self.cover_text_path = tk.StringVar()
        self.secret_text = tk.StringVar()

        # GUI Elements
        self.label_cover_text = tk.Label(root, text="Select Cover Text File:", font=("Helvetica", 12))
        self.entry_cover_text = tk.Entry(root, textvariable=self.cover_text_path, state="readonly", width=30, font=("Helvetica", 10))
        self.button_browse_cover_text = tk.Button(root, text="Browse", command=self.browse_cover_text, font=("Helvetica", 10))
        self.label_secret_text = tk.Label(root, text="Enter Secret Text:", font=("Helvetica", 12))
        self.entry_secret_text = tk.Entry(root, textvariable=self.secret_text, width=30, font=("Helvetica", 10))
        self.button_hide = tk.Button(root, text="Hide Text", command=self.hide_text, font=("Helvetica", 10))
        self.button_retrieve = tk.Button(root, text="Retrieve Text", command=self.retrieve_text, font=("Helvetica", 10))

        # Layout
        self.label_cover_text.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_cover_text.grid(row=0, column=1, padx=10, pady=5)
        self.button_browse_cover_text.grid(row=0, column=2, padx=10, pady=5)
        self.label_secret_text.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_secret_text.grid(row=1, column=1, padx=10, pady=5)
        self.button_hide.grid(row=2, column=1, padx=10, pady=5)
        self.button_retrieve.grid(row=3, column=1, padx=10, pady=5)

        # Styling
        self.root.configure(bg="#F0F0F0")
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg="#4CAF50", fg="white", padx=10, pady=5)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="white", fg="black", relief=tk.GROOVE, font=("Helvetica", 10))
            elif isinstance(widget, tk.Label):
                widget.configure(bg="#F0F0F0", fg="#333333", font=("Helvetica", 12, "bold"))

    def browse_cover_text(self):
        file_path = filedialog.askopenfilename(title="Select Cover Text File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.cover_text_path.set(file_path)

    def encode_text(self, cover_text_path, secret_text):
        with open(cover_text_path, 'a') as cover_file:
            cover_file.write('\n' + secret_text)

    def hide_text(self):
        cover_text_path = self.cover_text_path.get()
        secret_text = self.secret_text.get()

        if cover_text_path and secret_text:
            self.encode_text(cover_text_path, secret_text)
            print("Text hidden successfully.")
        else:
            print("Please select a cover text file and enter a secret text.")

    def retrieve_text(self):
        cover_text_path = self.cover_text_path.get()

        if cover_text_path:
            with open(cover_text_path, 'r') as cover_file:
                lines = cover_file.readlines()

            # Retrieve the hidden text from the last line
            if lines:
                hidden_text = lines[-1].strip()
                print(f"Hidden Text: {hidden_text}")
            else:
                print("No hidden text found.")
        else:
            print("Please select a cover text file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextFileSteganographyApp(root)
    root.mainloop()
