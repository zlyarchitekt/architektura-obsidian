import os
import re
import shutil

src_root = "temp_pdf_out_34"
output_md = "RZUT-34-joined.md"
output_images = "RZUT-34-joined_images"
os.makedirs(output_images, exist_ok=True)

# Find all chunk directories: chunk_1_16, etc.
chunk_dirs = []
for d in os.listdir(src_root):
    if d.startswith("chunk_"):
        parts = d.split("_")
        if len(parts) >= 2 and parts[1].isdigit():
            chunk_dirs.append((int(parts[1]), os.path.join(src_root, d)))

# Sort by start page index
chunk_dirs.sort(key=lambda x: x[0])

all_lines = []

for start_idx, cdir in chunk_dirs:
    md_path = os.path.join(cdir, "RZUT34__PLEC-ayx8rw.md")
    img_dir = os.path.join(cdir, "RZUT34__PLEC-ayx8rw_images")
    
    if not os.path.exists(md_path):
        continue
        
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    # We must replace image links: "RZUT34__PLEC-ayx8rw_images/imageFile1.png"
    # and "temp_pdf_out_34/chunk.../RZUT34__PLEC-ayx8rw_images/imageFile1.png"
    # Actually wait, since it ran in chunk directory, opendataloader_pdf uses relative paths to the output dir.
    # So it will be just "RZUT34__PLEC-ayx8rw_images/imageFileX.png"
    
    def repl_img(m):
        old_path = m.group(1) # just "imageFileX.png"
        new_name = f"chunk{start_idx}_{old_path}"
        # Copy image file
        src_img = os.path.join(img_dir, old_path)
        dst_img = os.path.join(output_images, new_name)
        if os.path.exists(src_img):
            shutil.copy2(src_img, dst_img)
        return f"![image]({output_images}/{new_name})"

    text = re.sub(r'!\[.*?\]\(RZUT34__PLEC-ayx8rw_images/([^\)]+)\)', repl_img, text)
    
    all_lines.append(text)

with open(output_md, "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_lines))

print(f"Created {output_md}")
