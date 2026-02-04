import os
import re
import shutil
from urllib.parse import quote

# Paths
posts_dir = "/var/home/deck/Documents/Vault/posts/"
attachments_dir = "/var/home/deck/Documents/Vault/static/images/"
static_images_dir = "/home/deck/Documents/techno/static/images/"

# Create static dir
os.makedirs(static_images_dir, exist_ok=True)

# Process each post
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "r") as file:
            content = file.read()

        # Find Obsidian images: ![[gobo.jpg]]
        images = re.findall(r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|webp))\]\]', content, re.IGNORECASE)

        for image in images:
            clean_name = image.replace('%20', ' ')
            hugo_link = f"![{clean_name}](/images/{quote(clean_name)})"

            content = content.replace(f"![[{image}]]", hugo_link)

            # Copy image
            source_path = os.path.join(attachments_dir, image)
            if os.path.exists(source_path):
                dest_path = os.path.join(static_images_dir, clean_name)
                shutil.copy2(source_path, dest_path)
                print(f"Copied: {image}")

        # Save post
        with open(filepath, "w") as file:
            file.write(content)

print("✅ Images fixed!")
