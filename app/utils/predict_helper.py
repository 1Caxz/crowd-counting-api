import uuid
import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
from PIL import Image
from .csrnet_helper import CSRNet

# Load model once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CSRNet().to(device)
model.load_state_dict(torch.load("assets/models/crowd_counting_csrnet_vgg.pt", map_location=device))
model.eval()

# Transform for input
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

def predict_count(image_path: str):
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(input_tensor)[0, 0].cpu().numpy()
        count = float(np.sum(output))
    return count, output

def save_heatmap(heatmap: np.ndarray, filename: str) -> str:
    filename = f"heatmap_{uuid.uuid4().hex[:8]}.jpg"
    path = os.path.join("uploads", filename)

    plt.imshow(heatmap, cmap='jet')
    plt.axis("off")
    plt.savefig(path, bbox_inches='tight', pad_inches=0)
    plt.close()

    return path