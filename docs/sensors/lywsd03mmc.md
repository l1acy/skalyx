# Xiaomi LYWSD03MMC Setup Guide

This guide explains how to flash, configure, and connect the **Xiaomi Mijia LYWSD03MMC** temperature and humidity sensor to Skalyx

By default, this sensor uses a proprietary and encrypted BLE protocol with a very slow broadcasting interval (often 10 minutes). To achieve real-time updates and local-first privacy, we will replace the stock firmware with a custom open-source one and configure it to broadcast using the standard BTHome v2 format

# Prerequisites
- **Hardware:** Xiaomi LYWSD03MMC sensor
- **Battery:** A fresh CR2032 battery. **Important:** The sensor's battery level must be above 40% for reliable flashing and GATT connections. If you encounter connection errors, replace the battery first
- **Browser:** Google Chrome or Microsoft Edge on a computer with Bluetooth, or on an Android smartphone

# 1. Flash the Custom Firmware
We recommend using the PVVX custom firmware due to its stability, active development, and excellent BTHome v2 support

1. Open the PVVX Web Flasher in your browser:
https://pvvx.github.io/ATC_MiThermometer/TelinkMiFlasher.html
2. Click Connect and select your LYWSD03MMC sensor from the Bluetooth popup.
3. Follow the on-screen prompts to flash the custom firmware. If you are on a newer hardware revision (e.g., B1.5/B1.6) or a newer stock firmware, the tool may automatically guide you through flashing an intermediate "Original OTA" firmware first. Let the process complete fully
4. Once the flashing is done, the sensor will reboot and its screen will briefly show a surprised smiley face (:O)

# 2. Configure BTHome v2 for Skalyx
1. On the same PVVX Flasher page, click Connect again to reconnect to the sensor
2. Scroll down to the settings section
3. Set `Advertising type` to `BTHome v2`. This is the standard format for Home Assistant and Skalyx
4. (Optional) Set `Advertising interval` to `10000` ms (10 seconds). Avoid setting it too high (e.g., 60 seconds) to prevent connection timeouts during future configuration changes.
5. Ensure `Encryption` is turned Off for the simplest setup
6. Click `Send Config` to save the settings to the sensor

# Step 3: Add to Skalyx
1. Find the MAC address of your sensor. You can see it in the PVVX flasher interface or by using a BLE scanner app like n`RF Connect`
2. **Edit your configuration file.** Open the skalyx.toml file located in the server directory and add a new device section using the following format:
    ```toml
    [[devices]]
    device_id = "YOUR_DEVICE_ID"
    address = "YOUR_DEVICE_MAC"
    parser = "bthome_v2"
    
    [devices.parser_params]
    service_data_uuid = "0000fcd2-0000-1000-8000-00805f9b34fb"
    ```
3. Restart the Skalyx server
