
from ultralytics import YOLOv10

class Detect():
    def __init__(self):
        self.model = YOLOv10('ModelVehicleDetect\\best.pt')
        
        
    def predict(self, image):
        return self.model(image, conf=0.3, iou=0.5, verbose=False)
    
    def calculate_weight(self, results):
        class_detections_values = []
        for k, v in self.model.names.items():
            class_detections_values.append(results[0].boxes.cls.tolist().count(k))
        # create dictionary of objects detected per class
        classes_detected = dict(zip(self.model.names.values(), class_detections_values))

        weight = (classes_detected['Bus']*3 + classes_detected['Car'] + classes_detected['Motor']*0.75 + classes_detected['Truck']*1.5)
        return weight
        