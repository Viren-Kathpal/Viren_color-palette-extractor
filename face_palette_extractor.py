import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import sys

def extract_face_palette(image_path, clusters=5, output_dir="output_faces"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load Haar Cascade
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    if face_cascade.empty():
        print("Error loading Haar Cascade.")
        return

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image: {image_path}")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        print("No face detected in", image_path)
        return

    (x, y, w, h) = faces[0]
    face_img = image[y:y+h, x:x+w]
    face_resized = cv2.resize(face_img, (200, 200))
    flat_face = face_resized.reshape((-1, 3))

    # KMeans clustering
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(flat_face)
    colors = kmeans.cluster_centers_
    percentages = np.bincount(kmeans.labels_) / len(kmeans.labels_)

    # Save cropped face
    face_filename = os.path.splitext(os.path.basename(image_path))[0] + "_face.jpg"
    cv2.imwrite(os.path.join(output_dir, face_filename), face_img)

    # Save color palette bar
    save_palette_bar(colors, percentages, image_path, output_dir)

def save_palette_bar(colors, percentages, image_path, output_dir):
    bar = np.zeros((50, 500, 3), dtype='uint8')
    start = 0

    for color, percent in zip(colors, percentages):
        end = start + int(percent * bar.shape[1])
        bar[:, start:end] = color[::-1]  # BGR to RGB for matplotlib display
        start = end

    plt.figure(figsize=(8, 2))
    plt.imshow(bar)
    plt.axis("off")
    bar_filename = os.path.splitext(os.path.basename(image_path))[0] + "_palette.png"
    plt.savefig(os.path.join(output_dir, bar_filename), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python face_palette_extractor.py <path_to_image>")
    else:
        extract_face_palette(sys.argv[1])