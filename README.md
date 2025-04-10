# Color Palette Extractor & Analyzer


> Extract beautiful color palettes from any image. Perfect for designers, artists, web developers, and branding experts.

---

## Features

- 🎨 Extract dominant color palettes from an image
- 🧮 KMeans clustering with adjustable cluster count
- 📊 Visualize proportions of each color
- 📁 Batch mode for folders
- 🖼 Face vs background palette separation
- ✨ Export palettes in RGB, HEX, PNG, and JSON
- 🖱 Easy GUI (Tkinter)

---


## Demo

### Input Image:
![Input Image](sample.jpg)

### Generated Palette:
![Palette Output](sample_palette.png)

---

Functionality Overview

1. Color Palette Extraction

Extracts dominant colors from any image using KMeans clustering.

2. GUI Mode

A simple interface for selecting images and extracting palettes visually.


3. Batch Mode

Process multiple images at once from a folder.


4. Fac-Only Palette Extraction

Detects the face only using Haar Cascades and extracts dominant colors from that region:


Why use face-based palette extraction?

General image palettes often include irrelevant backgrounds.

Face palette isolates skin tones, hair, facial elements.

Crucial for:

Skin tone detection

Virtual makeup tools

Personalized fashion/design recommendations

Important:

Haar cascade works best on frontal face images.

Side-angle or poorly lit faces may fail.




