import cv2
import argparse
import numpy as np
from pathlib import Path
from collections import defaultdict
from shapely.geometry import Polygon, Point
from ultralytics import YOLO
from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors
import csv
import random

track_history = defaultdict(list)
ball_in_region = defaultdict(bool)
entered_region = defaultdict(bool)

current_region = None
counting_regions = [
    {
        "name": "Large Region 1",
        #"polygon": Polygon([(5, 557), (96, 563), (351, 544), (229, 539), (5, 557)]),  # Polygon points
        "polygon": Polygon([(586, 339), (919, 327), (1004, 362), (633, 381), (586, 339)]),  # Polygon points
        "region_color": (0, 165, 255),  # BGR Value (Red)
    },
    {
        "name": "Large Region 2",
        #"polygon": Polygon([(319, 573), (582, 550), (761, 555), (453, 586), (319, 573)]),  # Polygon points
        "polygon": Polygon([(1004, 362), (633, 381), (673,455), (1168, 432), (1004, 362)]),
        "region_color": (0, 165, 255),  # BGR Value (Red)
    },
    {
        "name": "Large Region 3",
        #"polygon": Polygon([(1183, 581), (835, 627), (1165, 656), (1531, 598), (1183, 581)]),  # Polygon points
        "polygon": Polygon([(673,455), (1168, 432), (1504,560), (795,595), (673,455)]),  # Polygon points
        "region_color": (0, 165, 255),  # BGR Value (Red)
    },
    {
        "name": "Yellow Region",
        "polygon": Polygon([(922, 325), (1006, 355), (999, 360), (916,329), (922,330)]),  # Polygon points
        "region_color": (0, 255, 255),  # BGR Value (Yellow)
    },
    {
        "name": "Green Region",
        "polygon": Polygon([(1008,353), (1171,425), (1163,430), (1002, 360), (1008,360)]),  # Polygon points
        "region_color": (0, 255, 0),  # BGR Value (Green)
    },
    {
        "name": "Blue Region",
        "polygon": Polygon([(1173,425), (1513, 550), (1483, 555), (1155, 435), (1173,425)]),  # Polygon points
        "region_color": (255, 0, 0),  # BGR Value (Blue)
    },
]

region_counts = {
    "Yellow Region": 0,
    "Green Region": 0,
    "Blue Region": 0,
}
total_frames = 0

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

def is_point_inside_region(point, region):
    return region["polygon"].contains(Point(point))

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
        marker_radius=5,  # Radio del marcador para el centroide
):
    global total_frames

    if not Path(source).exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")

    model = YOLO(weights)
    device = 0 if device == "0" else "cpu"
    model.to(device)

    names = model.model.names

    videocapture = cv2.VideoCapture(source)
    frame_width, frame_height = int(videocapture.get(3)), int(videocapture.get(4))
    fps, fourcc = int(videocapture.get(5)), cv2.VideoWriter_fourcc(*"mp4v")

    save_dir = increment_path(Path("ultralytics_rc_output") / "exp", exist_ok)
    save_dir.mkdir(parents=True, exist_ok=True)
    video_writer = cv2.VideoWriter(str(save_dir / f"{Path(source).stem}.mp4"), fourcc, fps, (frame_width, frame_height))

    csv_path = Path(__file__).resolve().parent / "coordenadas_pases.csv"
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
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            clss = results[0].boxes.cls.cpu().tolist()

            annotator = Annotator(frame, line_width=line_thickness, example=str(names))

            for box, track_id, cls in zip(boxes, track_ids, clss):
                if names[cls] == 'sports ball':
                    class_name = 'Balon'
                elif names[cls] == 'person':
                    class_name = 'Evaluado'
                else:
                    continue  # Omitir otras clases no deseadas

                annotator.box_label(box, class_name, color=colors(cls, True))
                bbox_center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)  # Centro del cuadro delimitador

                if class_name == 'Balon':
                    track = track_history[track_id]
                    track.append(bbox_center)
                    if len(track) > 30:
                        track.pop(0)

                    # Dibujar el centroide como un círculo o marcador
                    cv2.circle(frame, (int(bbox_center[0]), int(bbox_center[1])), marker_radius, (0, 0, 255), -1)

                    # Dibujar la línea de trayectoria
                    for i in range(1, len(track)):
                        if track[i - 1] is None or track[i] is None:
                            continue
                        cv2.line(frame, (int(track[i - 1][0]), int(track[i - 1][1])),
                                 (int(track[i][0]), int(track[i][1])), (0, 255, 0), 2)

                    # Manejo de la entrada y salida de la región
                    for region_idx, region in enumerate(counting_regions):
                        if is_point_inside_region(bbox_center, region):
                            if region["name"] in ["Yellow Region", "Green Region", "Blue Region"]:
                                if not ball_in_region[track_id]:  # Si no estaba dentro previamente
                                    if not entered_region[track_id]:  # Si es la primera vez que entra
                                        region_counts[region["name"]] += 1
                                        entered_region[track_id] = True
                                        # Guardar las coordenadas en CSV con una A
                                        with open(csv_path, mode='a', newline='') as file:
                                            writer = csv.writer(file)
                                            writer.writerow([f"{bbox_center[0]:.8f}", f"{bbox_center[1]:.8f}", "A"])
                            ball_in_region[track_id] = True
                        else:
                            if ball_in_region[track_id]:  # Si estaba dentro y ahora salió completamente
                                ball_in_region[track_id] = False
                                entered_region[track_id] = False

        # Dibujar regiones (Polígonos/Rectángulos)
        for region in counting_regions:
            polygon_coords = np.array(region["polygon"].exterior.coords, dtype=np.int32)
            cv2.polylines(frame, [polygon_coords], isClosed=True, color=region["region_color"],
                          thickness=region_thickness)

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

    # Calcular y mostrar porcentaje de efectividad por zona
    print("\nEfectividad por zona:")
    total_entries = sum(region_counts.values())
    if total_entries > 0:
        for region_name, count in region_counts.items():
            effectiveness_percentage = (count / total_entries) * 100
            print(f"{region_name}: {effectiveness_percentage:.2f}% ({count}/{total_entries} entradas)")
    else:
        print("No se detectaron entradas en ninguna región.")
    # Calcular y guardar los fallos
    total_tiros = 8
    fallos = total_tiros - total_entries
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for _ in range(fallos):
            coord_rand = (random.uniform(0, 150), random.uniform(0, 150))
            writer.writerow([f"{coord_rand[0]:.8f}", f"{coord_rand[1]:.8f}", "F"])
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str, default="yolov8n.pt", help="initial weights path")
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--source", type=str, required=True, help="video file path")
    parser.add_argument("--view-img", action="store_true", help="show results")
    parser.add_argument("--save-img", action="store_true", help="save results")
    parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")

    return parser.parse_args()
if __name__ == "__main__":
    opt = parse_opt()
    run(
        weights=opt.weights,
        source=opt.source,
        device=opt.device,
        view_img=opt.view_img,
        save_img=opt.save_img,
        exist_ok=opt.exist_ok
    )
