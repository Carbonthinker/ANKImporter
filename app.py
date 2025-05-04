import re
import json
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# ==== ANKI CONNECT FUNCTION ====
def check_anki_connection():
    try:
        result = requests.post('http://localhost:8765', json={
            "action": "version",
            "version": 6
        }, timeout=5).json()
        return result.get("error") is None
    except:
        return False

def check_deck_exists(deck_name):
    try:
        result = requests.post('http://localhost:8765', json={
            "action": "deckNames",
            "version": 6
        }, timeout=5).json()
        return deck_name in result.get("result", [])
    except:
        return False

def create_deck(deck_name):
    try:
        result = requests.post('http://localhost:8765', json={
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": deck_name
            }
        }, timeout=5).json()
        return result.get("error") is None
    except:
        return False

def add_note_to_anki(front, back, deck_name):
    try:
        result = requests.post('http://localhost:8765', json={
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front.strip(),
                        "Back": back.strip()
                    },
                    "options": {
                        "allowDuplicate": False
                    },
                    "tags": ["auto_imported"]
                }
            }
        }, timeout=5).json()
        return result
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed"}
    except requests.exceptions.Timeout:
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)}

# ==== FLASHCARD EXTRACTION ====
def extract_flashcards(text):
    return re.findall(r"Question:\s*(.*?)\s*Answer:\s*(.*?)(?:\n|$)", text, re.DOTALL)

# ==== TEXT IMPORT FUNCTION ====
def import_from_text():
    if not check_anki_connection():
        messagebox.showerror("Error", "Could not connect to Anki. Please make sure:\n1. Anki is running\n2. Anki Connect is installed and enabled\n3. Anki Connect is running on port 8765")
        return

    text = text_box.get("1.0", tk.END)
    deck_name = deck_entry.get().strip()
    
    if not deck_name:
        messagebox.showerror("Error", "Please enter a deck name.")
        return
        
    flashcards = extract_flashcards(text)
    if not flashcards:
        messagebox.showerror("Error", "No flashcards found. Check the format of your text.")
        return

    # Check if deck exists, if not create it
    if not check_deck_exists(deck_name):
        if not create_deck(deck_name):
            messagebox.showerror("Error", f"Could not create deck '{deck_name}'. Please check Anki and try again.")
            return

    added = 0
    errors = 0
    for q, a in flashcards:
        res = add_note_to_anki(q, a, deck_name)
        if "error" in res and res["error"] is None:
            added += 1
        else:
            errors += 1
            print(f"⚠️ Error adding card: {res}")

    if added > 0:
        messagebox.showinfo("Success", f"✅ {added} flashcards added to Anki deck '{deck_name}'.")
    if errors > 0:
        messagebox.showwarning("Partial Success", f"⚠️ {errors} cards could not be added. Check the console for details.")

# ==== MAIN FUNCTION ====
def import_flashcards():
    if not check_anki_connection():
        messagebox.showerror("Error", "Could not connect to Anki. Please make sure:\n1. Anki is running\n2. Anki Connect is installed and enabled\n3. Anki Connect is running on port 8765")
        return

    file_path = filedialog.askopenfilename(
        title="Select flashcards.txt",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if not file_path:
        return

    deck_name = deck_entry.get().strip()
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

    # Check if deck exists, if not create it
    if not check_deck_exists(deck_name):
        if not create_deck(deck_name):
            messagebox.showerror("Error", f"Could not create deck '{deck_name}'. Please check Anki and try again.")
            return

    added = 0
    errors = 0
    for q, a in flashcards:
        res = add_note_to_anki(q, a, deck_name)
        if "error" in res and res["error"] is None:
            added += 1
        else:
            errors += 1
            print(f"⚠️ Error adding card: {res}")

    if added > 0:
        messagebox.showinfo("Success", f"✅ {added} flashcards added to Anki deck '{deck_name}'.")
    if errors > 0:
        messagebox.showwarning("Partial Success", f"⚠️ {errors} cards could not be added. Check the console for details.")

# ==== GUI SETUP ====
root = tk.Tk()
root.title("Flashcard Importer to Anki")

# Create main frame
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Deck name entry
tk.Label(main_frame, text="Anki Deck Name:").pack(pady=5)
deck_entry = tk.Entry(main_frame, width=40)
deck_entry.pack(pady=5)
deck_entry.insert(0, "ChatGPT Imported Cards")

# Text input area
tk.Label(main_frame, text="Paste your flashcards here:").pack(pady=5)
text_box = scrolledtext.ScrolledText(main_frame, width=50, height=10)
text_box.pack(pady=5)

# Buttons frame
buttons_frame = tk.Frame(main_frame)
buttons_frame.pack(pady=10)

# Import buttons
tk.Button(buttons_frame, text="Import from Text", command=import_from_text).pack(side=tk.LEFT, padx=5)
tk.Button(buttons_frame, text="Import from File", command=import_flashcards).pack(side=tk.LEFT, padx=5)

root.mainloop()