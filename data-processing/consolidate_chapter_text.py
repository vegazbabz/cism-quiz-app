import json
from pathlib import Path

# Load the chapter overviews JSON
input_file = Path('../chapter_overviews.json')
output_file = Path('../chapter_overviews.json')

with open(input_file, 'r', encoding='utf-8') as f:
    chapters = json.load(f)

# Process each chapter
for chapter in chapters:
    if 'overview' not in chapter or not isinstance(chapter['overview'], list):
        continue
    
    new_overview = []
    current_paragraph = []
    
    for line in chapter['overview']:
        stripped = line.strip()
        
        # If it's a bullet point, flush current paragraph and add bullet
        if stripped.startswith('- '):
            if current_paragraph:
                new_overview.append(' '.join(current_paragraph))
                current_paragraph = []
            new_overview.append(stripped)
        else:
            # It's regular text - add to current paragraph
            current_paragraph.append(stripped)
    
    # Don't forget the last paragraph
    if current_paragraph:
        new_overview.append(' '.join(current_paragraph))
    
    chapter['overview'] = new_overview

# Write back with nice formatting
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(chapters, f, indent=2, ensure_ascii=False)

print(f"✓ Consolidated chapter overviews written to {output_file}")
