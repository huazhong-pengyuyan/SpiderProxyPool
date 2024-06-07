from proxypool.schemas.proxy import Proxy


def is_valid_proxy(data):
    """
    check 获取后的代理地址的合法性，且return ip:host
    :param data: ip:host
    :return: 合法性：bool值
    """
    if is_auth_proxy(data):
        host, port = extract_auth_proxy(data)
        return is_ip_valid(host) and is_port_valid(port)
    elif data.__contains__(':'):  # 判断data是否包含:
        ip = data.split(':')[0]
        port = data.split(':')[1]
        return is_ip_valid(ip) and is_port_valid(port)
    else:
        return is_ip_valid(data)


def is_ip_valid(ip) -> bool:
    """
    检查ip是否合法
    :param ip:
    :return:
    """
    if is_auth_proxy(ip):
        ip = ip.split('@')[1]
    a = ip.split('.')
    # a 等于 [1，2，3，4]
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():  # isdigit判断字符串是够只有数字 返回True 否则False
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def is_port_valid(port) -> bool:
    return port.isdigit()


def convert_proxy_or_proxies(data):
    """
    遍历下来的代理ip，单个地址和地址列表都做了处理
    :param data: ip or [ip, ip, ip]
    :return: @username:password and prot
    or ip and port
    """
    if not data:
        return None
    if isinstance(data, list):  # isinstance 检查data是否为list
        result = []
        for item in data:
            item = item.strip()
            if not is_valid_proxy(item): continue
            if is_auth_proxy(item):
                host, port = extract_auth_proxy(item)
            else:
                host, port, *_ = item.split(':')
            result.append(Proxy(host, port))
        return result
    if isinstance(data, str) and is_valid_proxy(data):
        if is_auth_proxy(data):
            host, port = extract_auth_proxy(data)
        else:
            host, port = data.split(':')
        return Proxy(host, port)


def is_auth_proxy(data: str) -> bool:
    """
    判断认证@
    :param data:
    :return:
    """
    return '@' in data


def extract_auth_proxy(data: str) -> (str, int):
    """
    域名进行拆分，比如 user:password@url:port
    :param data:
    :return: (user:password@url, port)
    """
    auth = data.split('@')[0]
    ip_port = data.split('@')[1]
    ip = ip_port.split(':')[0]
    port = ip_port.split(':')[1]
    host = auth + '@' + ip
    return host, port


if __name__ == '__main__':
    proxy = 'test123:test456@127.0.0.1:1234'
    proxies = ['test123:test456@127.0.0.1:1234', 'test123:test456@127.0.0.1:1234']
    print(convert_proxy_or_proxies(proxies))
    print(is_valid_proxy(proxy))