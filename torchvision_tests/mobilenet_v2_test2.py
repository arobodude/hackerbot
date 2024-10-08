import os
import ast
import time

import torch
import numpy as np
from torchvision import models, transforms

import cv2
from PIL import Image
#import requests

torch.backends.quantized.engine = 'qnnpack'

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 36)

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v3_large(pretrained=True, quantize=True)
# jit model to take it from ~20fps to ~30fps
net = torch.jit.script(net)

started = time.time()
last_logged = time.time()
frame_count = 0

with open('imagenet1000_clsidx_to_labels.txt') as f:
    classes = ast.literal_eval(f.read()) 

fps = 0.0

with torch.no_grad():
    while True:
        # Read frame
        ret, image = cap.read()
        if not ret:
            raise RuntimeError("failed to read frame")

        # Convert opencv output from BGR to RGB
        image = image[:, :, [2, 1, 0]]
        permuted = image

        # Preprocess
        input_tensor = preprocess(image)

        # Create a mini-batch as expected by the model
        input_batch = input_tensor.unsqueeze(0)

        # Run model
        output = net(input_batch)
        # do something with output ...

        # Clear the screen to print updated results
        # os.system('clear')

        # Log model performance and print the current fps
        frame_count += 1
        now = time.time()
        if now - last_logged > 1:
            fps = f"{frame_count / (now-last_logged)} fps"
            print(fps)
            last_logged = now
            frame_count = 0
        else:
            print(fps)

        # Print top 10 classes
        top = list(enumerate(output[0].softmax(dim=0)))
        top.sort(key=lambda x: x[1], reverse=True)
        os.system('clear')
        for idx, val in top[:10]:
            print(f"{val.item()*100:.2f}% {classes[idx]}")
