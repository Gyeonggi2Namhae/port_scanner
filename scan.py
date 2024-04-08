from scapy.all import *

import db

ports = db.get_well_known_port()

def well_known_port_scan(target):
    ports_info = db.get_all_list()

    scan_result = []
    for port_info in ports_info:
        port = port_info['port_number']
        try:
            ip = IP(dst=target)
            tcp = TCP(dport=port, flags="S")
            packet = ip/tcp
            response = sr1(packet, timeout=2, verbose=0)
            if response is None:
                status = 'none'
            elif response.haslayer(TCP): # TCP레이어 존재 여부 확인
                if response.getlayer(TCP).flags == 0x12: # 해당 레이어의 flag 확인
                    status = 'open'
                elif response.getlayer(TCP).flags == 0x14:
                    status = 'closed'
        except Exception as e:
            print(f"{target}:{port} - {e}")
            
        scan_result.append({
            "port": port,
            "status": status,
            "service": port_info['service_namea'],
            "description": port_info['port_description']
        })
    return scan_result
        