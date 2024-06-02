from fastapi import FastAPI, File, UploadFile
from PIL import Image
from ultralytics import YOLO
import easyocr
import numpy as np
from io import BytesIO

app = FastAPI()

model = YOLO('id_card_detector.pt')
reader = easyocr.Reader(['ro', 'en'])


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    results = model(image, imgsz=640, conf=0.5)
    response_data = []

    for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
        label = model.names[int(cls)]
        if label == 'Cards':
            crop_img = image.crop((int(box[0]), int(box[1]), int(box[2]), int(box[3])))
            text_results = reader.readtext(np.array(crop_img), detail=0)
            response_data.append({
                'label': label,
                'confidence': float(conf),
                'text': text_results
            })
    return response_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5036)
