# AgroVision

## Evaluación Automatizada de Tomates mediante Visión Artificial

AgroVision es un sistema de visión por computadora desarrollado para la detección, clasificación y seguimiento de tomates en tiempo real utilizando técnicas de inteligencia artificial. El proyecto implementa un modelo basado en YOLO para la detección de objetos y el algoritmo SORT para el seguimiento de cada tomate durante el procesamiento de video.

El sistema está diseñado para automatizar procesos de inspección agrícola, permitiendo clasificar tomates según su estado de maduración y detectar productos defectuosos con un alto nivel de precisión.

---

## Características

- Detección automática de tomates en tiempo real.
- Clasificación en tres categorías:
  - Maduro
  - Verde
  - Defectuoso
- Seguimiento de objetos mediante el algoritmo SORT.
- Procesamiento de video en tiempo real.
- Compatible con ejecución en CPU y GPU (CUDA).
- Visualización de:
  - Bounding Boxes
  - Clase detectada
  - Nivel de confianza
  - Identificador (Tracking ID)
  - Frames por segundo (FPS)

---

## Demostración

### Video

[Ver demostración](https://youtu.be/TU_VIDEO)


---

## Tecnologías utilizadas

- Python 3.10
- OpenCV
- PyTorch
- Ultralytics YOLO
- SORT
- FilterPy
- NumPy
- CUDA (opcional)

---

## Requisitos del sistema

### Hardware mínimo

- Procesador Intel Core i3 o equivalente
- 4 GB de memoria RAM
- Webcam compatible con OpenCV
- 2 GB de espacio disponible

### Hardware recomendado

- Procesador Intel Core i5 o superior
- 8 GB de memoria RAM o más
- Tarjeta gráfica NVIDIA compatible con CUDA
- Cámara HD (720p o superior)

### Software

- Windows 10 u 11
- Python 3.10
- pip actualizado

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/AgroVision.git

cd AgroVision
```

### 2. Crear un entorno virtual

**Windows**

```bash
python -m venv venv

venv\Scripts\activate
```

**Linux**

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar PyTorch con soporte CUDA (opcional)

Si dispone de una GPU NVIDIA, instale la versión de PyTorch compatible con CUDA desde:

https://pytorch.org/get-started/locally/

---

## Ejecución

Ejecute el sistema mediante:

```bash
python main.py
```

Al iniciar la aplicación:

1. Se activa la cámara.
2. Se capturan los fotogramas en tiempo real.
3. El modelo YOLO detecta los tomates presentes en la imagen.
4. Cada tomate es clasificado automáticamente.
5. El algoritmo SORT realiza el seguimiento de cada objeto.
6. Los resultados son mostrados en pantalla.

---

## Estructura del proyecto

```
AgroVision/
│
├── models/
│   └── best.pt
│
├── camera.py
├── detector.py
├── tracker.py
├── sort.py
├── train.py
├── main.py
├── requirements.txt
├── README.md
│
├── images/
│   ├── deteccion.png
│   ├── clasificacion.png
│   └── tracking.png
```

---

## Descripción de los archivos

| Archivo | Descripción |
|----------|-------------|
| `main.py` | Punto de entrada del sistema. Controla el flujo general del programa. |
| `camera.py` | Captura y configuración de la cámara. |
| `detector.py` | Implementa la detección utilizando el modelo YOLO. |
| `tracker.py` | Gestiona el seguimiento de objetos mediante SORT. |
| `sort.py` | Implementación del algoritmo SORT. |
| `train.py` | Permite entrenar nuevamente el modelo. |
| `models/best.pt` | Modelo entrenado utilizado para la detección. |

---

## Resultados

El sistema permite:

- Automatizar la inspección de productos agrícolas.
- Reducir la intervención manual.
- Mejorar la precisión de clasificación.
- Mantener el seguimiento individual de cada tomate.
- Procesar video en tiempo real utilizando CPU o GPU.

---

## Autores

- Ramiro Vega Meza
- Enrique Jiménez Calzada
- Haide Sánchez Gutiérrez
- Jazmín Alejandra Rojas Palafox
- María Esperanza Acosta Bernal
- Néstor Ariel Medina Díaz

**Universidad Autónoma del Estado de México**

Ingeniería en Computación

2026

---

## Licencia

Este proyecto fue desarrollado con fines académicos.
