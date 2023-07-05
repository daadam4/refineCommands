import csv
import datetime
from netmiko import ConnectHandler
from multiprocessing import Pool
import getpass

print("""

  _   _      _                      _      ____                  
 | \ | | ___| |___      _____  _ __| | __ / ___|  ___ __ _ _ __  
 |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ / \___ \ / __/ _` | '_ \ 
 | |\  |  __/ |_ \ V  V / (_) | |  |   <   ___) | (_| (_| | | | |
 |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\ |____/ \___\__,_|_| |_|
                                                                 
                 
"""
)

username = input("Username:")
password = getpass.getpass()

# Function to establish SSH connection and run show commands for a single host
def process_host(host):
    hostname = host['hostname']
    ip = host['ip']
    commands = host['commands']

    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
    }

    try:
        # Establish SSH connection
        net_connect = ConnectHandler(**device)
        net_connect.enable()

        # Execute show commands
        output = ""
        for command in commands:
            output += f"Command: {command}\n"
            output += net_connect.send_command(command)
            output += "\n"

        # Close SSH connection
        net_connect.disconnect()

        # Return the hostname and output
        return {'hostname': hostname, 'output': output}

    except Exception as e:
        return {'hostname': hostname, 'output': f"Error connecting to {hostname}: {str(e)}"}

# Function to write output to a file
def write_output_file(hostname, output):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{hostname}_{timestamp}.txt"

    with open(filename, 'w') as file:
        file.write(output)

    print(f"Output saved to {filename}")

# Main function
def main():
    # CSV file paths
    input_csv_file = input("Enter path to host CSV file (Press Enter to default to ./ip_addresses.csv):") or "ip_addresses.csv"
    commands_csv_file = input("Enter path to commands CSV file (Press Enter to default to ./commands.csv):") or "commands.csv"

    # Read hostnames and IP addresses from input CSV
    hosts = []
    with open(input_csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hosts.append({'hostname': row['Hostname'], 'ip': row['IP'], 'commands': []})

    # Read commands from commands CSV
    with open(commands_csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for host in hosts:
                host['commands'].append(row['Command'])

    # Create a process pool
    pool = Pool()

    # Process hosts in parallel
    results = pool.map(process_host, hosts)

    # Write output files
    for result in results:
        hostname = result['hostname']
        output = result['output']
        write_output_file(hostname, output)

if __name__ == '__main__':
    main()
