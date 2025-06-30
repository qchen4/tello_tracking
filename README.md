# 🛸 Tello Drone Object Tracker

This project enables a **DJI Tello drone** to track a colored object (e.g. green, red, or blue) in real-time using computer vision (OpenCV) and HSV color masking. It includes a robust command-line interface and an HSV tuning tool to support flexible deployments.

---

## 🎯 Features

- ✅ Real-time object detection via HSV color masking
- 🎨 Choose from built-in color presets or load custom HSV from `hsv_config.json`
- 🛠 Interactive command system: `takeoff`, `start`, `land`, `exit`
- 🧠 Modular, well-documented Python code with clean structure
- 🎛 Live HSV tuning tool (`hsv_calibrator.py`) to fine-tune object detection
- 💾 Configuration persistence using JSON
- 🧹 Safe shutdown with automatic landing and stream cleanup

---

## 🗂 Project Structure

```
tello_green_tracking/
├── track_green_logo.py         # Main drone object tracking script
├── hsv_calibrator.py           # GUI-based HSV calibration tool
├── hsv_config.json             # Saved HSV thresholds
├── requirements.txt            # Required Python dependencies
├── README.md                   # You're reading it!
└── utils/
    └── pid.py                  # (Optional) PID controller class for future use
```

---

## 🚀 Setup Instructions

### 1. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 📶 Connect to Tello

- Power on your DJI Tello
- Connect your computer to the Tello Wi-Fi network (e.g. `TELLO-XXXXXX`)

---

## ▶️ Usage

### 🔹 Step 1: Run the Main Script

```bash
python track_green_logo.py
```

### 🔹 Step 2: Select HSV Source

You will be prompted to select:

```
1 - Green (default)
2 - Red
3 - Blue
4 - Load from hsv_config.json
```

### 🔹 Step 3: Use Drone Commands

You can type any of the following during runtime:

- `takeoff` → Drone takes off
- `start` → Begin object tracking
- `land` → Land the drone
- `exit` → End program and shut down safely

You can press **`q`** during tracking to stop the tracking loop.

---

## 🎛 HSV Calibration Tool

To visually tune the HSV range:

```bash
python hsv_calibrator.py
```

- Use the sliders to adjust `H`, `S`, and `V` ranges
- View live mask and detection results
- Press `s` to save to `hsv_config.json`
- Press `q` to quit

---

## 💡 Future Enhancements

- [ ] PID-based motion smoothing
- [ ] Obstacle avoidance
- [ ] AprilTag / ArUco integration
- [ ] Voice-command control

---

## 🧑‍💻 Author

**Qiyue Chen**  
Graduate Student @ Georgia Tech  
Focus: Embedded AI, Computer Vision, Robotics

---

## 📜 License

MIT License – feel free to use, modify, and share.
