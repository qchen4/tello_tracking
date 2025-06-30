# 🛸 Tello Drone Green Object Tracker

A real-time computer vision system that enables a **DJI Tello drone** to autonomously detect and track colored objects using HSV color filtering and OpenCV. The system provides precise control with visual feedback and includes an interactive calibration tool for optimal color detection.

## ✨ Features

- 🎯 **Real-time Green Object Detection** using HSV color space filtering
- 🚁 **Autonomous Drone Control** via `djitellopy` library
- ⚙️ **Intelligent Tracking** with X/Y axis movement control
- 🎛️ **Interactive HSV Calibration Tool** with real-time slider adjustment
- 💾 **Persistent Configuration** with JSON-based settings storage
- 🛑 **Safety Features** including emergency landing and resource cleanup
- 📊 **Visual Feedback** with dual-window display (original + mask)
- 🧠 **Modular PID Controller** for smooth motion control (optional)

## 📋 Prerequisites

- **Python 3.7+**
- **DJI Tello Drone** (any model)
- **Computer with WiFi capability**
- **Good lighting conditions** for optimal color detection
- **Open space** for safe drone operation

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/tello_green_tracking.git
cd tello_green_tracking
pip install -r requirements.txt
```

### 2. Connect to Tello

1. Power on your Tello drone
2. Connect your computer to the Tello's WiFi network (e.g., `TELLO-XXXXXX`)
3. Ensure stable connection before proceeding

### 3. Calibrate Color Detection (Recommended)

```bash
python hsv_calibrator.py
```

- Use the sliders to adjust HSV values until your green object is clearly visible in the mask
- Press `s` to save the configuration
- Press `q` to exit

### 4. Start Tracking

```bash
python track_green_logo.py
```

The drone will:
- Take off automatically
- Begin searching for green objects
- Move to center detected objects in the camera view
- Display real-time video feed and detection mask

**Controls:**
- Press `q` to safely land and exit

## 📁 Project Structure

```
tello_green_tracking/
├── track_green_logo.py          # Main drone tracking application
├── hsv_calibrator.py            # Interactive HSV color calibration tool
├── hsv_config.json              # Saved HSV color thresholds
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── utils/
    └── pid.py                   # PID controller implementation
```

## 🔧 Configuration

### HSV Color Settings

The system uses HSV (Hue, Saturation, Value) color space for robust color detection. Default green thresholds:

```python
lower_green = [40, 70, 70]    # Lower HSV bounds
upper_green = [80, 255, 255]  # Upper HSV bounds
```

### Movement Parameters

- **Frame Size**: 640x480 pixels
- **Movement Tolerance**: 40 pixels (dead zone around center)
- **Movement Distance**: 20cm per command
- **Minimum Object Size**: 300 pixels² (noise filtering)

## 🎛️ Advanced Usage

### HSV Calibration Tool

The calibration tool (`hsv_calibrator.py`) provides:

- **Real-time HSV adjustment** with sliders
- **Live preview** of detection mask
- **Filtered result view** showing detected objects
- **Configuration persistence** to JSON file

**Usage:**
```bash
python hsv_calibrator.py
```

**Controls:**
- Adjust HSV sliders for optimal detection
- Press `s` to save current settings
- Press `q` to exit

### PID Controller Integration

For smoother motion control, the project includes a PID controller in `utils/pid.py`:

```python
from utils.pid import PID

# Initialize PID controllers for X and Y axes
pid_x = PID(kp=0.5, ki=0.1, kd=0.2)
pid_y = PID(kp=0.5, ki=0.1, kd=0.2)

# Use in tracking loop
output_x = pid_x.update(error_x, dt)
output_y = pid_y.update(error_y, dt)
```

## 🔍 How It Works

1. **Video Capture**: Streams real-time video from Tello's camera
2. **Color Conversion**: Converts BGR frames to HSV color space
3. **Object Detection**: Applies HSV mask to isolate green regions
4. **Contour Analysis**: Finds the largest green contour (target object)
5. **Position Calculation**: Computes offset from frame center
6. **Movement Control**: Sends RC commands to center the object
7. **Visual Feedback**: Displays original frame and detection mask

## 🛡️ Safety Guidelines

- **Always test in open spaces** with no obstacles
- **Maintain safe distance** from people and objects
- **Ensure good lighting** for reliable color detection
- **Keep hands clear** of propellers during operation
- **Use emergency landing** (`q` key) if tracking becomes unstable
- **Check battery level** before extended flights

## 🐛 Troubleshooting

### Common Issues

**Drone not connecting:**
- Verify WiFi connection to Tello network
- Check if Tello is powered on and ready
- Restart the script if connection fails

**Poor color detection:**
- Use the HSV calibrator to adjust thresholds
- Ensure adequate lighting conditions
- Check for color interference from background

**Erratic movement:**
- Increase movement tolerance in code
- Reduce movement distance per command
- Check for wind or environmental factors

**Performance issues:**
- Reduce frame resolution if needed
- Close unnecessary applications
- Ensure stable WiFi connection

## 🔮 Future Enhancements

- [ ] **Multi-color tracking** support
- [ ] **Obstacle avoidance** using depth sensors
- [ ] **Path planning** and return-to-home functionality
- [ ] **Voice control** integration
- [ ] **Web interface** for remote monitoring
- [ ] **Data logging** and analytics
- [ ] **Machine learning** for improved detection
- [ ] **Multi-drone** coordination support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Qiyue Chen**  
Graduate Student @ Georgia Tech  
Focus: Embedded AI, Computer Vision, Robotics, and Data Systems  
GitHub: [github.com/yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- DJI for the Tello drone platform
- OpenCV community for computer vision tools
- `djitellopy` library developers
- Georgia Tech for academic support

---

**⚠️ Disclaimer**: This project is for educational and research purposes. Always follow local drone regulations and safety guidelines when operating unmanned aerial vehicles.
