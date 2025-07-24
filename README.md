# Quality Python Plugin Example

This repository contains a Python example of a microservice plugin for the PalletScan platform. It demonstrates how a partner can connect to the PalletScan system's MQTT broker, receive notifications for new pallets, fetch pallet data via a REST API, perform a mock analysis, and submit the results back to the system.

## ⚙️ How it Works

1.  **MQTT Connection**: The script connects to the PalletScan MQTT broker and subscribes to the `palletscan/pallets/new` topic.
2.  **Receive Notification**: When a new pallet is scanned, the PalletScan system publishes a message to the topic with a `pallet_id`.
3.  **Fetch Data**: Upon receiving a notification, the script makes a `GET` request to the PalletScan API (`/api/v1/pallets/{pallet_id}/data`) to download the full data package for the pallet.
4.  **Process Data**: The script then simulates a custom analysis on the data. **This is where you would integrate your own machine learning model and processing logic.**
5.  **Submit Results**: Finally, the script submits the analysis results back to the PalletScan system via a `POST` request to `/api/v1/pallets/{pallet_id}/results`.

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* A PalletScan developer account with API keys and MQTT credentials.

### 1. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS and Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
