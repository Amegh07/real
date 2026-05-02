import re

with open(r'C:\Users\amegh\OneDrive\Desktop\real\backend\agents\agent.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print("Length:", len(content))

# Find section by searching for specific patterns
search_patterns = [
    "if self.is_sick:",
    "if self.is_married:",
    "Non-linear starvation panic",
    "self.age_ticks += 1"
]

for p in search_patterns:
    idx = content.find(p)
    if idx >= 0:
        print(f"Found '{p[:30]}...' at index {idx}")
    else:
        print(f"NOT FOUND: '{p}'")

# Let's check what's actually there by looking around line 309
lines = content.split('\n')
print("\nLines 309-335:")
for i in range(308, min(335, len(lines))):
    line = lines[i]
    # Show hex representation of first 50 chars
    hex_part = line[:50].encode('utf-8').hex() if len(line) > 0 else ""
    print(f"{i+1}: {hex_part} | {line[:60]}")