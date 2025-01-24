import platform
import subprocess

def install_wazuh_agent():
    # Get platform details
    system = platform.system()
    
    # Get user inputs for Wazuh configuration
    wazuh_manager = '23.239.16.27'
    wazuh_agent_group = input("Enter the Wazuh Agent Group: ")
    wazuh_agent_name = input("Enter the Wazuh Agent Name: ")
    
    if system == "Windows":
        print("Detected Windows platform.")
        
        # Define the installation command
        install_command = (
            f"Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.7.5-1.msi "
            f"-OutFile ${{env:TMP}}\\wazuh-agent.msi; msiexec.exe /i ${{env:TMP}}\\wazuh-agent.msi /q "
            f"WAZUH_MANAGER='{wazuh_manager}' WAZUH_AGENT_GROUP='{wazuh_agent_group}' "
            f"WAZUH_AGENT_NAME='{wazuh_agent_name}' WAZUH_REGISTRATION_SERVER='{wazuh_manager}'"
        )

        # Start Wazuh agent command
        start_command = "NET START WazuhSvc"

        try:
            print("Installing Wazuh agent...")
            subprocess.run(["powershell", "-Command", install_command], check=True)
            print("Starting Wazuh agent...")
            subprocess.run(["powershell", "-Command", start_command], check=True)
            print("Wazuh agent installation completed successfully.")
            print("Please configure the ossec.conf file manually using the following path:")
            print("C:\\Program Files (x86)\\ossec-agent\\ossec.conf")
        except subprocess.CalledProcessError as e:
            print(f"Error during installation or startup on Windows: {e}")

    elif system == "Linux":
        print("Detected Linux platform.")
        
        # Define the installation command
        install_command = (
            f"wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.7.5-1_arm64.deb -O wazuh-agent.deb "
            f"&& sudo WAZUH_MANAGER='{wazuh_manager}' WAZUH_AGENT_GROUP='{wazuh_agent_group}' "
            f"WAZUH_AGENT_NAME='{wazuh_agent_name}' dpkg -i ./wazuh-agent.deb"
        )

        # Reload daemon and enable/start Wazuh agent
        reload_command = "sudo systemctl daemon-reload"
        enable_command = "sudo systemctl enable wazuh-agent"
        start_command = "sudo systemctl start wazuh-agent"

        try:
            print("Installing Wazuh agent...")
            subprocess.run(install_command, shell=True, check=True)
            print("Reloading systemd daemon...")
            subprocess.run(reload_command, shell=True, check=True)
            print("Enabling Wazuh agent...")
            subprocess.run(enable_command, shell=True, check=True)
            print("Starting Wazuh agent...")
            subprocess.run(start_command, shell=True, check=True)
            print("Wazuh agent installation completed successfully.")
            print("Please configure the ossec.conf file manually. Example commands:")
            print("sudo nano /var/ossec/etc/ossec.conf")
        except subprocess.CalledProcessError as e:
            print(f"Error during installation or startup on Linux: {e}")

    else:
        print("Unsupported operating system. This script supports only Windows and Linux.")

if __name__ == "__main__":
    install_wazuh_agent()
