import re

def clean_log():
    try:
        with open('conversation.log', 'rb') as f:
            raw = f.read()
        
        # We handle the file as a sequence of bytes.
        # We try to find the start of the UTF-16LE mess.
        # It's characterized by null bytes.
        
        if b'\x00' not in raw:
            print("No null bytes found.")
            return

        # Let's try a heuristic: 
        # Scan through the bytes. If we see a null byte, try to decode that region as UTF-16LE.
        # Actually, let's just use a regex to find blocks of (char + \x00)
        
        # This is a bit risky. Let's try a simpler way:
        # Split the file into "Valid UTF-8" and "The rest".
        
        parts = []
        current_pos = 0
        
        while current_pos < len(raw):
            # Try to find the next null byte
            next_null = raw.find(b'\x00', current_pos)
            if next_null == -1:
                # Rest is UTF-8
                parts.append(raw[current_pos:].decode('utf-8', errors='ignore'))
                break
            
            # Found a null byte. This is likely the start of a UTF-16LE segment.
            # But wait, it might be in the middle of a segment.
            # Let's find the start of this line.
            line_start = raw.rfind(b'\n', current_pos, next_null)
            if line_start == -1: line_start = current_pos
            else: line_start += 1
            
            # Text before the line_start is UTF-8
            if line_start > current_pos:
                parts.append(raw[current_pos:line_start].decode('utf-8', errors='ignore'))
            
            # Now we have the start of the "corrupted" block.
            # We need to find where it ends.
            # It ends when we stop seeing null bytes for a while.
            # Or just find the next UTF-8 valid block?
            # Actually, PowerShell appends the WHOLE rest in UTF-16LE until the next python append.
            
            # Find the first valid UTF-8 block AFTER this.
            # A valid UTF-8 block is something that has NO null bytes and is not UTF-16LE.
            # But wait, my python appends were UTF-8.
            
            # Let's find the next sequence of characters that DON'T have null bytes.
            next_utf8_start = -1
            search_pos = next_null
            while search_pos < len(raw) - 2:
                # If we see TWO consecutive bytes that are NOT null, and the next one is NOT null
                if raw[search_pos] != 0 and raw[search_pos+1] != 0:
                     # Check if it marks the end of the null-byte-land
                     # Let's check the next 10 bytes. If none are null, it's UTF-8.
                     if b'\x00' not in raw[search_pos : search_pos+20]:
                         next_utf8_start = search_pos
                         break
                search_pos += 1
            
            if next_utf8_start == -1:
                # Rest of file is UTF-16LE
                parts.append(raw[line_start:].decode('utf-16le', errors='ignore'))
                break
            else:
                # This segment is UTF-16LE
                parts.append(raw[line_start:next_utf8_start].decode('utf-16le', errors='ignore'))
                current_pos = next_utf8_start

        final_text = "".join(parts).replace('\r\n', '\n')
        
        with open('conversation.log', 'w', encoding='utf-8') as f:
            f.write(final_text)
        print("Cleaned!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_log()
