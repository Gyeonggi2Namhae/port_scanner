from scapy.all import *

import db

def well_known_port_scan(target):
    ports_info = db.get_all_list()
    scan_result = []

    for port_info in ports_info[:19]:
        port = port_info['port_number']
        try:
            ip = IP(dst=target)
            tcp = TCP(dport=port, flags="S")
            packet = ip / tcp
            response = sr1(packet, timeout=2, verbose=0)

            if response is None:
                status = 'none'
            elif response.haslayer(TCP):
                if response.getlayer(TCP).flags == 0x12:
                    status = 'open'
                elif response.getlayer(TCP).flags == 0x14:
                    status = 'closed'
        except Exception as e:
            print(f"{target}:{port} - {e}")
            status = 'error'

        scan_result.append({
            "port": port,
            "status": status,
            "service": port_info['service_name'],
            "description": port_info['port_description']
        })

    return scan_result
