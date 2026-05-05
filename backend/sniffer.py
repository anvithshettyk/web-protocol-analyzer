from scapy.all import sniff, DNS, DNSQR, TCP
from datetime import datetime
import socket
import time

packets = []
dns_map = {}
target_ip = None
start_time = time.time()

# 🎯 Set target URL
def set_target(url):
    global target_ip
    try:
        target_ip = socket.gethostbyname(url)
    except:
        target_ip = None

def detect_protocol(packet):
    if packet.haslayer(TCP):
        dport = packet[TCP].dport
        if dport == 80:
            return "HTTP"
        elif dport == 443:
            return "HTTPS"
        else:
            return "TCP"
    elif packet.haslayer(DNS):
        return "DNS"
    return "OTHER"

def process_packet(packet):
    global target_ip

    try:
        src = packet[0][1].src
        dst = packet[0][1].dst

        # 🌍 DNS mapping
        if packet.haslayer(DNS) and packet.haslayer(DNSQR):
            domain = packet[DNSQR].qname.decode().strip('.')
            dns_map[dst] = domain

        # 🎯 Filter by target
        if target_ip:
            if src != target_ip and dst != target_ip:
                return

        protocol = detect_protocol(packet)

        packets.append({
            "time": str(datetime.now()),
            "src_ip": src,
            "dst_ip": dst,
            "protocol": protocol,
            "size": len(packet),
            "domain": dns_map.get(dst, "Unknown")
        })

    except:
        pass

def start_sniffing():
    sniff(prn=process_packet, store=False)

def get_packets():
    return packets[-300:]