import os
import re
import shutil

output_dir = 'RZUT-34'
img_out_dir = os.path.join(output_dir, 'images')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(img_out_dir):
    os.makedirs(img_out_dir)

# Clear existing files in RZUT-34 to be safe
for f in os.listdir(output_dir):
    p = os.path.join(output_dir, f)
    if os.path.isfile(p):
        os.remove(p)

with open('temp_pdf_out_34_fast/RZUT34__PLEC-ayx8rw.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean up spacing FIRST on the whole text
text = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', text)
text = re.sub(r'([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)-\s*\n+([a-ząćęłńóśźżA-ZĄĆĘŁŃÓŚŹŻ]+)', r'\1\2', text)
text = re.sub(r'([a-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ,])\n+([a-ząćęłńóśźż])', r'\1 \2', text)
text = text.replace('P Ł E Ć', 'PŁEĆ')
text = text.replace('A U T O R K I', 'AUTORKI')

# 2. Split into articles based on heading '# ' or '## '
lines = text.split('\n')

def safe_filename(name):
    name = re.sub(r'[^A-Za-z0-9ĄĆĘŁŃÓŚŹŻąćęłńóśźż]+', '_', name.strip())
    if name.startswith('_'): name = name[1:]
    return name[:50] + '.md'

current_filename = '00_Poczatek.md'
current_content = []
file_index = 1

alt_image_pattern = re.compile(r'!\[.*?\]\([^)]+\)')

def save_current():
    global current_filename, current_content
    if current_content:
        path = os.path.join(output_dir, current_filename)
        with open(path, 'w', encoding='utf-8') as out_f:
            out_f.write('\n'.join(current_content))

for line in lines:
    # A new article if it's a heading 1 or 2, and the text is mostly uppercase
    if re.match(r'^#{1,2}\s', line):
        title_text = re.sub(r'^#{1,2}\s*', '', line).strip()
        if len(title_text) > 4: # arbitrary logic to split logically
            save_current()
            current_filename = f"{file_index:02d}_{safe_filename(title_text)}"
            file_index += 1
            current_content = []
    
    current_content.append(line)

save_current()

# 3. Copy images if any exist in fast mode
fast_img_dir = 'temp_pdf_out_34_fast/RZUT34__PLEC-ayx8rw_images'
if os.path.exists(fast_img_dir):
    for f in os.listdir(fast_img_dir):
        shutil.copy2(os.path.join(fast_img_dir, f), os.path.join(img_out_dir, f))

print("Split and clean complete!")
