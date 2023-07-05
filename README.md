# refineCommands

This Python script automates the process of connecting to Cisco switches, running show commands, and saving the output to individual files named after the hostname and timestamp.

## Requirements

- Python 3.6 or above
- `netmiko` library (install using `pip install netmiko`)

## Usage

1. Prepare the CSV files:
   - **ip_addresses.csv**: Contains a list of hostnames and IP addresses in the format: `Hostname,IP`.
   - **commands.csv**: Contains a list of show commands to run on the switches in the format: `Command`.

2. Modify the script:
   - Open `script.py` and replace the placeholder values (`your_username`, `your_password`, `your_enable_password`) in the `process_host` function with your actual login credentials for the Cisco switches.

3. Run the script:
   - Open a terminal or command prompt and navigate to the directory containing the script.
   - Execute the command: `python script.py`

4. Output:
   - The script establishes SSH connections to the switches listed in `input.csv` and executes the show commands specified in `commands.csv`.
   - The output of each switch is saved to a separate text file named after the hostname and timestamp (e.g., `Switch1_20230704_120000.txt`).

## Performance Optimization

For processing a large number of hosts, the script has been optimized using parallel processing. It utilizes the `multiprocessing` module to establish multiple SSH connections and run show commands simultaneously, significantly reducing the overall execution time.

The number of parallel processes created can be adjusted by modifying the `processes` parameter when creating the process pool in the `main` function.

## License

This script is released under the MIT License. See [LICENSE](LICENSE) for more information.
