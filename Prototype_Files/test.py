from scapy.all import *
import Jobs

#print("Working 0")
#target_ip = "192.168.2.1/24"
# IP Address for the destination
# create ARP packet
#arp = ARP(pdst=target_ip)
# create the Ether broadcast packet
# ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
#ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# stack them
#packet = ether/arp

#print("Working 1")
#result = srp(packet, timeout=3, verbose=0)[0]
#print("Working 2")
## a list of clients, we will fill this in the upcoming loop
#clients = []
#print("Working 3")
#for sent, received in result:
#    # for each response, append ip and mac address to `clients` list
#    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

#packets = []
#icmp_layer = ICMP(seq = 9999)
#for client in clients:
#    ip_layer = IP(dst=client['ip'])
#    packets.append(ip_layer/icmp_layer)


#send(packets)
print("Hello")
jobb = Jobs.ICMPFlood('192.168.2.10')
jobb.setJobTaker("Matteus")
jobb.addJobTaker("Nick")


for name in jobb.jobTaker:
     print(name)