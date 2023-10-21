from pathlib import Path

if __name__ == '__main__':
    feature_dir = Path("./static/feature")

    for feature_file in feature_dir.glob("*.npy"):
        feature_file.unlink()

    print("Data in the model has been reset.")

