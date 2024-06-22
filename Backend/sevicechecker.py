import os
import psutil
import pandas as pd
from datetime import datetime

def monitor_services(services_file_path, log_path):
    # Generate log file name with timestamp
    log_file = f"Services-{datetime.now().strftime('%Y-%m-%d %H-%M')}.txt"
    log_file_path = os.path.join(log_path, log_file)

    # Ensure log directory exists
    os.makedirs(log_path, exist_ok=True)

    # Read services list from CSV
    services_list = pd.read_csv(services_file_path)

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
    with open(log_file_path, 'a') as log:
        for index, row in services_list.iterrows():
            service_name = row['Name']
            desired_status = row['Status']
            current_status = get_service_status(service_name)

            if desired_status.lower() != current_status.lower():
                log_msg = f"Service : {service_name} is currently {current_status}, should be {desired_status}"
                print(log_msg)
                log.write(log_msg + '\n')
                log.flush()

                log_msg = f"Setting {service_name} to {desired_status}"
                print(log_msg)
                log.write(log_msg + '\n')
                log.flush()
                set_service_status(service_name, desired_status)

                after_service_status = get_service_status(service_name)
                if desired_status.lower() == after_service_status.lower():
                    log_msg = f"Action was successful: Service {service_name} is now {after_service_status}"
                    print(log_msg)
                    log.write(log_msg + '\n')
                    log.flush()
                else:
                    log_msg = f"Action failed: Service {service_name} is still {after_service_status}, should be {desired_status}"
                    print(log_msg)
                    log.write(log_msg + '\n')
                    log.flush()

    print(f"Service monitoring and logging completed. Logs are saved to {log_file_path}")

# Example usage
if __name__ == "__main__":
    services_file_path = "D:/Sushama_NewStart/Automation Project/service.csv"
    log_path = "D:/Sushama_NewStart/Automation Project/Backend/Log"
    monitor_services(services_file_path, log_path)
