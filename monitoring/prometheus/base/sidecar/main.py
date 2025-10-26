from kubernetes import client, config
import json
import logging
import time
import os # Included for best practice/atomic write, though not used in final code below

# --- Logging Setup ---
logging.basicConfig(level="INFO")
# logging.getLogger("kubernetes").setLevel(logging.DEBUG)

# --- K8s Config Loading ---
try:
    # 1. Load the in-cluster configuration (uses ServiceAccount token and ENV vars)
    config.load_incluster_config()
    logging.info("Successfully loaded in-cluster config.")
except config.ConfigException:
    logging.warning("Warning: Failed to load in-cluster config. Falling back to external config.")
    config.load_kube_config("./.config") # Load local kubeconfig for development and testing


v1 = client.CoreV1Api()
sleepTime = 100
FINAL_FILE_PATH = "/etc/prometheus/targets/target.json"

logging.info(f"Starting discovery agent. Refresh interval: {sleepTime}s")

while True:
    try:
        response = v1.list_endpoints_for_all_namespaces()
        targets = []
        
        for ep in response.items:
            if not ep.subsets:
                continue
            
            for subset in ep.subsets:
                addresses = subset.addresses or []
                ports = subset.ports or []
                
                # --- NESTED LOOPS START HERE ---
                
                # 1. Loop over addresses (IPs)
                for address in addresses:
                    target_ip = address.ip
                    
                    # 2. Loop over ports 
                    for port in ports:
                        
                        # Filter logic: only target if the port is 9100
                        if port.port != 9100:
                            continue
                        pod_name = address.target_ref.name if address.target_ref else "unknown-pod"                        
                        target_port = port.port
                        
                        targets.append(
                            {
                                 # Use IP:PORT format
                                "targets": [f'{target_ip}:{target_port}'], 
                                "labels": {
                                    # Use Endpoint metadata
                                    "namespace": ep.metadata.namespace, 
                                    "service_name": ep.metadata.name, 
                                    "pod_name": pod_name
                                }
                            }
                        )
                
                # --- NESTED LOOPS END HERE ---
    
        # --- File Writing ---
        with open(FINAL_FILE_PATH, 'r') as existingConf:
            existingTargets = json.load(existingConf)
        with open(FINAL_FILE_PATH, 'w') as file:
            for target in targets:
                existingTargets.append(target)
            json.dump(existingTargets, file, indent=4)
        logging.info(f"Successfully wrote {len(targets)} targets to JSON file. Sleeping.")

        # The order of Exceptions matters! Python goes top to bottom when looking for exception handling
        # FileNotFoundError - is a subclass of the Exception
    except FileNotFoundError:
        # Log if file not exist
        logging.INFO("Scraping targets file doesn't exist, creating a new one")
        with open(FINAL_FILE_PATH, 'w') as file:
            json.dump(targets, file, indent=4)
    except Exception as e:
        # Log any unexpected errors
        logging.error(f"An error occurred in the loop: {e}. Retrying after delay.")
       
    # Pause execution
    time.sleep(sleepTime)
