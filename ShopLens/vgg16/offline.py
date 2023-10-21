from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np

if __name__ == '__main__':
    fe = FeatureExtractor()

    for img_path in sorted(Path("./static/img").rglob("*.[jJ][pP][gG]")):
        if img_path.is_file():
            feature_path = Path("./static/feature") / (img_path.stem + ".npy")

            if not feature_path.exists():
                print(img_path)
                feature = fe.extract(img=Image.open(img_path))
                np.save(feature_path, feature)
            else:
                print(f"Skipping {img_path} - Feature file already exists")

