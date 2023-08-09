import socket
import nmap

def scan_port(host):
    open_ports = []
    closed_ports = []
    try:
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)  #Timeout para 0.5 segundos
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            else:
                closed_ports.append(port)
            sock.close()
        print(f"Portas abertas em {host}: {', '.join(map(str, open_ports))}")
        print(f"Portas fechadas em {host}: {', '.join(map(str, closed_ports[:20]))} ...")  #Mostrando apenas as 20 primeiras portas fechadas para evitar saídas muito longas
    except KeyboardInterrupt:
        print("Scanner interrompido pelo usuário")
        exit()
    except socket.gaierror:
        print("O nome do host não pôde ser resolvido")
        exit()
    except socket.error:
        print("Erro ao tentar se conectar ao host")
        exit()

def scan_network_range(network_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_range, arguments='-O')

    for host in nm.all_hosts():
        ip = nm[host]['addresses']['ipv4']
        print(f"Host: {host}")

def main():
    choice = input("Escolha uma opção:\n1 - Port Scan\n2 - Scan de Rede\nDigite o número da opção: ")

    if choice == '1':
        host = input("Digite o IP do host para a varredura de porta: ")
        scan_port(host)
    elif choice == '2':
        network_range = input("Digite o range da rede (exemplo: 192.168.1.0/24): ")
        scan_network_range(network_range)
    else:
        print("Opção inválida")

if __name__ == "__main__":
    main()
