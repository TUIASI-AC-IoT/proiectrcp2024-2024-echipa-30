import socket
import struct
import time

# Configurare adresa multicast si portul RIP
RIP_MULTICAST_GROUP = "224.0.0.9"
RIP_PORT = 520

# Structura pentru stocarea topologiei retelei
topologie = {}
max_hops = 16

def create_rip_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", RIP_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(RIP_MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock

def build_rip_message():
    rip_header = struct.pack("!BBH", 2, 2, 0)  # Command=Response (2), Version=2
    entries = b""

    for ip, info in topologie.items():
        ip_bytes = struct.unpack("!I", socket.inet_aton(ip))[0]
        mask_bytes = struct.unpack("!I", socket.inet_aton(info["masca"]))[0]
        next_hop_bytes = struct.unpack("!I", socket.inet_aton(info["next_hop"]))[0]
        metric = info["metric"]

        entries += struct.pack("!HHIIII", 2, 0, ip_bytes, mask_bytes, next_hop_bytes, metric)

    return rip_header + entries



def send_rip_message(sock):
    message = build_rip_message()
    neighbors = ["192.168.1.2"]  # Adresele vecinilor din retea

    for neighbor in neighbors:
        sock.sendto(message, (neighbor, 520))
        print(f"Mesaj RIPv2 trimis catre {neighbor}")


def parse_rip_message(data, addr):
    global topologie
    global max_hops
    rip_header = data[:4]
    entries = data[4:]

    command, version, _ = struct.unpack("!BBH", rip_header)
    if command != 2 or version != 2:
        print(f"Mesaj ignorat de la {addr}: Nu este RIPv2 Response.")
        return

    print(f"Mesaj valid RIPv2 primit de la {addr}")
    num_entries = len(entries) // 20

    for i in range(num_entries):
        offset = i * 20
        afi, route_tag, ip, mask, next_hop, metric = struct.unpack("!HHIIII", entries[offset:offset + 20])
        ip_addr = socket.inet_ntoa(struct.pack("!I", ip))
        mask_addr = socket.inet_ntoa(struct.pack("!I", mask))
        next_hop_addr = addr[0]  # Adresa sursa a pachetului
        metric = metric + 1  # Adaugam 1 la metric (costul)
        if metric > max_hops:
            print(f"Ruta catre {ip_addr} este inaccesibila (metric > {max_hops}).")
            continue
        # Actualizam ruta daca este noua sau daca avem un cost mai mic
        if ip_addr not in topologie or topologie[ip_addr]["metric"] > metric:
            topologie[ip_addr] = {
                "masca": mask_addr,
                "next_hop": next_hop_addr,
                "metric": metric
            }



def receive_rip_message(sock):
    """
    Primeste mesaje RIPv2 si actualizeaza topologia.
    """
    sock.settimeout(5)
    try:
        data, addr = sock.recvfrom(1024)
        parse_rip_message(data, addr)
    except socket.timeout:
        pass

def display_topology():
    print("\n=== Topologia Retelei Descoperite ===")
    for ip, info in topologie.items():
        print(f"Destinatie: {ip}, Masca: {info['masca']}, Next Hop: {info['next_hop']}, Metric: {info['metric']}")
    print("====================================")


def main():
    global max_hops
    sock = create_rip_socket()
    print("Socket-ul RIP este configurat si activ.")

    # Adauga ruta locala in topologie
    topologie["192.168.1.0"] = {
        "masca": "255.255.255.0",
        "next_hop": "0.0.0.0",
        "metric": 1
    }
    update_time = 5
    option = 1
    while option:
        try:
            while True:
                send_rip_message(sock)
                receive_rip_message(sock)
                display_topology()
                time.sleep(update_time)
        except KeyboardInterrupt:
            option=int(input("\n1-modificare update time\n2-modificare limita de distanta(max_hops)\n3-anulare\n0-exit\n"))
            if option==1:
                update_time=int(input("\nnoua valoare pentru update time:"))
            elif option==2:
                max_hops=int(input("\nnoua valoare pentru max_hops:"))
            elif not option:
                print("Inchidere socket.")
                sock.close()
                break

if __name__ == "__main__":
    main()
