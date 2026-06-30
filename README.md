<div align="center">

# 🤖 SortBot

### AI-Powered Waste Sorting Simulation

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/YOLOv11n-Ultralytics-FF6F00?style=for-the-badge&logo=yolo&logoColor=white" alt="YOLOv11n"/>
  <img src="https://img.shields.io/badge/Unity-Integration-000000?style=for-the-badge&logo=unity&logoColor=white" alt="Unity"/>
</p>

<p align="center">
  An intelligent waste sorting system that combines <strong>computer vision</strong> with a <strong>Unity simulation</strong>.<br/>
  A YOLOv11n AI model detects and classifies waste objects in real-time, while a FastAPI server bridges the gap between the simulation and the AI brain.
</p>

---

</div>

## 🏗️ Architecture

```
┌──────────────────┐         ┌──────────────────────┐         ┌──────────────────┐
│                  │  Image  │                      │  Image  │                  │
│   Unity Game     │ ──────►│   FastAPI Server      │ ──────►│   YOLOv11n AI    │
│   (Simulation)   │         │   (The Messenger)    │         │   (The Brain)    │
│                  │ ◄────── │                      │ ◄────── │                  │
│                  │  JSON   │   localhost:8000     │  Result │                  │
└──────────────────┘         └──────────────────────┘         └──────────────────┘
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **AI Detection** | YOLOv11n model trained to classify waste into **Cardboard**, **Metal**, **Plastic**, and **Other** |
| 🌐 **REST API** | FastAPI server with `POST /detect` endpoint accepting image uploads |
| 🎮 **Unity Bridge** | Seamless integration — Unity sends frames, gets JSON results back automatically |
| 🛡️ **Error Handling** | Validates images, handles corrupt files, and manages no-detection cases |
| 📊 **Confidence Gate** | Detections below 25% confidence are automatically classified as `"Unknown"` |
| 📝 **Auto Docs** | Interactive Swagger UI at `/docs` for easy testing |

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/nourahmedmohamed1/sortBot.git
cd sortBot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
python main.py
```

The server starts at **http://localhost:8000** 🎉

### 4. Test it
- Visit **http://localhost:8000/** → Health check
- Visit **http://localhost:8000/docs** → Swagger UI (upload an image to test)

## 📡 API Reference

### `GET /` — Health Check
```json
{
  "status": "online",
  "service": "SortBot Waste Detection API",
  "version": "1.0.0"
}
```

### `POST /detect` — Waste Detection

**Request:** `multipart/form-data` with an image file

**Response (Success):**
```json
{
  "success": true,
  "detection": {
    "waste_class": "Plastic",
    "confidence": 0.87,
    "center_coordinates": { "x": 320, "y": 240 }
  },
  "message": null
}
```

**Response (No Detection):**
```json
{
  "success": true,
  "detection": null,
  "message": "No object detected in the image."
}
```

## 🗂️ Project Structure

```
sortBot/
├── main.py              # FastAPI server + YOLOv11n integration
├── Yolo11nBest.pt       # Trained YOLOv11n model weights
├── requirements.txt     # Python dependencies
└── README.md            # You are here!
```

## 🏷️ Waste Classes

| Class ID | Label |
|----------|-------|
| 0 | ♻️ Cardboard |
| 1 | 🗑️ Other |
| 2 | 🔩 Metal |
| 3 | 🧴 Plastic |

---

<div align="center">

## 👥 Meet the Team

<table>
  <tr>
    <td align="center" width="160">
      <img src="https://api.dicebear.com/9.x/initials/svg?seed=MA&backgroundColor=0284c7&textColor=ffffff&fontSize=40" width="80" height="80" style="border-radius:50%;" alt="Member 1"/><br/>
      <strong>Member A</strong><br/>
      <sub>🧠 The AI Brain</sub><br/><br/>
      <a href="https://linkedin.com/in/member-a"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="22"/></a>
      <a href="https://github.com/member-a"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="22"/></a>
    </td>
    <td align="center" width="160">
      <img src="https://api.dicebear.com/9.x/initials/svg?seed=MB&backgroundColor=7c3aed&textColor=ffffff&fontSize=40" width="80" height="80" style="border-radius:50%;" alt="Member 2"/><br/>
      <strong>Member B</strong><br/>
      <sub>📡 The Messenger</sub><br/><br/>
      <a href="https://linkedin.com/in/member-b"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="22"/></a>
      <a href="https://github.com/member-b"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="22"/></a>
    </td>
    <td align="center" width="160">
      <img src="https://api.dicebear.com/9.x/initials/svg?seed=MC&backgroundColor=059669&textColor=ffffff&fontSize=40" width="80" height="80" style="border-radius:50%;" alt="Member 3"/><br/>
      <strong>Member C</strong><br/>
      <sub>🎮 Unity Developer</sub><br/><br/>
      <a href="https://linkedin.com/in/member-c"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="22"/></a>
      <a href="https://github.com/member-c"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="22"/></a>
    </td>
  </tr>
  <tr>
    <td align="center" width="160">
      <img src="https://api.dicebear.com/9.x/initials/svg?seed=MD&backgroundColor=dc2626&textColor=ffffff&fontSize=40" width="80" height="80" style="border-radius:50%;" alt="Member 4"/><br/>
      <strong>Member D</strong><br/>
      <sub>🎨 3D Artist</sub><br/><br/>
      <a href="https://linkedin.com/in/member-d"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="22"/></a>
      <a href="https://github.com/member-d"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="22"/></a>
    </td>
    <td align="center" width="160">
      <img src="https://api.dicebear.com/9.x/initials/svg?seed=ME&backgroundColor=ea580c&textColor=ffffff&fontSize=40" width="80" height="80" style="border-radius:50%;" alt="Member 5"/><br/>
      <strong>Member E</strong><br/>
      <sub>📋 Project Manager</sub><br/><br/>
      <a href="https://linkedin.com/in/member-e"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="22"/></a>
      <a href="https://github.com/member-e"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="22"/></a>
    </td>
    <td align="center" width="160">
      <img src="https://api.dicebear.com/9.x/initials/svg?seed=MF&backgroundColor=ca8a04&textColor=ffffff&fontSize=40" width="80" height="80" style="border-radius:50%;" alt="Member 6"/><br/>
      <strong>Member F</strong><br/>
      <sub>🧪 QA & Testing</sub><br/><br/>
      <a href="https://linkedin.com/in/member-f"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="22"/></a>
      <a href="https://github.com/member-f"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="22"/></a>
    </td>
    </td>
  </tr>
  <tr>
    <td align="center" width="160" colspan="3">
      <img src="https://api.dicebear.com/9.x/initials/svg?seed=MG&backgroundColor=ec4899&textColor=ffffff&fontSize=40" width="80" height="80" style="border-radius:50%;" alt="Member 7"/><br/>
      <strong>Member G</strong><br/>
      <sub>⚙️ Systems Engineer</sub><br/><br/>
      <a href="https://linkedin.com/in/member-g"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="22"/></a>
      <a href="https://github.com/member-g"><img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="22"/></a>
    </td>
  </tr>
</table>

---

<p>
  <img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red?style=for-the-badge" alt="Made with Love"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License"/>
</p>

</div>
