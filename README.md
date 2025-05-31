# EmbodyCraft

EmbodyCraft captures muscle activity and fingertip vibrations during pottery, translating them into tactile cues for post-action reflection. Co-designed with Okinawan potters, the system enhances video-based review by revealing subtle force patterns and deepening skill understanding.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4e79a25e-d745-4e20-8c82-549069dfd7ba" width="500"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7b84fd54-fe65-429d-b1f3-8bdaa60791f8" width="500"/>
</p>



# FMG Interface and Accelerometer
This system records forearm **muscle activity (FMG)** and **fingertip vibrations** using two ESP32-connected 16-channel wireless FMG devices. The data is transmitted to a PC over UDP and can be replayed through haptic devices to support **post-action self-reflection** in craft practices, such as **pottery**.
![Slide 16_9 - 1](https://github.com/user-attachments/assets/4a53b777-6b6a-47a8-a84c-6d3aaa17932f)


## Features
-  16-channel FMG sensing per device (up to 2 devices)
-  Wireless UDP data streaming from ESP32
-  Data recording to CSV format
-  Device control panel: LED, brightness sliders, gain, calibration
-  Real-time visualization of FMG data
-  TouchDesigner-compatible output for multimedia applications
-  Designed for embodied skill reflection in craft practices
