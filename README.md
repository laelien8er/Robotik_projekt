# Robotik Projekt

## Topic
Vergleich der Performance von Reinforcement Learning mit traditionellen Algorithmen der Bahnplanung für einen mobilen Roboter in einer 2D Grid World

## Installation
Installieren als Python Package mit:
```python
pip install -e .
```
Die .ipynb Files des Abgabeordners können über Jupyter Notebook geöffnet werden. 

Für Jupyter Notebooks: autoreload um Kernel nicht neustarten zu müssen 
```python
%load_ext autoreload
%autoreload 2
```
Der gefundene Pfad jedes Algorithmus wird wie folgt ausgegeben:
```python
<alg>.find_path() -> [(x_start, y_start), ... , (x_end, y_end)]
```



