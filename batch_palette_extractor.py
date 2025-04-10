import os
import argparse
from color_palette_extractor import extract_colors

def batch_process(folder_path, clusters=5):
    if not os.path.exists(folder_path):
        print(f"[ERROR] Folder does not exist: {folder_path}")
        return

    for file in os.listdir(folder_path):
        if file.startswith('.') or not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        full_path = os.path.join(folder_path, file)
        print(f"[INFO] Processing {file}...")
        try:
            hex_colors = extract_colors(full_path, clusters=clusters)
            if hex_colors:
                print(f"[SUCCESS] Colors: {hex_colors}\n")
            else:
                print(f"[WARNING] No colors extracted from {file}\n")
        except Exception as e:
            print(f"[ERROR] Failed to process {file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch process image folder for color palettes")
    parser.add_argument("folder", help="Folder with images")
    parser.add_argument("--clusters", type=int, default=5)
    args = parser.parse_args()

    batch_process(args.folder, args.clusters)