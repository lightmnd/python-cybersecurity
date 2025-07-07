import subprocess
import optparse
import sys

ifc = "ifconfig"


def change_mac(interface, mac):
    print("[+] Changing MAC address for " + interface + " to " + mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

# # Set the inteface type
# interface = input("interface > ")

# # set mac address from prompt
# mac = input("Enter the MAC address > ")

def get_arguments():
    # Create an option parser
    opts = optparse.OptionParser()
    opts.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    opts.add_options('-m', "--mac", dest="mac", help="Mac address to change")

    # Parse the command line arguments
    verify_arguments(opts.parse_args())
    return opts.parse_args()

def verify_arguments(options):
    interface = options.interface
    mac = options.mac

    # Check if the user provided an interface
    if not interface:
        options.error("[-] Error, please provide an interface")
        sys.exit(1)

    # Check if the user provided a MAC address
    if not mac:
        options.error("[-] Error, please provide a MAC Address")
        sys.exit(1)

# uncomment to print the current ifconfig status
# subprocess.call(ifc, shell=True)

# Set the MAC address of the WLAN interface

# =================================================================
# The commented comand below is more insecure because is subject to the hijacking attack
# subprocess.call(ifc +  interface + "up", shell=True)

# for example I can pass different concatenated commands to the input shell
# Eg: interface > ifconfig;ls;cat /path/to/file

# Run the change_mac function
(interface, mac) = get_arguments()
change_mac(interface, mac)

# =================================================================

# Print wlan ifconfig status
wlan_status = subprocess.check_output([ifc, interface], universal_newlines=True)
print(wlan_status)

# Execute the port scanning with NMAP  
nmap_output = subprocess.check_output(["nmap", "-p-", "--open", "192.168.1.1", "-V"], universal_newlines=True)
print(nmap_output)

# Execute the vuln scanning with NMAP
vuln_output = subprocess.check_output(["nmap", "--script vuln", "192.168.1.1", "-V"], universal_newlines=True)
print(vuln_output)