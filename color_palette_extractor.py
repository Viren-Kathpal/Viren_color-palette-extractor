import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import argparse
import os
import json
import imutils

def extract_colors(image_path, clusters=5, resize_height=200, save_palette=True, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Couldn't load image: {image_path}")
        return []

    original = img.copy()
    img = imutils.resize(img, height=resize_height)
    flat_img = img.reshape((-1, 3))

    kmeans = KMeans(n_clusters=clusters, random_state=42)
    kmeans.fit(flat_img)
    colors = np.array(kmeans.cluster_centers_, dtype='uint')
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    percentages = counts / flat_img.shape[0]

    sorted_colors = sorted(zip(percentages, colors), reverse=True)

    # Save bar & palette
    plot_color_bar(sorted_colors, output_dir, image_path)
    hex_colors = save_palette_data(sorted_colors, output_dir, image_path)

    return hex_colors

def plot_color_bar(p_and_c, output_dir, image_path):
    bar = np.ones((50, 500, 3), dtype='uint')
    start = 0
    for percent, color in p_and_c:
        end = start + int(percent * bar.shape[1])
        bar[:, start:end] = color[::-1]  # BGR to RGB
        start = end

    plt.figure(figsize=(10, 2))
    plt.imshow(bar)
    plt.axis('off')
    out_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_palette.png")
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()

def save_palette_data(p_and_c, output_dir, image_path):
    palette_data = []
    for percent, color in p_and_c:
        r, g, b = map(int, color)
        hex_code = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        palette_data.append({
            "rgb": [r, g, b],
            "hex": hex_code,
            "percentage": round(float(percent) * 100, 2)
        })

    out_json = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_colors.json")
    with open(out_json, 'w') as f:
        json.dump(palette_data, f, indent=4)
    return [color["hex"] for color in palette_data]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract dominant colors from an image")
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("--clusters", type=int, default=5, help="Number of dominant colors")
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()

    hex_colors = extract_colors(args.image, clusters=args.clusters, output_dir=args.output)
    if hex_colors:
        print("Dominant HEX Colors:", hex_colors)