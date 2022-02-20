import threading
from raw_socket import send_packet

payload = "OWNED"
dest_ip = 'xxx.xxx.xxx.xxx'	# or socket.gethostbyname('www.example.com')
port = 80
max_threads = 2

if __name__ == "__main__":

    threads = []

    for i in range(0, max_threads):
        t = threading.Thread(target=send_packet, args=(dest_ip, port, payload))
        t.start()
        threads.append(t)
		
    for t in threads:
        t.join()