import socket

def get_banner(target_ip, port):
    """
    Parameters:
    target_ip(str): 타겟 IP
    port(int): 스캔할 port

    Returns:
    banner.decode().strip() : 배너값
    e : 에러
    """
    
    try:
        # 소켓 생성
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 포트 연결
        s.connect((target_ip, port))
        # 데이터 수신
        banner = s.recv(1024)
        return banner.decode().strip()
    # 에러 처리
    except Exception as e:
        return str(e)


# 테스트용 메인 함수
# 코드 합산시 수정 예정
if __name__ == "__main__":
    target_ip = "15.164.228.181"  # 타겟 IP
    # HTTP, HTTPS, SSH -> test용 세개의 포트 (all sacnning : test 시간 초과) 이후 수정 예정
    ports = [80, 443, 22] 

    for port in ports:
        banner = get_banner(target_ip, port)
        if banner:
            print(f"[{port}]port banner: {banner}")
        else:
            print(f"[{port}]port Failed ")
