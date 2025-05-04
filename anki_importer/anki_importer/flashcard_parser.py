import re

def extract_flashcards_multi(text, fields, field_map=None):
    """
    Extract flashcards with multiple fields from text.
    
    Args:
        text: Input text containing flashcards
        fields: List of Anki field names (e.g., ["Front", "Back", "Extras"])
        field_map: Dict mapping input field names to Anki field names (e.g., {"References": "Extras"})
    
    Returns:
        List of tuples containing field values in the order specified by fields
    """
    if field_map is None:
        field_map = {}
    
    # Normalize text
    text = text.replace('\r\n', '\n').replace('\r', '\n').strip()
    
    # Split into card blocks
    card_blocks = re.split(r'(?=^Front:)', text, flags=re.MULTILINE)
    cards = []
    
    for block in card_blocks:
        block = block.strip()
        if not block:
            continue
            
        card_dict = {field: "" for field in fields}
        current_field = None
        current_value = []
        
        for line in block.splitlines():
            line = line.strip()
            if not line:
                continue
                
            # Check for field name at start of line
            m = re.match(r'^([A-Za-z.]+):\s*(.*)', line)
            if m:
                # Save previous field if exists
                if current_field:
                    card_dict[current_field] = '\n'.join(current_value).strip()
                    current_value = []
                
                field_name, value = m.group(1).strip(), m.group(2).strip()
                current_field = _find_matching_field(field_name, fields, field_map)
                
                if current_field and value:
                    current_value.append(value)
            elif current_field:
                # Continue collecting value for current field
                current_value.append(line)
        
        # Save last field
        if current_field:
            card_dict[current_field] = '\n'.join(current_value).strip()
        
        # Add card if Front and Back are present
        if card_dict['Front'] and card_dict['Back']:
            cards.append(tuple(card_dict[f] for f in fields))
            
    return cards

def _find_matching_field(field_name, fields, field_map):
    """
    Find the matching Anki field name for the given input field name.
    
    Args:
        field_name: Input field name
        fields: List of Anki field names
        field_map: Dict mapping input field names to Anki field names
    
    Returns:
        Matching Anki field name or None if no match found
    """
    # Direct match
    if field_name in fields:
        return field_name
        
    # Mapped field
    mapped_field = field_map.get(field_name)
    if mapped_field and mapped_field in fields:
        return mapped_field
        
    # Case-insensitive match
    for f in fields:
        if field_name.lower().replace('.', '') == f.lower().replace('.', ''):
            return f
            
    return None