from fastapi import FastAPI, File, UploadFile
from PIL import Image
from ultralytics import YOLO
import easyocr
import numpy as np
from io import BytesIO
import uvicorn

app = FastAPI()

model = YOLO('./models/id_card_detector.pt')
reader = easyocr.Reader(['ro', 'en'])


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read()))
    results = model(image, imgsz=640, conf=0.5)

    response_data = []
    boxes = results[0].boxes.xyxy.cpu().tolist()
    clss = results[0].boxes.cls.cpu().tolist()

    if boxes is not None:
        for box, cls in zip(boxes, clss):
            label = model.names[int(cls)]
            if label == 'Cards':
                crop_img = image.crop((int(box[0]), int(box[1]), int(box[2]), int(box[3])))
                text_results = reader.readtext(np.array(crop_img))
                text_results_formatted = [
                    {
                        'bound_box': [[int(point[0]), int(point[1])] for point in bound_box],
                        'text': text,
                        'confidence': float(conf)
                    } for bound_box, text, conf in text_results
                ]
                response_data.append({
                    'label': label,
                    'results': text_results_formatted
                })

    return response_data

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5036)
