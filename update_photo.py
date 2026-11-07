"""
Photo & Avatar Updater for GitHub Profile
------------------------------------------
Usage:
  python update_photo.py [path_to_image]

Examples:
  python update_photo.py my_headshot.png
  python update_photo.py my_cutout.png

If no file argument is provided, it looks for 'photo.png' in the current folder.
This script automatically resizes the image and embeds it into:
  - assets/hero.svg
  - assets/about-life.svg
  - assets/id-dashboard.svg
  - assets/connect.svg
"""

import sys
import os
import re
import base64
from PIL import Image

def update_photos(image_path="photo.png"):
    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' not found!")
        print("Please provide an image path: python update_photo.py your_photo.png")
        return

    print(f"Loading '{image_path}'...")
    src_img = Image.open(image_path).convert("RGBA")

    # Target 1: 461 x 541 (Hero, About, ID Badge)
    target1 = Image.new("RGBA", (461, 541), (0, 0, 0, 0))
    scale1 = min(461 / src_img.width, 541 / src_img.height)
    w1, h1 = int(src_img.width * scale1), int(src_img.height * scale1)
    resized1 = src_img.resize((w1, h1), Image.Resampling.LANCZOS)
    target1.paste(resized1, ((461 - w1) // 2, (541 - h1) // 2), resized1)

    import io
    buf1 = io.BytesIO()
    target1.save(buf1, format="PNG")
    b64_461 = base64.b64encode(buf1.getvalue()).decode("ascii")

    # Target 2: 408 x 612 (Connect Card)
    target2 = Image.new("RGBA", (408, 612), (0, 0, 0, 0))
    scale2 = min(408 / src_img.width, 612 / src_img.height)
    w2, h2 = int(src_img.width * scale2), int(src_img.height * scale2)
    resized2 = src_img.resize((w2, h2), Image.Resampling.LANCZOS)
    target2.paste(resized2, ((408 - w2) // 2, (612 - h2) // 2), resized2)

    buf2 = io.BytesIO()
    target2.save(buf2, format="PNG")
    b64_408 = base64.b64encode(buf2.getvalue()).decode("ascii")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")

    # Update SVGs
    for fname in ["hero.svg", "about-life.svg", "id-dashboard.svg"]:
        fpath = os.path.join(assets_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            content = re.sub(r'href="data:image/png;base64,[^"]+"', f'href="data:image/png;base64,{b64_461}"', content, count=1)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {fname}!")

    connect_path = os.path.join(assets_dir, "connect.svg")
    if os.path.exists(connect_path):
        with open(connect_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'href="data:image/png;base64,[^"]+"', f'href="data:image/png;base64,{b64_408}"', content, count=1)
        with open(connect_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated connect.svg!")

    # Bump version in README.md to bust GitHub image cache
    readme_path = os.path.join(base_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme = f.read()
        # Find current version
        m = re.search(r'\?v=(\d+)', readme)
        if m:
            curr_v = int(m.group(1))
            new_v = curr_v + 1
            readme = re.sub(r'\?v=\d+', f'?v={new_v}', readme)
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(readme)
            print(f"Bumped cache version in README.md to v={new_v}!")

    print("\nAll done! Push the updated files to your GitHub profile repository.")

if __name__ == "__main__":
    img = sys.argv[1] if len(sys.argv) > 1 else "photo.png"
    update_photos(img)
