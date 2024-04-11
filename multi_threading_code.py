import threading
import socket
import time


resultLock = threading.Semaphore(value = 1) # 결과 출력을 제어하는 세마포어
maxConnection = 15000 # 스레드 개수를 제어하는 세마포어
connection_lock = threading.BoundedSemaphore(value=maxConnection)
scan_result = {}

def portscan(target_ip, portnum):
    try:                        # 접속 시도
        with socket.socket() as s:
            data = None
            
            s.settimeout(1)
            s.connect((target_ip, portnum))
            s.send("Python Connect\n".encode())

            data = s.recv(1024).decode()
    except Exception as e:
        if str(e) == "timed out":
                data = str(e)
        else : data = 'error'
    finally:
        if data == None:
            data = "no_data"
        elif data == "error":
            connection_lock.release()
            return
        resultLock.acquire() # 출력 세마포어 설정
        if data != "timed out" : print(f"[+] Port {portnum} opened : {data[:20].strip()}")
        # 프린트 할 부분 (배너 서비스 정보를 가져와서 출력)
        resultLock.release() # 출력 세마포어 해제
        scan_result[portnum] = data
        connection_lock.release()

def main():
    target_ip = "127.0.0.1" # 스캔 대상 (웹에서 가져옴)

    for portNum in range(65536): # 반복문 수행 -> 풀스캔
        connection_lock.acquire()
        t = threading.Thread(target=portscan, args =(target_ip, portNum)) # 쓰레드 초기화
        t.start() # 스레드 실행
    time.sleep(1)

    print(scan_result)


if __name__ == "__main__":
    startTime = time.time()
    main()
    print("exceuted Time:", (time.time()-startTime))
    portscan # 여기부터 다시 개발