# netmonitor
A command-line application that uses the proc directory to analyze the network traffic generated and received by a process. 

### Purpose
The purpose of this program is to learn how the /proc file system works. Specifically, the directory of a process /proc/[\pid\]/net is studied and leveraged to display the network activities of a process. A Tangible user interface (TUI) program is developed which uses the  /proc/[\pid\]/net directory to monitor the network activities of a process chosen by the user. 

### Installation
Make sure Python’s rich library is installed on your system. 
Run either of the following commands to install the rich library (in case one of the commands doesn’t work):

pip install rich 
sudo apt install python3-rich 

### Running
Execute the following command on a terminal to start the program:
python3 netmonitor.py <\PID\>

### Command Line Arguments
| Variable | Purpose                            |
|----------|------------------------------------|
| pid      | The pid of the process to monitor  |

## Examples
### Starting
The following figure shows an instance of starting the program on the command line:
![Example 1](./docs/images/2-example1.png)

### Selecting a Tab
The following figure shows an instance of selecting a tab:
![Example 2](./docs/images/3-example2.png)

### Terminating 
The following figure shows an instance of terminating the program by pressing CTRL+D key combination:
![Example 3](./docs/images/4-example3.png)

#### Data Types
##### Arguments
Purpose: To hold the unparsed command-line argument information
| Field     | Type | Description         |
|----------|------|---------------------|
| argv     | str  | The arguments       |
| argv[\0\]  | str  | File name           |
| argv[\1\]  | str  | PID of program.     |

##### Context
Purpose: To hold the arguments, settings, and exit information
| Field           | Type | Description                                         |
|----------------|------|-----------------------------------------------------|
| refresh_interval | int  | Period in seconds when the values are refreshed.    |

##### States
| State         | Description                                               |
|---------------|-----------------------------------------------------------|
| START         | Program started.                                          |
| NO_PID        | PID not provided as a command line argument.              |
| INVALID_PID   | Invalid PID given.                                        |
| FAIL_EXIT     | Program exits due to improper configuration.              |
| NO_SELECTION  | User has not made a selection yet.                        |
| TAP_SELECTED  | One of the tab options has been selected by the user.     |
| REFRESHING    | Current tab selected is being refreshed.                  |
| TERMINATED    | Program session terminated by the user.                   |


##### State Table
| From State     | To State       | Function            |
|----------------|----------------|---------------------|
| START          | NO_PID         | main()              |
| START          | INVALID_PID    | main()              |
| NO_PID         | FAIL_EXIT      | main()              |
| INVALID_PID    | FAIL_EXIT      | main()              |
| START          | NO_SELECTION   | session()           |
| NO_SELECTION   | TAP_SELECTED   | posix_net_monitor() |
| NO_SELECTION   | REFRESHING     | session()           |
| REFRESHING     | TAP_SELECTED   | posix_net_monitor() |
| TAP_SELECTED   | TERMINATED     | main()              |


##### State Transition Diagram
![FSM](./docs/images/1-fsm.png)

## Testing
| Test                                                                 | Expected             | Actual                |
|----------------------------------------------------------------------|----------------------|------------------------|
| Running the program and not not providing the PID as the command line argument. | Terminate gracefully | Terminate gracefully  |
| Running the program and providing an invalid PID as the command line argument. | Terminate gracefully | Terminate gracefully  |
| Killing the process being monitored while the program is running.   | Terminate gracefully | Terminate gracefully  |
| Happy path: normal usage.                                           | Works properly       | Works properly        |


## Walk-through











