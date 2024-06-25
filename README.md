# ECG Tracker
---
KiCad8_project : KiCad 8.0 project with PCB design for LUT  
![Alt text](./images_for_readme/schematic.png?raw=true "Scheme of connections")
![Alt text](./images_for_readme/tracing.png?raw=true "Traced PCB")
Case_3dmodels : 3d models of case in .step format  
model : folder with neural network (LSTM-based autoencoder) and notebook for its training  

ECG_track.py : class for ECG tracking realizing Interface.py
socket_.py : PC program
main.py : micropython program for ESP32