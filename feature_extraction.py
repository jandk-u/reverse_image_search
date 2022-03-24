# Extract feature from image
from torch import nn
from torchvision import models
from PIL import Image
from torchvision import transforms
from torch import linalg as LA


class FeatureExtraction(nn.Module):
    def __init__(self):
        super(FeatureExtraction, self).__init__()
        self.vgg = models.vgg16(pretrained=True)
        self.vgg.classifier = self.vgg.classifier[:-1]
        for param in self.vgg.parameters():
            param.requires_grad = False
        self.vgg.eval()
        self.transform = transforms.Compose(
            [
                transforms.Resize(224),
                transforms.ToTensor(),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
            ]
        )

    def extract(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image = self.transform(image).unsqueeze(0)
        feature = self.vgg(image)
        feature = feature / LA.norm(feature)
        return feature.tolist()
