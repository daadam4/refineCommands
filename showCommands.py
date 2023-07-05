import csv
import datetime
from netmiko import ConnectHandler

# Function to establish SSH connection and run show commands
def run_show_commands(hostname, ip, commands):
    device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'your_username',
        'password': 'your_password',
        'secret': 'your_enable_password',
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

        return output

    except Exception as e:
        return f"Error connecting to {hostname}: {str(e)}"

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
    input_csv_file = 'input.csv'
    commands_csv_file = 'commands.csv'

    # Read hostnames and IP addresses from input CSV
    hosts = []
    with open(input_csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            hosts.append({'hostname': row[0], 'ip': row[1]})

    # Read commands from commands CSV
    commands = []
    with open(commands_csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            commands.append(row[0])

    # Connect to switches and run show commands
    for host in hosts:
        output = run_show_commands(host['hostname'], host['ip'], commands)

        # Write output to file
        write_output_file(host['hostname'], output)

if __name__ == '__main__':
    main()
