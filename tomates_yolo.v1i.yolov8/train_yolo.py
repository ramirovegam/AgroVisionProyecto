from ultralytics import YOLO

def main():
    # Cargar modelo base
    model = YOLO("yolov8n.pt")

    # Entrenamiento
    model.train(
        data="data.yaml",
        epochs=100,
        imgsz=640,
        batch=8,
        device="cpu"   # cambia a "0" si tienes GPU NVIDIA
    )

if __name__ == "__main__":
    main()
    