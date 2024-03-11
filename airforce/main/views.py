from django.http import JsonResponse
from .models import ImageModel
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import torch
from torchvision import transforms
from .model_inference import FighterJetClassifier
from .models import ImageModel
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        image = ImageModel.objects.create(image=file)
        return JsonResponse({'image_url': image.image.url})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def latest_image(request):
    latest_image = ImageModel.objects.last()
    if latest_image:
        return JsonResponse({'image_url': latest_image.image.url})
    else:
        return JsonResponse({'error': 'No images uploaded yet'}, status=404)
    

# Path to the model file
model_path = 'best_fighter_jet_classifier.pth'

# Create an instance of the classifier
classifier = FighterJetClassifier(model_path)

@csrf_exempt
def classify_image(request):
    if request.method == 'POST':
        file = request.FILES['file']

        image = ImageModel.objects.create(image=file)
        image_url = request.build_absolute_uri(image.image.url)  # Get the absolute URL of the saved image
        # Classify the image
        predicted_class = classifier.classify_image(file)
        return JsonResponse({'image_url': image_url, 'predicted_class': predicted_class})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
        