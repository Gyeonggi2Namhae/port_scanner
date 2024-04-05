import socket

def get_ip():
    """
    Parameters:
    None

    Returns:
    ip_add : 현 접속 IP 주소
    e : 에러
    """
    
    try:
        # 호스트 이름
        hostname = socket.gethostname()
        # IP 주소 가져오기
        ip_add = socket.gethostbyname(hostname)
        return ip_add
    #에러 처리
    except Exception as e:
        return str(e)


# 테스트용 메인 함수
# 코드 합산시 삭제 예정
if __name__ == "__main__":
    ip_add = get_ip()
    print(ip_add)