import requests

class AnkiConnect:
    def __init__(self, host="localhost", port=8765):
        self.base_url = f"http://{host}:{port}"
        
    def _request(self, action, **params):
        try:
            response = requests.post(
                self.base_url,
                json={
                    "action": action,
                    "version": 6,
                    "params": params
                },
                timeout=5
            )
            return response.json()
        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed"}
        except requests.exceptions.Timeout:
            return {"error": "Timeout"}
        except Exception as e:
            return {"error": str(e)}

    def check_connection(self):
        result = self._request("version")
        return result.get("error") is None

    def check_deck_exists(self, deck_name):
        result = self._request("deckNames")
        return deck_name in result.get("result", [])

    def create_deck(self, deck_name):
        result = self._request("createDeck", deck=deck_name)
        return result.get("error") is None

    def add_note(self, front, back, deck_name):
        result = self._request(
            "addNote",
            note={
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
        )
        return result 