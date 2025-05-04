# Anki Importer

A simple tool to import flashcards into Anki using Anki Connect.

## Prerequisites

- Python 3.11 or higher
- Anki installed and running
- Anki Connect add-on installed and enabled in Anki

## Installation

1. Install Anki Connect:
   - Open Anki
   - Go to Tools > Add-ons > Get Add-ons
   - Enter the code 2055492159
   - Restart Anki

2. Install the Anki Importer:
```bash
pip install anki-importer
```

## Usage

1. Make sure Anki is running
2. Run the importer:
```bash
anki-importer
```

3. In the application:
   - Enter the deck name where you want to import the cards
   - Either paste your flashcards in the text box or import from a file
   - Click "Import from Text" or "Import from File"

## Flashcard Format

Your flashcards should be in the following format:
```
Question: Your question here
Answer: Your answer here

Question: Another question
Answer: Another answer
```

## Troubleshooting

If you encounter connection errors:
1. Make sure Anki is running
2. Verify that Anki Connect is installed and enabled
3. Check that Anki Connect is running on port 8765

## License

MIT License 