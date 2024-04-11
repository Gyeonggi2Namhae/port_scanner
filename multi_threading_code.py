import threading
import socket
import time

# 세마포어 및 기타 설정
resultLock = threading.Semaphore(value=1)
maxConnection = 15000
connection_lock = threading.BoundedSemaphore(value=maxConnection)

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
                scan_result.append({'port': portnum, 'status': status, 'service': data.split()[0], 'description': None})
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
