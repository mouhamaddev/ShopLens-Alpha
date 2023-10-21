import os
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path

app = Flask(__name__)

# Read image features and paths
fe = FeatureExtractor()
features = []
img_paths = []

def process_images_in_folder(folder_path):
    for folder_name, _, file_names in os.walk(folder_path):
        for file_name in file_names:
            img_path = os.path.join(folder_name, file_name)
            img_paths.append(img_path)
            img = Image.open(img_path)  # PIL image
            print("Processing image:", img_path)  # Display the image path being processed
            features.append(fe.extract(img))

img_folder = "./static/img"
process_images_in_folder(img_folder)
features = np.array(features)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results

        scores = []  # Initialize an empty list to hold the results
        for id in ids:
            dist = dists[id]
            img_path = img_paths[id]
            scores.append((dist, img_path))

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')

