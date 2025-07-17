import subprocess, re, os, sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
import time
from rich.console import Console
from rich.panel import Panel
from rich import box
import signal




def get_posix_entries(path_str):
    path = Path(path_str)

    if path.is_dir():

        files = [file.as_posix() for file in path.iterdir() if file.is_file()]
        directories = [directory.as_posix() for directory in path.iterdir() if directory.is_dir()]

        return {'directories': directories, 'files': files}

    else:
        return None



def hex_ip_port_to_dec(ip_port_hex):
    hex_ip,hex_port = ip_port_hex.split(':')
    ip = ".".join(str(int(hex_ip[i:i+2], 16)) for i in range(6, -1, -2))
    port = int(hex_port, 16)
    return f'{ip}:{port}'



def tcp(parent_path_str, entries):
    states = {'01': 'ESTABLISHED', '02': 'SYN_SENT', '03': 'SYN_RECV', '04': 'FIN_WAIT1',
    '05': 'FIN_WAIT2', '06': 'TIME_WAIT', '07': 'CLOSE',
    '08': 'CLOSE_WAIT', '09': 'LAST_ACK', '0A': 'LISTEN', '0B': 'CLOSING'}

    parh_str = f'{parent_path_str}/tcp'
    if parh_str not in entries['files']:
        return None

    result = subprocess.run(['cat', parh_str], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    data = [line.split() for line in lines]

    table = Table(title="Formatted TCP")
    for header in data[0]:
        table.add_column(header, justify="left")


    for row in data[1:]:
       row[1] = hex_ip_port_to_dec(row[1])
       row[2] = hex_ip_port_to_dec(row[2])
       row[3] = states.get(row[3], row[3])
       table.add_row(*row)

    console = Console()
    console.print(table)






def udp(parent_path_str, entries):
    states = {'00': 'Unused', '01': 'ESTABLISHED', '07': 'Listening'}
    path_str = f'{parent_path_str}/udp'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    data = [line.split() for line in lines]

    table = Table(title="Formatted UDP")
    for header in data[0]:
        table.add_column(header, justify="left")
    for row in data[1:]:
        row[1] = hex_ip_port_to_dec(row[1])
        row[2] = hex_ip_port_to_dec(row[2])
        row[3] = states.get(row[3], row[3])
        table.add_row(*row)

    console = Console()
    console.print(table)



def stat_arp_cache(parent_path_str, entries):
    file_path_str = f'{parent_path_str}/stat/arp_cache'
    dir_path_str = f'{parent_path_str}/stat'
    if  dir_path_str not in entries['directories']:
        return None
    if file_path_str not in get_posix_entries(dir_path_str)['files']:
        return None

    result = subprocess.run(['cat', file_path_str], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    data = [line.split() for line in lines]

    table = Table(title="Formatted ARP Cache")
    for header in data[0]:
        table.add_column(header, justify="left")
    for row in data[1:]:
        table.add_row(*row)

    console = Console()
    console.print(table)


def netstat(parent_path_str, entries):
    path_str = f'{parent_path_str}/netstat'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout
    data = {}
    lines = text.strip().split("\n")
    for i in range(0, len(lines), 2):  # Process two lines at a time
        header = lines[i].split(":")[0]
        fields = lines[i].split(":")[1].strip().split()
        values = lines[i + 1].split(":")[1].strip().split()
        data[header] = dict(zip(fields, values))

    console = Console()

    for section, values in data.items():
        table = Table(title=f"{section} Section", show_lines=True)
        table.add_column("Field")
        table.add_column("Value", justify="right")
        for field, value in values.items():
            table.add_row(field, value)
        console.print(table)




def dev(parent_path_str, entries):
    path_str = f'{parent_path_str}/dev'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout.strip()
    lines = text.splitlines()
    header_tokens = lines[1].split()
    loopback_tokens = lines[2].split()
    nic_tokens = lines[3].split()

    table = Table(title="Formatted device stats")
    for header in header_tokens:
        table.add_column(header, justify="left")

    for row in [loopback_tokens, nic_tokens]:
        table.add_row(*row)

    console = Console()
    console.print(table)


def raw(parent_path_str, entries):
    path_str = f'{parent_path_str}/raw'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout.strip()
    lines = text.splitlines()
    data = [line.split() for line in lines]

    table = Table(title="Formatted Raw")
    for header in data[0]:
        table.add_column(header, justify="left")
    for row in data[1:]:
        table.add_row(*row)

    console = Console()
    console.print(table)



def icmp(parent_path_str, entries):
    path_str = f'{parent_path_str}/icmp'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout.strip()
    lines = text.splitlines()
    data = [line.split() for line in lines]

    table = Table(title="ICMP Raw")
    for header in data[0]:
        table.add_column(header, justify="left")
    for row in data[1:]:
        table.add_row(*row)

    console = Console()
    console.print(table)



def snmp(parent_path_str, entries):
    path_str = f'{parent_path_str}/snmp'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout.strip()

    lines = text.strip().split("\n")
    data = {}
    for i in range(0, len(lines), 2):  # Process in pairs of lines
        header_line = lines[i]
        values_line = lines[i + 1]

        # Extract protocol name and keys
        protocol, *keys = header_line.split(":")[1].strip().split()
        # Extract values
        values = values_line.split(":")[1].strip().split()

        # Create a dictionary for the protocol
        data[protocol] = dict(zip(keys, values))


    parsed_data = data
    # Display the parsed data using Rich
    console = Console()
    for protocol, metrics in parsed_data.items():
        table = Table(title=f"{protocol} Metrics", show_lines=True)
        table.add_column("Metric")
        table.add_column("Value", justify="right")

        for metric, value in metrics.items():
            table.add_row(metric, value)

        console.print(table)





def softnet_stat(parent_path_str, entries):
    """
        Each row corresponds to a CPU, and each column represents a specific counter.
        Column 1 (Processed Packets), Column 2 (Dropped Packets), column 3 (Time Squeezes),
        Column 4 (CPU Collisions), Columns 5–12:(kernel specific), Column 13 (Received RPS Packets), Column 14 and 15 (Reserved).
    """
    path_str = f'{parent_path_str}/softnet_stat'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout.strip()
    lines = text.splitlines()
    table2d = [line.split() for line in lines]
    data = [[f'CPU {i}'] + table2d[i-1]for i in range(1, len(table2d) + 1)]
    #print(data)

    integer = lambda x: str(int(x, 16))

    table = Table(title="Packet Stats Per CPU")
    for header in ['CPU', 'Processed Packets', 'Dropped Packets', 'Time Squeezes', 'CPU Collisions', 'Received RPS Packets']:
        table.add_column(header, justify="left")
    for row in data:
        table.add_row(*[row[0], integer(row[1]), integer(row[2]), integer(row[3]), integer(row[4]), integer(row[13])])


    console = Console()
    console.print(table)

def route(parent_path_str, entries):
    path_str = f'{parent_path_str}/route'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout.strip()

    lines = text.splitlines()
    data = [line.split() for line in lines]


    table = Table(title="Routes")
    for header in data[0]:
        table.add_column(header, justify="left")
    for row in data[1:]:
        table.add_row(*row)

    console = Console()
    console.print(table)



def arp(parent_path_str, entries):
    path_str = f'{parent_path_str}/arp'
    if path_str not in entries['files']:
        return None

    result = subprocess.run(['cat', path_str], capture_output=True, text=True)
    text = result.stdout.strip()

    lines = text.splitlines()
    data = [line.split() for line in lines]


    table = Table(title="Host ARP")
    for header in data[0]:
        table.add_column(header, justify="left")
    for row in data[1:]:
        table.add_row(*row)

    console = Console()
    console.print(table)







def posix_net_monitor(pid, selection):
    path_str = f'/proc/{pid}/net'
    entries = get_posix_entries(path_str)
    if entries == None:
        raise Exception(f"Failed to access {path_str}.")

    if 'tcp' == selection:
        tcp(path_str, entries)
    elif 'udp' == selection:
        udp(path_str, entries)
    elif 'arp' == selection:
        stat_arp_cache(path_str, entries)
        arp(path_str, entries)
    elif 'traffic' == selection:
        dev(path_str, entries)
    elif 'stats' == selection:
        netstat(path_str, entries)
    elif 'raw' == selection:
        raw(path_str, entries)
    elif 'icmp' == selection:
        icmp(path_str, entries)
    elif 'routing' == selection:
        route(path_str, entries)
    elif 'analysis' == selection:
        snmp(path_str, entries)
        softnet_stat(path_str, entries)
    else:
        raise Exception(f"Unkown selection: {selection}.")



def session(pid):
    """
    - The user can choose from predefined options.
    - Only the selected option is displayed on the screen.
    - The user can change the refresh interval by typing: set <seconds>
    - Pressing CTRL+D (sending EOF) will exit the program.
    """
    
    if get_posix_entries(f'/proc/{pid}/net') == None:
        raise Exception(f"Directory /proc/{pid}/net' does not exist.")

    
    console = Console()

    # Predefined options
    options = ['tcp', 'udp', 'arp', 'traffic', 'stats', 'raw', 'icmp', 'routing', 'analysis']

    # Default selected option
    selected_option = "tcp"

    # Default refresh interval (in seconds)
    refresh_interval = 5

    # Introduction
    console.print("[bold magenta]Welcome to the NetStat Dashboard[/bold magenta]")
    console.print(
        "Press [bold red]CTRL+D[/bold red] at any time to exit.\n"
        "You can choose one of the following options: [bold green]tcp[/bold green], [bold green]udp[/bold green], [bold green]arp[/bold green], [bold green]traffic[/bold green], [bold green]stats[/bold green], [bold green]raw[/bold green], [bold green]icmp[/bold green], [bold green]routing[/bold green], and [bold green]analysis[/bold green] \n"
        "Or type [italic]'set <seconds>'[/italic] to configure the refresh interval.",
        style="bold blue"
    )

    try:
        _ = console.input("[bold blue]Press any key to contiune . . .[/bold blue] ")
    except (EOFError, KeyboardInterrupt):
        return # CTRL+D / EOF  or CTRL+C was pressed, break out of the loop

    def timeout_handler(signum, frame):
        raise TimeoutError("Input timed out!")

    signal.signal(signal.SIGALRM, timeout_handler)

    console.clear()

    while True:
     

        # Build a panel showing the currently selected option and interval
        panel = Panel.fit(
            f"Selected Option: [bold yellow]{selected_option}[/bold yellow]\n"
            f"Refresh Interval: [bold cyan]{refresh_interval}[/bold cyan] seconds",
            title="[bold green]Current State[/bold green]",
            border_style="bright_magenta",
            box=box.ROUNDED
        )

        console.print(panel)





        user_input = selected_option
        try:
            signal.alarm(refresh_interval)  
            user_input = console.input("[bold blue]Enter an option [bold green]tcp[/bold green], [bold green]udp[/bold green], [bold green]arp[/bold green], [bold green]traffic[/bold green], [bold green]stats[/bold green], [bold green]raw[/bold green], [bold green]icmp[/bold green], [bold green]routing[/bold green], and [bold green]analysis[/bold green] or 'set <seconds>': [/bold blue] ")
        except (EOFError, KeyboardInterrupt):
            # CTRL+D / EOF  or CTRL+C was pressed, break out of the loop
            break
        except TimeoutError:
            pass

        signal.alarm(0)  # Disable alarm after input


        user_input = user_input.strip()

        # If the user enters one of the predefined options, update the selected_option
        if user_input.lower() in options:
            selected_option = user_input.lower()


        # If the user tries to set the refresh interval
        elif user_input.lower().startswith("set"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                try:
                    refresh_interval = int(parts[1])
                except ValueError:
                    console.print("[bold red]Invalid refresh interval![/bold red]")
            else:
                console.print("[bold red]Usage: set <seconds>[/bold red]")
        elif user_input:
            console.print("[bold red]Invalid input. Please try again.[/bold red]")

        console.clear()        
        posix_net_monitor(pid, selected_option)
    # print a new line 
    print()



def main():
    if len(sys.argv) < 2:
        print("Error: No command-line argument provided.")
        print("Usage: python script.py <arg>")
        sys.exit(1)

    try:
        session(sys.argv[1])

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)






if __name__ == "__main__":
    main()















