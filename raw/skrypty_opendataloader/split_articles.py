import os
import re
import shutil

titles = [
    'W S T Ę P N I A K',
    'WA RSZ AWA PR Z YSZ ŁOŚ CI B Ę DZ I E WA RSZ AWĄ N A SZ YCH M A R Z E Ń',
    'R A M Y   ROZ WOJ U',
    'R A M Y ROZ WOJ U',
    'RÓW N O U PR AW N I E N I E   WSZ YS T K I CH   U CZ E S T N I KÓW   RU CH U',
    'RÓW N O U PR AW N I E N I E WSZ YS T K I CH U CZ E S T N I KÓW RU CH U',
    'M I A S TO   JA KO   E KOS YS T E M',
    'M I A S TO JA KO E KOS YS T E M',
    'M Ą D R E   D O G Ę SZCZ A N I E',
    'M Ą D R E D O G Ę SZCZ A N I E',
    'S P O Ł ECZ N A   W R A Ż L I WOŚ Ć',
    'S P O Ł ECZ N A W R A Ż L I WOŚ Ć',
    'WYCHODZENIE ZA RÓG',
    'SKŁĘBIONE PROBLEMY PUSTOSTANÓW',
    'PLAN SHARONA',
    'FUNERALNE PLANOWANIE',
    'P O D M I E J S K I E   B I O G R A F I E',
    'P O D M I E J S K I E B I O G R A F I E'
]

# We need a robust matcher
def is_new_article(line):
    clean = re.sub(r'^#+\s*', '', line).strip()
    # Normalize spaces for matching
    clean_norm = re.sub(r'\s+', ' ', clean)
    for t in titles:
        if clean_norm == re.sub(r'\s+', ' ', t):
            return True, clean_norm
    return False, None

def safe_filename(name):
    # remove spaces and special characters, make camelCase or just snake_case
    name = name.replace(' ', '')
    name = re.sub(r'[^A-Za-z0-9ĄĆĘŁŃÓŚŹŻąćęłńóśźż]+', '_', name)
    if name.startswith('_'): name = name[1:]
    return name[:50] + '.md'

output_dir = 'RZUT-33'
img_out_dir = os.path.join(output_dir, 'images')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(img_out_dir):
    os.makedirs(img_out_dir)

with open('temp_pdf_out/RZUT-33-PLANOWANIE-b0mjya.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_file = None
current_content = []
file_index = 1
current_filename = '00_Poczatek.md'

image_pattern = re.compile(r'!\[.*?\]\((temp_pdf_out/)?RZUT-33-PLANOWANIE-b0mjya_images/(.*?)\)')
alt_image_pattern = re.compile(r'!\[.*?\]\(RZUT-33-PLANOWANIE-b0mjya_images/(.*?)\)')

def save_current():
    global current_filename, current_content
    if current_content:
        path = os.path.join(output_dir, current_filename)
        with open(path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(current_content)

for line in lines:
    is_art, title = is_new_article(line)
    if is_art:
        save_current()
        current_filename = f"{file_index:02d}_{safe_filename(title)}"
        file_index += 1
        current_content = []
    
    # Check for images and copy them
    matches = alt_image_pattern.finditer(line)
    for m in matches:
        img_name = m.group(1)
        src_img = os.path.join('temp_pdf_out', 'RZUT-33-PLANOWANIE-b0mjya_images', img_name)
        dst_img = os.path.join(img_out_dir, img_name)
        if os.path.exists(src_img):
            shutil.copy2(src_img, dst_img)
    
    # Update image links in markdown
    line = alt_image_pattern.sub(r'![image](images/\1)', line)
    
    current_content.append(line)

save_current()
print("Done splitting.")
