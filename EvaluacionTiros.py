import cv2
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict
from shapely.geometry import Polygon, Point
from ultralytics import YOLO
from ultralytics.utils.files import increment_path
import csv
import random

track_history = defaultdict(list)

current_region = None
counting_region = {
    "name": "Zona Azul",
    "polygon": Polygon([(300, 319), (300, 316),(947, 321), (947, 325)]),  
    "region_color": (255, 0, 0), 
    "dragging": False,
    "offset_x": 0,
    "offset_y": 0,
}

region_azul_count = 0
fallo_count = 0
total_frames = 0
total_tiros = 6

def mouse_callback(event, x, y, flags, param):
    global current_region

    if event == cv2.EVENT_LBUTTONDOWN:
        if counting_region["polygon"].contains(Point((x, y))):
            current_region = counting_region
            current_region["dragging"] = True
            current_region["offset_x"] = x
            current_region["offset_y"] = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if current_region is not None and current_region["dragging"]:
            dx = x - current_region["offset_x"]
            dy = y - current_region["offset_y"]
            current_region["polygon"] = Polygon(
                [(p[0] + dx, p[1] + dy) for p in current_region["polygon"].exterior.coords]
            )
            current_region["offset_x"] = x
            current_region["offset_y"] = y

    elif event == cv2.EVENT_LBUTTONUP:
        if current_region is not None and current_region["dragging"]:
            current_region["dragging"] = False

def run(
    weights="yolov8n.pt",
    source=None,
    device="cpu",
    view_img=False,
    save_img=False,
    exist_ok=False,
    classes=None,
    line_thickness=2,
    track_thickness=2,
    region_thickness=2,
):
    global region_azul_count, fallo_count, total_frames

    if not Path(source).exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")

    model = YOLO(weights)
    model.to("cuda") if device == "0" else model.to("cpu")

    names = model.model.names

    videocapture = cv2.VideoCapture(source)
    frame_width, frame_height = int(videocapture.get(3)), int(videocapture.get(4))
    fps, fourcc = int(videocapture.get(5)), cv2.VideoWriter_fourcc(*"mp4v")

    # Directorio para guardar el video y el archivo CSV
    save_dir = increment_path(Path("ultralytics_rc_output") / "exp", exist_ok)
    save_dir.mkdir(parents=True, exist_ok=True)
    video_writer = cv2.VideoWriter(str(save_dir / f"{Path(source).stem}.mp4"), fourcc, fps, (frame_width, frame_height))

    csv_path = Path(__file__).resolve().parent / "coordenadas_tiros.csv"
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['X', 'Y', 'T'])

    while videocapture.isOpened():
        success, frame = videocapture.read()
        if not success:
            break
        total_frames += 1

        results = model.track(frame, persist=True, classes=classes)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            clss = results[0].boxes.cls.cpu().tolist()

            for box, track_id, cls in zip(boxes, track_ids, clss):
                label = ""
                color = None
                if names[cls] == 'person':
                    label = "Evaluado"
                    color = (0, 255, 255)  # Amarillo
                elif names[cls] == 'sports ball':
                    label = "Balon"
                    color = (0, 255, 0)  # Verde

                if label:
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, line_thickness)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    bbox_center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)  # Centro del bbox

                    track = track_history[track_id]
                    track.append((float(bbox_center[0]), float(bbox_center[1])))
                    if len(track) > 30:
                        track.pop(0)
                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(frame, [points], isClosed=False, color=color, thickness=track_thickness)

                    # Verificar si el centroide está en la zona azul
                    if counting_region["polygon"].contains(Point((bbox_center[0], bbox_center[1]))):
                        region_azul_count += 1
                        # Guardar centroides en el archivo CSV con etiqueta "A"
                        with open(csv_path, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([f"{bbox_center[0]:.8f}", f"{bbox_center[1]:.8f}", "A"])

        polygon_coords = np.array(counting_region["polygon"].exterior.coords, dtype=np.int32)
        cv2.polylines(frame, [polygon_coords], isClosed=True, color=counting_region["region_color"], thickness=region_thickness)

        if view_img:
            if total_frames == 1:
                cv2.namedWindow("Ultralytics YOLOv8 Region Counter Movable")
                cv2.setMouseCallback("Ultralytics YOLOv8 Region Counter Movable", mouse_callback)
            cv2.imshow("Ultralytics YOLOv8 Region Counter Movable", frame)

        if save_img:
            video_writer.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_writer.release()
    videocapture.release()
    cv2.destroyAllWindows()

    # Calcular y guardar los fallos
    fallos = total_tiros - region_azul_count
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for _ in range(fallos):
            coord_rand = (random.uniform(0, 150), random.uniform(0, 150))
            writer.writerow([f"{coord_rand[0]:.8f}", f"{coord_rand[1]:.8f}", "F"])

    # Calcular y mostrar porcentaje de efectividad por zona
    print("\nEfectividad por zona:")
    total_entries = region_azul_count
    if total_entries > 0:
        effectiveness_percentage = (region_azul_count / total_tiros) * 100
        print(f"Zona Azul: {effectiveness_percentage:.2f}% ({region_azul_count}/{total_tiros} entradas)")
    else:
        print("No se detectaron entradas en la Zona Azul.")

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str, default="yolov8n.pt", help="initial weights path")
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--source", type=str, required=True, help="video file path")
    parser.add_argument("--view-img", action="store_true", help="show results")
    parser.add_argument("--save-img", action="store_true", help="save results")
    parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")
    parser.add_argument("--classes", nargs="+", type=int, help="filter by class: --classes 0, or --classes 0 2 3")
    parser.add_argument("--line-thickness", type=int, default=2, help="bounding box thickness")
    parser.add_argument("--track-thickness", type=int, default=2, help="Tracking line thickness")
    parser.add_argument("--region-thickness", type=int, default=4, help="Region thickness")
    return parser.parse_args()

def main(opt):
    run(**vars(opt))
if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
