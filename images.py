import os
import re
import shutil
from urllib.parse import quote

# Paths - FIXED for your setup
posts_dir = "/var/home/deck/Documents/Vault/posts/"
attachments_dir = "/var/home/deck/Documents/Vault/attachments/"
static_images_dir = "/home/deck/Documents/techno/static/images/"

# Create static dir if missing
os.makedirs(static_images_dir, exist_ok=True)

# Process each markdown file
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r") as file:
            content = file.read()

        # Find Obsidian images: ![[image.png]]
        images = re.findall(r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|webp))\]\]', content, re.IGNORECASE)

        for image in images:
            # Clean filename (remove %20 → spaces → re-encode)
            clean_name = image.replace('%20', ' ')

            # Hugo Markdown link: ![alt](/static/images/image.png)
            hugo_link = f"![{clean_name}](/static/images/{quote(clean_name)})"

            # Replace in content
            content = content.replace(f"![[{image}]]", hugo_link)

            # Copy image file
            source_path = os.path.join(attachments_dir, image)
            if os.path.exists(source_path):
                dest_path = os.path.join(static_images_dir, clean_name)
                shutil.copy2(source_path, dest_path)
                print(f"Copied: {image} → static/images/{clean_name}")

        # Save updated post
        with open(filepath, "w") as file:
            file.write(content)

print("✅ Images processed! Check static/images/")
