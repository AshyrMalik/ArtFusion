from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import torch
from torchvision import transforms, models
from PIL import Image
import io
import base64
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Device Setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load VGG19 Model
vggnet = models.vgg19(pretrained=True).features.to(device).eval()

# Define image transformations (matching original pipeline)
transform_pipeline = transforms.Compose([
    transforms.Resize((800, 600)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Denormalization for output
def denormalize(tensor):
    mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).to(device)
    std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).to(device)
    return tensor * std + mean

# Function to Extract Feature Maps
def getFeatureMapActs(img, net):
    featuremaps = []
    featurenames = []
    convLayerIdx = 0
    # Iterate directly over the layers in the Sequential container
    for layer in net:
        img = layer(img)
        if isinstance(layer, torch.nn.Conv2d):
            featuremaps.append(img)
            featurenames.append('ConvLayer_' + str(convLayerIdx))
            convLayerIdx += 1
    return featuremaps, featurenames


# Function to Compute Gram Matrix
def gram_matrix(M):
    _, chans, height, width = M.shape
    M = M.view(chans, height * width)
    return torch.mm(M, M.t()) / (chans * height * width)

# Style Transfer Function
def run_style_transfer(content_img, style_img, net, device='cpu'):
    # Compute feature maps for content and style images once
    contentFeatureMaps, contentFeatureNames = getFeatureMapActs(content_img, net)
    styleFeatureMaps, styleFeatureNames = getFeatureMapActs(style_img, net)

    # Detach these tensors so they won't be part of the backward graph
    contentFeatureMaps = [fmap.detach() for fmap in contentFeatureMaps]
    styleFeatureMaps = [fmap.detach() for fmap in styleFeatureMaps]

    layers4content = ['ConvLayer_1', 'ConvLayer_4']
    layers4style = ['ConvLayer_1', 'ConvLayer_2', 'ConvLayer_3', 'ConvLayer_4', 'ConvLayer_5']
    weights4style = [1, 0.5, 0.5, 0.2, 0.1]

    # Initialize target image from the content image
    target = content_img.clone()
    target.requires_grad = True
    target = target.to(device)

    styleScaling = 1e6
    numepochs = 3500
    optimizer = torch.optim.RMSprop([target], lr=0.005)

    for epoch in range(numepochs):
        targetFeatureMaps, targetFeatureNames = getFeatureMapActs(target, net)
        styleLoss, contentLoss = 0, 0

        for layeri in range(len(targetFeatureNames)):
            if targetFeatureNames[layeri] in layers4content:
                contentLoss += torch.mean((targetFeatureMaps[layeri] - contentFeatureMaps[layeri]) ** 2)
            if targetFeatureNames[layeri] in layers4style:
                Gtarget = gram_matrix(targetFeatureMaps[layeri])
                Gstyle = gram_matrix(styleFeatureMaps[layeri])
                styleLoss += torch.mean((Gtarget - Gstyle) ** 2) * weights4style[layers4style.index(targetFeatureNames[layeri])]
        combiloss = styleScaling * styleLoss + contentLoss
        optimizer.zero_grad()
        combiloss.backward()
        optimizer.step()
        print(f"Epoch {epoch} loss: {combiloss.item()}")

    return target

# Transform Image Function
def transform_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform_pipeline(image).unsqueeze(0)

# Initialize FastAPI App
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI Style Transfer Endpoint
@app.post("/style-transfer")
@app.post("/style-transfer")
async def style_transfer(image: UploadFile = File(...), style: UploadFile = File(...)):
    try:
        content_bytes = await image.read()
        style_bytes = await style.read()

        content_img = transform_image(content_bytes).to(device)
        style_img = transform_image(style_bytes).to(device)

        print("Content image shape:", content_img.shape)
        print("Style image shape:", style_img.shape)

        # Run style transfer
        stylized_tensor = run_style_transfer(content_img, style_img, vggnet, device)
        print("Style transfer complete. Tensor shape:", stylized_tensor.shape)

        # Denormalize before converting back to an image
        output_tensor = denormalize(stylized_tensor).clamp(0, 1)
        output_image = transforms.ToPILImage()(output_tensor.squeeze().cpu().detach())

        buffered = io.BytesIO()
        output_image.save(buffered, format="JPEG")
        encoded_image = base64.b64encode(buffered.getvalue()).decode()

        print("Image encoding complete")
        return JSONResponse(content={"stylized_image": encoded_image})

    except Exception as e:
        # Print the full stack trace to the console
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Run Server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
