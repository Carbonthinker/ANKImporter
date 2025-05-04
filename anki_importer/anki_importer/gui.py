import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from .anki_connect import AnkiConnect
from .flashcard_parser import extract_flashcards_multi

# Configuration
FIELDS = ["Front", "Back", "Extras"]  # Anki field names
FIELD_MAP = {"References": "Extras"}  # Input to Anki field mapping
DEFAULT_DECK = "ChatGPT Imported Cards"
MODEL_BASIC = "2.Basic"
MODEL_REVERSED = "2.Basic (and reversed card)"

class AnkiImporterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Anki Importer")
        self.anki = AnkiConnect()
        self.fields = FIELDS
        self.field_map = FIELD_MAP
        self.reversed_var = tk.BooleanVar(value=False)
        self.setup_gui()
        
    def setup_gui(self):
        """Initialize the GUI components"""
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Deck name entry
        self._add_deck_entry(main_frame)
        
        # Fields display
        self._add_fields_display(main_frame)
        
        # Reversed card toggle
        self._add_reversed_toggle(main_frame)
        
        # Text input area
        self._add_text_input(main_frame)
        
        # Import buttons
        self._add_import_buttons(main_frame)

    def _add_deck_entry(self, parent):
        """Add deck name entry field"""
        tk.Label(parent, text="Anki Deck Name:").pack(pady=5)
        self.deck_entry = tk.Entry(parent, width=40)
        self.deck_entry.pack(pady=5)
        self.deck_entry.insert(0, DEFAULT_DECK)

    def _add_fields_display(self, parent):
        """Add fields display listbox"""
        fields_frame = tk.Frame(parent)
        fields_frame.pack(pady=5, fill=tk.X)
        tk.Label(fields_frame, text="Fields (fixed):").pack(side=tk.LEFT)
        self.fields_listbox = tk.Listbox(fields_frame, height=3, width=20, font=("Arial", 14))
        self.fields_listbox.pack(side=tk.LEFT, padx=5)
        for f in self.fields:
            self.fields_listbox.insert(tk.END, f)
        self.fields_listbox.config(state=tk.DISABLED)

    def _add_reversed_toggle(self, parent):
        """Add reversed card toggle checkbox"""
        self.rev_check = tk.Checkbutton(
            parent, 
            text="Add reversed card (Back → Front)", 
            variable=self.reversed_var
        )
        self.rev_check.pack(pady=5)

    def _add_text_input(self, parent):
        """Add text input area"""
        tk.Label(parent, text="Paste your flashcards here:").pack(pady=5)
        self.text_box = scrolledtext.ScrolledText(parent, width=50, height=10)
        self.text_box.pack(pady=5)

    def _add_import_buttons(self, parent):
        """Add import buttons"""
        buttons_frame = tk.Frame(parent)
        buttons_frame.pack(pady=10)
        tk.Button(
            buttons_frame, 
            text="Import from Text", 
            command=self.import_from_text
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            buttons_frame, 
            text="Import from File", 
            command=self.import_from_file
        ).pack(side=tk.LEFT, padx=5)

    def _check_anki_connection(self):
        """Check if Anki is running and accessible"""
        if not self.anki.check_connection():
            messagebox.showerror(
                "Error", 
                "Could not connect to Anki. Please make sure:\n"
                "1. Anki is running\n"
                "2. Anki Connect is installed and enabled\n"
                "3. Anki Connect is running on port 8765"
            )
            return False
        return True

    def _get_deck_name(self):
        """Get and validate deck name"""
        deck_name = self.deck_entry.get().strip()
        if not deck_name:
            messagebox.showerror("Error", "Please enter a deck name.")
            return None
        return deck_name

    def _process_text(self, text, deck_name):
        """Process text input and import flashcards"""
        flashcards = extract_flashcards_multi(text, self.fields, self.field_map)
        if not flashcards:
            messagebox.showerror("Error", "No flashcards found. Check the format of your text.")
            return
        self.process_flashcards(flashcards, deck_name)

    def import_from_text(self):
        """Import flashcards from text input"""
        if not self._check_anki_connection():
            return
        deck_name = self._get_deck_name()
        if not deck_name:
            return
        text = self.text_box.get("1.0", tk.END)
        self._process_text(text, deck_name)

    def import_from_file(self):
        """Import flashcards from file"""
        if not self._check_anki_connection():
            return
        file_path = filedialog.askopenfilename(
            title="Select flashcards.txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if not file_path:
            return
        deck_name = self._get_deck_name()
        if not deck_name:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")
            return
        self._process_text(text, deck_name)

    def process_flashcards(self, flashcards, deck_name):
        """Process and import flashcards to Anki"""
        if not self.anki.check_deck_exists(deck_name):
            if not self.anki.create_deck(deck_name):
                messagebox.showerror(
                    "Error", 
                    f"Could not create deck '{deck_name}'. Please check Anki and try again."
                )
                return

        model_name = MODEL_REVERSED if self.reversed_var.get() else MODEL_BASIC
        added = 0
        errors = []

        for idx, card in enumerate(flashcards, 1):
            card_filled = list(card) + [""] * (len(self.fields) - len(card))
            fields_dict = {field: value for field, value in zip(self.fields, card_filled)}
            
            if not fields_dict.get("Front") or not fields_dict.get("Back"):
                errors.append(f"Card {idx}: Front or Back is empty.")
                continue

            res = self.anki.add_note_fields(fields_dict, deck_name, model_name=model_name)
            if "error" in res and res["error"] is None:
                added += 1
            else:
                err_msg = res.get("error", "Unknown error")
                errors.append(f"Card {idx}: {err_msg}")

        if added > 0:
            messagebox.showinfo("Success", f"✅ {added} flashcards added to Anki deck '{deck_name}'.")
        if errors:
            messagebox.showwarning("Import Issues", "\n".join(errors))

    def run(self):
        """Start the application"""
        self.root.mainloop() 