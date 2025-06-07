import os
import h5py
import scipy.io as io
import PIL.Image as Image
import numpy as np
from matplotlib import pyplot as plt, cm as c
from scipy.ndimage.filters import gaussian_filter
import scipy
import torchvision.transforms.functional as F
import torch
from torchvision import transforms
from .csrnet_helper import CSRNet

# Load model once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CSRNet().to(device)
model.load_state_dict(torch.load(
    "assets/models/crowd_counting_vgg.pth", map_location=device))
model.eval()

# Transform for input
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])


def predict_count(image_path: str):
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(input_tensor)
        count = float(output.sum().item())
    return round(count, 2), output


def save_densitymap(map: np.ndarray, filename: str):
    density = map.squeeze().cpu().numpy()
    filename = f"densitymap_{filename}.jpg"
    path = os.path.join("uploads", filename)
    np.save(path, density)
    return density


def save_heatmap(map: np.ndarray, filename: str, count: float) -> str:
    filename = f"heatmap_{filename}.jpg"
    path = os.path.join("uploads", filename)
    plt.imshow(map, cmap='jet')
    plt.axis("off")
    plt.title(f"Count: {count:.2f}")
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.close()

    return path
