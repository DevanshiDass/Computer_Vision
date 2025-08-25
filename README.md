# 🖐️⚡ Computer Vision Playground  
_Real-time Gesture Recognition & Human-Computer Interaction Experiments_  

Welcome to my **Computer Vision Lab**, where I hack around with **OpenCV + MediaPipe + Python** to turn hand gestures into **mouse clicks, air drawings, and even music 🎹**.  

This repo is a **fusion of HCI (Human-Computer Interaction), AI-powered vision, and creativity**, showing how far webcams + clever math can go.  

---

## 🌐 Project Index  

### 1️⃣ Hand Mouse – _Touchless Control_  
Turn your webcam into a **gesture-driven mouse**:  
- 🖱 **Move cursor** → Index finger tip maps to screen space  
- 👌 **Left Click** → Pinch Index + Thumb (held = drag)  
- ✌️ **Right Click** → Pinch Index + Middle  

👉 Code: [`HandMouse/hand_mouse.py`](HandMouse/hand_mouse.py)  

---

### 2️⃣ Air Drawing Toolkit – _Iron Man Mode ✨_  
Use your fingers like a **digital paintbrush**:  
- 🖊 Draw → Index finger only  
- 🎨 Change Colors → Middle (Blue), Ring (Green), Pinky (Yellow)  
- 🧹 Clear → Open palm (all 5 fingers up)  
- 📐 Shapes → Pinch Index + Thumb (Rectangle)  
- ↩️ Undo → Thumb + Pinky  

👉 Code: [`AirDrawingToolkit/air_drawing.py`](AirDrawingToolkit/air_drawing.py)  

---

### 3️⃣ Virtual Piano – _Music Meets Vision 🎵_  
A camera-based **piano keyboard**:  
- 🎹 Screen is split into **13 virtual keys**  
- 🖐 Fingertips mapped → Trigger audio samples in real-time  
- 🔊 Plays pre-loaded `.wav` piano sounds with **zero lag**  

👉 Code: [`VirtualPiano/virtual_piano.py`](VirtualPiano/virtual_piano.py)  

---

## 🛠 Tech Stack  

- **OpenCV** → Real-time video processing  
- **MediaPipe** → Hand landmark detection (21 keypoints per hand 🤯)  
- **NumPy** → Canvas overlay & geometric math  
- **PyAutoGUI** → Mouse/keyboard emulation  
- **Pygame** → Audio engine for piano  
- **Math/Linear Algebra** → Distance, scaling, mapping screen coordinates  

💡 Combined, these create **real-time interaction pipelines**:  
`Webcam → Hand Tracking → Gesture Logic → Action (Draw / Click / Play Sound)`  

---

## ⚡ Quickstart  

```bash
git clone https://github.com/your-username/ComputerVision-Projects.git
cd ComputerVision-Projects
