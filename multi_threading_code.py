import threading
import socket
import db

# 세마포어 및 기타 설정
resultLock = threading.Semaphore(value=1)
maxConnection = 3000
connection_lock = threading.BoundedSemaphore(value=maxConnection)

def well_known_scan(target_ip):
    ports_info = db.get_all_list()  # DB에서 포트 정보를 가져옴
    scan_result = []
    threads = []

    def portscan(port_info):
        portnum = port_info['port_number']
        servicename = port_info['service_name']  # 서비스 이름을 DB에서 가져옴
        status = 'closed'
        desc = port_info['port_description']
        try:
            with socket.socket() as s:
                s.settimeout(1)
                s.connect((target_ip, portnum))
                s.send("Python Connect\n".encode())
                data = s.recv(1024).decode()
                if data:
                    status = 'open'
        except Exception as e:
            if str(e) == "timed out":
                data = str(e)
            else:
                data = 'error'
        finally:
            resultLock.acquire()
            if status == 'open':
                # 스캔 결과에 서비스 이름 추가
                scan_result.append({
                    'port': portnum,
                    'status': status,
                    'service': servicename,
                    'description': desc  # 필요하다면 여기에 추가 정보 포함
                })
            resultLock.release()
            connection_lock.release()

    for port_info in ports_info:
        connection_lock.acquire()
        t = threading.Thread(target=portscan, args=(port_info,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()  # 모든 스레드의 완료를 기다림

    return scan_result

def multi_threading_scan(target_ip, port_range):
    scan_result = []
    threads = []

    def portscan(portnum):
        status = 'closed'
        try:
            with socket.socket() as s:
                s.settimeout(1)
                s.connect((target_ip, portnum))
                s.send("Python Connect\n".encode())
                data = s.recv(1024).decode()
                if data:
                    status = 'open'
        except Exception as e:
            if str(e) == "timed out":
                data = str(e)
            else:
                data = 'error'
        finally:
            resultLock.acquire()
            if status == 'open':
                scan_result.append({'port': portnum, 'status': status, 'service': data.strip(), 'description': None})
            resultLock.release()
            connection_lock.release()

    for portNum in range(*port_range):  # 스캔할 포트 범위
        connection_lock.acquire()
        t = threading.Thread(target=portscan, args=(portNum,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()  # 모든 스레드의 완료를 기다림

    return scan_result
