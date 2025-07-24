import os
import json
import logging
import time
import requests
import paho.mqtt.client as mqtt

# --- Configuration ---
# It's recommended to use environment variables for sensitive data and configuration.
MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST", "mqtt-host")
MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT", 1883))
MQTT_USERNAME = os.environ.get("MQTT_USERNAME", "your-username")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "your-password")
MQTT_NEW_PALLET_TOPIC = "quality/pallets/new"
MQTT_RESULTS_TOPIC_TEMPLATE = "quality/plugins/{plugin_id}/results"

QUALITY_API_URL = os.environ.get("QUALITY_API_URL", "https://east.arvistcloud.net/api/v1")
QUALITY_API_KEY = os.environ.get("QUALITY_API_KEY", "your-api-key")
PLUGIN_ID = os.environ.get("PLUGIN_ID", "your-plugin-id")

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_pallet_data(pallet_id: str):
    """
    This function orchestrates the processing of a single pallet.
    It fetches data, runs a mock analysis, and submits the results.
    """
    logging.info(f"Processing pallet with ID: {pallet_id}")

    # 1. Fetch data from quality API
    headers = {"X-API-Key": QUALITY_API_KEY}
    data_url = f"{QUALITY_API_URL}/pallets/{pallet_id}/data"
    
    try:
        response = requests.get(data_url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        pallet_data = response.json()
        logging.info(f"Successfully fetched data for pallet {pallet_id}")
        # In a real application, you would now download the images from the URLs provided in pallet_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data for pallet {pallet_id}: {e}")
        return

    # 2. Run your custom model and processing logic (mocked here)
    logging.info("Running custom model and analysis...")
    time.sleep(5)  # Simulate a time-consuming analysis
    analysis_results = {
        "custom_model_version": "1.2.3",
        "detected_products": [
            {"name": "Industrial Widget A", "quantity": 15, "confidence": 0.95},
            {"name": "Industrial Widget B", "quantity": 10, "confidence": 0.89},
        ],
        "quality_check": {
            "status": "PASS",
            "anomalies_detected": 0
        }
    }
    logging.info("Analysis complete.")

    # 3. Submit results back to quality
    # You can choose to submit via REST API for immediate feedback or MQTT for asynchronous processing.
    # Here, we'll use the REST API.
    results_url = f"{QUALITY_API_URL}/pallets/{pallet_id}/results"
    try:
        response = requests.post(results_url, headers=headers, json=analysis_results)
        response.raise_for_status()
        logging.info(f"Successfully submitted results for pallet {pallet_id}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to submit results for pallet {pallet_id}: {e}")


def on_connect(client, userdata, flags, rc):
    """The callback for when the client receives a CONNACK response from the server."""
    if rc == 0:
        logging.info("Connected to MQTT Broker!")
        client.subscribe(MQTT_NEW_PALLET_TOPIC)
        logging.info(f"Subscribed to topic: {MQTT_NEW_PALLET_TOPIC}")
    else:
        logging.error(f"Failed to connect, return code {rc}\n")


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    logging.info(f"Received message on topic {msg.topic}")
    try:
        payload = json.loads(msg.payload.decode())
        pallet_id = payload.get("pallet_id")
        if pallet_id:
            process_pallet_data(pallet_id)
        else:
            logging.warning("Received message without a 'pallet_id'")
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from message payload")
    except Exception as e:
        logging.error(f"An error occurred in on_message: {e}")


def main():
    """Main function to set up and run the MQTT client."""
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        client.loop_forever()
    except Exception as e:
        logging.error(f"Could not connect to MQTT broker: {e}")
    finally:
        client.disconnect()
        logging.info("Disconnected from MQTT broker.")


if __name__ == "__main__":
    main()
