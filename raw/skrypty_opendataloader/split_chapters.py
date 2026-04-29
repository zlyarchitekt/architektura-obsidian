import os
import re

input_file = "raw/Książki/Low-Rise, High-Density Housing_/Low-Rise, High-Density Housing_.md"
output_dir = "raw/Książki/Low-Rise, High-Density Housing_/parts"
os.makedirs(output_dir, exist_ok=True)

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

chapters = []
current_chapter = None
current_lines = []

for line in lines:
    # Match chapter headers like "# Chapter 1. Introduction" or "# Chapter 12. Bibliography"
    match = re.match(r'^# Chapter\s+(\d+)\.\s+(.*)$', line.strip())
    if match:
        if current_chapter is not None:
            chapters.append((current_chapter, current_lines))
        current_chapter = (int(match.group(1)), match.group(2).strip())
        current_lines = [line]
    else:
        if current_chapter is not None:
            current_lines.append(line)

if current_chapter is not None:
    chapters.append((current_chapter, current_lines))

for (num, title), chap_lines in chapters:
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    filename = f"Chapter_{num:02d}_{safe_title}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(chap_lines)
    print(f"Wrote {len(chap_lines)} lines to {filename}")

print(f"Done! Split into {len(chapters)} chapters.")
