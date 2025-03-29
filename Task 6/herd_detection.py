import cv2
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import folium

net = cv2.dnn.readNet(
    r"C:\Users\321 Pillay\Desktop\Task 6\yolov3.weights",
    r"C:\Users\321 Pillay\Desktop\Task 6\yolov3.cfg"
)

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
with open("animal.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

current_location = (28.4199, 70.3034)  

def animals_detect(frame):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids, confidences, boxes = [], [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == "cat":  
                center_x, center_y = int(detection[0] * width), int(detection[1] * height)
                w, h = int(detection[2] * width), int(detection[3] * height)
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    return boxes, indexes

def calculate_the_distance(loc1, loc2):
    return geodesic(loc1, loc2).meters

def send_alert(distance):
    print(f"🚨 Alert! Animal herd detected nearby: Distance = {distance:.2f} meters 🚨")

image_path = "cat2.jpg"  
frame = cv2.imread(image_path)
if frame is None:
    print("❌ Error: Could not load image!")
else:
    herd_locations = []  #
    boxes, indexes = animals_detect(frame)
    for i in range(len(boxes)):
        if i in indexes:
            herd_lat = current_location[0] + np.random.uniform(-0.01, 0.01)
            herd_lon = current_location[1] + np.random.uniform(-0.01, 0.01)
            herd_locations.append((herd_lat, herd_lon))
            distance = calculate_the_distance(current_location, (herd_lat, herd_lon))
            send_alert(distance)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(10, 10))
    plt.imshow(frame_rgb)
    plt.axis('off')
    plt.title("Detected Animals")
    plt.show()

    folium_map = folium.Map(location=current_location, zoom_start=15)
    folium.Marker(
        location=current_location,
        popup="Your Location",
        icon=folium.Icon(color="blue")
    ).add_to(folium_map)
    for herd_loc in herd_locations:
        folium.Circle(
            location=herd_loc,
            radius=50, 
            color="red",
            fill=True,
            fill_color="red",
            popup=f"Herd Location: {herd_loc}"
        ).add_to(folium_map)
    folium_map.save("herd_map.html")
    import webbrowser
    webbrowser.open("herd_map.html")
