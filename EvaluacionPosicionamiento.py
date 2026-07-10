import argparse
import csv
from collections import defaultdict
from pathlib import Path
import cv2
import numpy as np
from shapely.geometry import Polygon, Point
from ultralytics import YOLO
from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors

track_history = defaultdict(list)

current_region = None
counting_regions = [
    {
        "name": "Blue Region",
        "polygon": Polygon([(401, 138), (295, 310), (1283, 272), (907, 123)]),  # Polygon points,
        "region_color": (255, 0, 0),  # BGR Value
    },
    {
        "name": "Red Region",
        #"polygon": Polygon([(338, 497), (584, 318), (368, 326), (7, 407)]),  # Polygon points
        "polygon": Polygon([(293, 390), (153, 702), (1205, 676), (1288, 331)]),  # Polygon points
        "region_color": (0, 0, 255),  # BGR Value
    },
    {
        "name": "Red Region",
        "polygon": Polygon([(367, 154), (264, 308), (2, 322), (61, 158)]),  # Polygon points,
        "region_color": (0, 0, 255),  # BGR Value
    },
]

region_red_count = 0
region_blue_count = 0

# Lista para almacenar las coordenadas del centroide
centroid_coordinates = []

def mouse_callback(event, x, y, flags, param):
    global current_region

    if event == cv2.EVENT_LBUTTONDOWN:
        for region in counting_regions:
            if region["polygon"].contains(Point((x, y))):
                current_region = region
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
    global region_red_count, region_blue_count

    if not Path(source).exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")

    model = YOLO(f"{weights}")
    model.to("cuda") if device == "0" else model.to("cpu")

    names = model.model.names

    videocapture = cv2.VideoCapture(source)
    frame_width, frame_height = int(videocapture.get(3)), int(videocapture.get(4))
    fps, fourcc = int(videocapture.get(5)), cv2.VideoWriter_fourcc(*"mp4v")

    save_dir = increment_path(Path("ultralytics_rc_output") / "exp", exist_ok)
    save_dir.mkdir(parents=True, exist_ok=True)
    video_writer = cv2.VideoWriter(str(save_dir / f"{Path(source).stem}.mp4"), fourcc, fps, (frame_width, frame_height))

    while videocapture.isOpened():
        success, frame = videocapture.read()
        if not success:
            break

        results = model.track(frame, persist=True, classes=classes)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()  # Convert to numpy array
            track_ids = results[0].boxes.id.int().cpu().tolist()
            clss = results[0].boxes.cls.cpu().tolist()

            annotator = Annotator(frame, line_width=line_thickness, example=str(names))

            for box, track_id, cls in zip(boxes, track_ids, clss):
                if names[cls] == 'person':
                    annotator.box_label(box, 'Evaluado', color=(114, 128, 250))
                    bbox_center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                    track = track_history[track_id]
                    track.append((bbox_center[0], bbox_center[1]))
                    if len(track) > 30:
                        track.pop(0)
                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(frame, [points], isClosed=False, color=(114, 128, 250), thickness=track_thickness)
                    # Check if detection inside region
                    in_any_region = False
                    for region in counting_regions:
                        if region["polygon"].contains(Point((bbox_center[0], bbox_center[1]))):
                            in_any_region = True
                            if region["name"] == "Red Region":
                                region_red_count += 1
                            elif region["name"] == "Blue Region":
                                region_blue_count += 1

                    # If not in any defined region, count as Red Region
                    if not in_any_region:
                        region_red_count += 1

                    # Agregar coordenadas del centroide a la lista
                    centroid_coordinates.append((bbox_center[0], bbox_center[1]))

        # Draw regions (Polygons/Rectangles)
        for region in counting_regions:
            polygon_coords = np.array(region["polygon"].exterior.coords, dtype=np.int32)
            cv2.polylines(frame, [polygon_coords], isClosed=True, color=region["region_color"],
                          thickness=region_thickness)

        if view_img:
            if not cv2.getWindowProperty("Ultralytics YOLOv8 Region Counter Movable", cv2.WND_PROP_VISIBLE):
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

    # Escribir las coordenadas del centroide en un archivo CSV
    def write_to_csv(filename, coordinates):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y'])
            writer.writerows(coordinates)

    # Llamar a la función para escribir en el archivo CSV
    write_to_csv('coordenadas_posicionamiento.csv', centroid_coordinates)

    # Calcular porcentajes
    total = region_red_count + region_blue_count
    region_red_percentage = (region_red_count / total) * 100 if total > 0 else 0
    region_blue_percentage = (region_blue_count / total) * 100 if total > 0 else 0

    print(f"Red Region: {region_red_percentage:.2f}%")
    print(f"Blue Region: {region_blue_percentage:.2f}%")

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
