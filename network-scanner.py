import scapy.all as scapy

# This script scans a network for active devices and their MAC addresses.
# It uses the Scapy library to send ARP requests and receive responses.
# To run this script, you   need to have Scapy installed and run it with root privileges
# (e.g., using `sudo` on Linux or macOS).

# use optparse to parse command line arguments
import optparse
parser = optparse.OptionParser("usage: python3 network_scanner.py -i <ip_address>")
parser.add_option("-t", "--target", dest="ip_address", type="string", help="specify the IP address to scan")
ip = ""
cidr_range = ""
(opts, args) = parser.parse_args()

if opts.ip_address is not None:
    ip = opts.ip_address
else:
    print(parser.usage)
    exit(0)

if len(args) > 0:
    # if there are extra arguments, we assume they are CIDR ranges
    # and we set cidr_range to the first argument
    cidr_range = args[0]
else:
    #error, stop the program and show an error message
    print("Error: No CIDR range provided. Please provide a CIDR range as an argument.")
    exit(1)

def scan(ip, cidr_range):
    full_ip = ip + "/" + cidr_range
    arp_request = scapy.ARP(pdst=full_ip)
    # scapy.ls(arp_request) # Uncomment to see the fields of the ARP request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
    client_dict_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_dict_list.append(client_dict)
    return print_result(client_dict_list)
   
def print_result(client_res):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for index in range(len(client_res)):
        print(f"{client_res[index]['ip']}\t\t{client_res[index]['mac']}\n")
        print("--------------------------------------------------\n")
    
scan(ip, cidr_range)
