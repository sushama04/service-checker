from flask import Flask, request, jsonify
import os
import psutil
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# File paths
log_path = "D:\Sushama_NewStart\Automation Project\Backend\Log"
log_file = f"Services-{datetime.now().strftime('%Y-%m-%d %H-%M')}.txt"
log_file_path = os.path.join(log_path, log_file)

# Ensure log directory exists
os.makedirs(log_path, exist_ok=True)

# Function to get service status
def get_service_status(service_name):
    try:
        service = psutil.win_service_get(service_name)
        return service.as_dict()['status']
    except Exception as e:
        return f"Error: {e}"

# Function to set service status (start/stop)
def set_service_status(service_name, desired_status):
    try:
        service = psutil.win_service_get(service_name)
        if desired_status.lower() == "running":
            service.start()
        elif desired_status.lower() == "stopped":
            service.stop()
    except Exception as e:
        return f"Error: {e}"

# Log actions
def log_actions(services_list):
    with open(log_file_path, 'a') as log:
        for index, row in services_list.iterrows():
            service_name = row['Name']
            desired_status = row['Status']
            current_status = get_service_status(service_name)

            if desired_status.lower() != current_status.lower():
                log_msg = f"Service : {service_name} is currently {current_status}, should be {desired_status}"
                log.write(log_msg + '\n')
                log.flush()

                set_service_status(service_name, desired_status)

                after_service_status = get_service_status(service_name)
                if desired_status.lower() == after_service_status.lower():
                    log_msg = f"Action was successful: Service {service_name} is now {after_service_status}"
                else:
                    log_msg = f"Action failed: Service {service_name} is still {after_service_status}, should be {desired_status}"
                log.write(log_msg + '\n')
                log.flush()

@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['file']
    if file:
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400

            log_actions(df)
            return jsonify({'message': 'Service monitoring and logging completed', 'log_file_path': log_file_path}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)
