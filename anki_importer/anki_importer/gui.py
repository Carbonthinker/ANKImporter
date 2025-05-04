import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from .anki_connect import AnkiConnect
from .flashcard_parser import extract_flashcards

class AnkiImporterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Anki Importer")
        self.anki = AnkiConnect()
        
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Deck name entry
        tk.Label(main_frame, text="Anki Deck Name:").pack(pady=5)
        self.deck_entry = tk.Entry(main_frame, width=40)
        self.deck_entry.pack(pady=5)
        self.deck_entry.insert(0, "ChatGPT Imported Cards")

        # Text input area
        tk.Label(main_frame, text="Paste your flashcards here:").pack(pady=5)
        self.text_box = scrolledtext.ScrolledText(main_frame, width=50, height=10)
        self.text_box.pack(pady=5)

        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Import buttons
        tk.Button(buttons_frame, text="Import from Text", command=self.import_from_text).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Import from File", command=self.import_from_file).pack(side=tk.LEFT, padx=5)

    def import_from_text(self):
        if not self.anki.check_connection():
            messagebox.showerror("Error", "Could not connect to Anki. Please make sure:\n1. Anki is running\n2. Anki Connect is installed and enabled\n3. Anki Connect is running on port 8765")
            return

        text = self.text_box.get("1.0", tk.END)
        deck_name = self.deck_entry.get().strip()
        
        if not deck_name:
            messagebox.showerror("Error", "Please enter a deck name.")
            return
            
        flashcards = extract_flashcards(text)
        if not flashcards:
            messagebox.showerror("Error", "No flashcards found. Check the format of your text.")
            return

        self.process_flashcards(flashcards, deck_name)

    def import_from_file(self):
        if not self.anki.check_connection():
            messagebox.showerror("Error", "Could not connect to Anki. Please make sure:\n1. Anki is running\n2. Anki Connect is installed and enabled\n3. Anki Connect is running on port 8765")
            return

        file_path = filedialog.askopenfilename(
            title="Select flashcards.txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if not file_path:
            return

        deck_name = self.deck_entry.get().strip()
        if not deck_name:
            messagebox.showerror("Error", "Please enter a deck name.")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")
            return

        flashcards = extract_flashcards(text)
        if not flashcards:
            messagebox.showerror("Error", "No flashcards found. Check the format of your file.")
            return

        self.process_flashcards(flashcards, deck_name)

    def process_flashcards(self, flashcards, deck_name):
        # Check if deck exists, if not create it
        if not self.anki.check_deck_exists(deck_name):
            if not self.anki.create_deck(deck_name):
                messagebox.showerror("Error", f"Could not create deck '{deck_name}'. Please check Anki and try again.")
                return

        added = 0
        errors = 0
        for q, a in flashcards:
            res = self.anki.add_note(q, a, deck_name)
            if "error" in res and res["error"] is None:
                added += 1
            else:
                errors += 1
                print(f"⚠️ Error adding card: {res}")

        if added > 0:
            messagebox.showinfo("Success", f"✅ {added} flashcards added to Anki deck '{deck_name}'.")
        if errors > 0:
            messagebox.showwarning("Partial Success", f"⚠️ {errors} cards could not be added. Check the console for details.")

    def run(self):
        self.root.mainloop() 