import socket
import threading


class UntoldNet:
    """untold.net — Network & socket module"""

    @staticmethod
    def tcp_connect(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        return s

    @staticmethod
    def tcp_send(sock, data):
        if isinstance(data, str):
            data = data.encode()
        sock.send(data)

    @staticmethod
    def tcp_recv(sock, size=4096):
        return sock.recv(int(size)).decode(errors="replace")

    @staticmethod
    def tcp_close(sock):
        sock.close()

    @staticmethod
    def tcp_server(host, port, handler):
        """Start a TCP server. handler(conn, addr) is called per connection."""
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, int(port)))
        srv.listen(5)
        print(f"[untold.net] TCP server listening on {host}:{port}")
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=handler, args=(conn, addr), daemon=True)
            t.start()

    @staticmethod
    def udp_send(host, port, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if isinstance(data, str):
            data = data.encode()
        s.sendto(data, (host, int(port)))
        s.close()

    @staticmethod
    def udp_recv(port, size=4096):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", int(port)))
        data, addr = s.recvfrom(int(size))
        s.close()
        return {"data": data.decode(errors="replace"), "from": str(addr)}

    @staticmethod
    def resolve(hostname):
        return socket.gethostbyname(hostname)

    @staticmethod
    def my_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()

    @staticmethod
    def port_open(host, port, timeout=2):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((host, int(port)))
            s.close()
            return True
        except:
            return False

    @staticmethod
    def scan_ports(host, start, end):
        """Scan a port range. Returns list of open ports."""
        open_ports = []
        for port in range(int(start), int(end) + 1):
            if UntoldNet.port_open(host, port, timeout=0.5):
                open_ports.append(port)
        return open_ports
