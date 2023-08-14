import socket
import concurrent.futures
import ipaddress
import subprocess

def scan_port(host, port):
    try:
        with socket.create_connection((host, port), timeout=0.5):
            print(f"Porta {port} está aberta em {host}")
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass
    return False

def scan_host_ports(host):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = list(executor.map(lambda port: scan_port(host, port), range(1, 1025)))
        open_ports = [port for port, is_open in zip(range(1, 1025), results) if is_open]
    return open_ports

def scan_network_with_ports(network_range):
    network = ipaddress.ip_network(network_range, strict=False)
    for host in network.hosts():
        if is_host_online(host):
            open_ports = scan_host_ports(str(host))
            if open_ports:
                print(f"Host {host} tem as seguintes portas abertas: {', '.join(map(str, open_ports))}")

def is_host_online(host):
    try:
        subprocess.check_output(
            ['ping', '-c', '1', '-W', '1', str(host)],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        print(f"Host online: {host}")
        return True
    except subprocess.CalledProcessError:
        return False

def scan_network_hosts(network_range):
    network = ipaddress.ip_network(network_range, strict=False)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        list(executor.map(is_host_online, network.hosts()))

def main():
    print("Escolha uma opção:")
    print("1 - Scan rápido de porta em um único host")
    print("2 - Scan da rede com descoberta de portas")
    print("3 - Verificar hosts ativos na rede")
    choice = input("Digite o número da opção: ")

    if choice == '1':
        host = input("Digite o IP do host: ")
        open_ports = scan_host_ports(host)
        if open_ports:
            print(f"Host {host} tem as seguintes portas abertas: {', '.join(map(str, open_ports))}")
        else:
            print(f"Nenhuma porta aberta encontrada em {host}.")
    elif choice == '2':
        network_range = input("Digite o range da rede (exemplo: 192.168.1.0/24): ")
        scan_network_with_ports(network_range)
    elif choice == '3':
        network_range = input("Digite o range da rede (exemplo: 192.168.1.0/24): ")
        scan_network_hosts(network_range)
    else:
        print("Opção inválida")

if __name__ == "__main__":
    main()
