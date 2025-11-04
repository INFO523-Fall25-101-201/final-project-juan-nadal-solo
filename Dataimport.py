import kagglehub
import shutil
import os
from pathlib import Path

# Define the target data folder
DATA_FOLDER = Path("data/raw")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

# List of datasets to download
datasets = [
    "alanvourch/tmdb-movies-daily-updates",
    "rounakbanik/the-movies-dataset",
    "asaniczka/tmdb-movies-dataset-2023-930k-movies"
]

print("Starting dataset downloads...\n")

for dataset in datasets:
    print(f"Downloading: {dataset}")
    try:
        # Download the dataset
        path = kagglehub.dataset_download(dataset)
        print(f"Downloaded to: {path}")

        # Create a subfolder for this dataset
        dataset_name = dataset.split("/")[1]
        target_folder = DATA_FOLDER / dataset_name

        # Copy files to data folder
        if os.path.exists(path):
            if target_folder.exists():
                shutil.rmtree(target_folder)
            shutil.copytree(path, target_folder)
            print(f"Copied to: {target_folder}")

        print(f"Successfully processed {dataset}\n")

    except Exception as e:
        print(f"Error downloading {dataset}: {str(e)}\n")

print("All downloads complete!")
