# Oil & Gas Compressor Station SCADA Demo

## Description

This repository contains a proof-of-concept SCADA/HMI project for an oil & gas compressor station, built using Inductive Automation’s Ignition platform. It demonstrates:

- A live Vision HMI showing inlet/outlet pressures, a Start/Stop compressor control, and a pressure alarm indicator
- An OPC UA network capture of the SecureChannel handshake, ReadRequest, and WriteRequest messages (docs/wireshark.png)
- A Streamlit dashboard (to be linked below) that visualizes historical pressure data from a CSV log

## What’s Included

1. **Ignition HMI Project** (ignition_project/)

   - Vision window with numeric labels bound to OPC UA tags
   - 2-State Toggle button bound to a “Compressor_On” boolean tag
   - Multi-State Indicator for “Pressure_Alarm”
   - Tag definitions for `Inlet_Pressure`, `Outlet_Pressure`, `Compressor_On`, and `Pressure_Alarm`

2. **OPC UA Packet Capture** (docs/wireshark_pressure.png)

   - Screenshot of Wireshark showing:
     - OpenSecureChannelRequest/Response (Service 0 handshake)
     - ReadRequest (pressure polling)
     - WriteRequest (compressor on/off)

3. **Historical Data Log** (data/pressure_log.csv)

   - Sample timestamped pressures and alarm flags used by the Streamlit app. Currently it is done on randomly generated sample data and not from the created OPC UA server.

4. **Streamlit Dashboard** (streamlit_app/)
   - Interactive line and bar charts of pressure trends
   - Raw data table view
   - (Link to live demo: **https://oil-gas-pressure-dashboard-rqnnt84d9sbu793upsqmow.streamlit.app/**)

## Prerequisites

- **Ignition Maker Edition** (8.1.x or later)
- **Python 3.8+** and **pip** (for Streamlit)
- **Wireshark** (for packet capture)

## Setup & Run

### 1. Import & Launch the Ignition Project

1. Start Ignition Maker Edition on your machine.
2. In the Gateway web UI, go to **Config → Projects → Import Project** and select the `ignition_project/OilGasPressureDemo.gateway` bundle.
3. Under **Config → OPC UA → Server**, verify **Bind Port** is `62541` and the server is **Enabled**.
4. Under **Status → Connections → OPC Connections**, ensure the “Ignition OPC UA Server” is **Connected**.
5. Under **Status → Connections → Designer Sessions**, click **Launch Designer**, open **CompressorStation**, and enter **Preview**.

### 2. Capture OPC UA Traffic

1. Open **Wireshark** and start a capture on **Loopback: lo0** with capture filter `port 62541`.
2. In Designer Preview, reset your session (disconnect/relaunch) so it reconnects to OPC UA.
3. Click **Start Compressor** and **Stop Compressor** a few times.
4. Stop capture and open `docs/wireshark.png` to view the handshake, read, and write messages.

### 3. Launch the Streamlit Dashboard

1. Open the link: **https://oil-gas-pressure-dashboard-rqnnt84d9sbu793upsqmow.streamlit.app/**
