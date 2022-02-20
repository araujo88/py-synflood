import array

def checksum(packet):
    if len(packet) % 2 != 0:
        packet += b'\0' 
    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff