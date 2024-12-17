# Robotik Projekt
von Schu und Lae

## Topic
Vergleich der Performance von Reinforcement Learning mit traditionellen Algorithmen der Bahnplanung für einen mobilen Roboter in einer 2D Grid World

[Das ist alles nur geklaut eo eo, das ist alles gar nicht meine (shoutout an Peter)]: # 
## Installation
Installieren als Python Package mit:
```python
pip install -e .
```
Für Jupyter Notebooks: autoreload um Kernel nicht neustarten zu müssen :P
```python
%load_ext autoreload
%autoreload 2
```
Klassendefinition:
<alg>.find_path() -> [(x_start, y_start), ... , (x_end, y_end)]



Metriken:
- Zeitkomplexität
- Speicherplatzkomplexität
- Rechenzeit (Training; Zeit bis Weg gefunden)
- Ressourcenverbrauch
- Konvergenz / Zeit bis Konvergenz
- Echtzeitfähig / Anytime --> kann er mit mehr Zeit was anfangen

falls noch Zeit:
- Optimierung / -fähigkeit
- Robustheit
- Lernfähigkeit (ja, nein)
- (Erklärbarkeit)
- globale / lokale Sicht

Map Metriken:
- Durchschnittliche Anzahl an Zuständen
- Durchschnittlicher längster Pfad
- (dynamisch absperrbare Gebiete)

Bahn Metriken:
- nähe zu Hindernis
- kantig; glatt --> max. Drehwinkel

Test:
- Größe der Umgebung
- Benchmark Umgebungen (basic und mit anderen kombiniert)

