import torch
from torchvision import models, transforms
from PIL import Image

class FighterJetClassifier:
    def __init__(self, model_path, confidence_threshold=0.5):
        self.model = models.efficientnet_b4(pretrained=False)
        num_ftrs = self.model.classifier[1].in_features
        self.model.classifier[1] = torch.nn.Linear(num_ftrs, 2)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.confidence_threshold = confidence_threshold

    def classify_image(self, image_path):
        img = Image.open(image_path)
        img_tensor = self.transform(img).unsqueeze(0)
        outputs = self.model(img_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        max_probability, predicted = torch.max(probabilities, 1)
        
        if max_probability.item() >= self.confidence_threshold:
            predicted_class = 'Sukhoi' if predicted.item() == 0 else 'Tejas'
            print("Detected aircraft:", predicted_class)
            return predicted_class
        else:
            print("No aircraft detected")
            return "No aircraft detected"