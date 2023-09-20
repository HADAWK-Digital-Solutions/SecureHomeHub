#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ifaddrs.h>
#include <netinet/in.h>
#include <arpa/inet.h>

void check_network_requirements() {
    char* ip_address = "10.187.239.45"; // This should be the IP address of the device you're setting up.
    char command[100];
    char result[10];
    char subnet_str[INET_ADDRSTRLEN];


    // Query the IP subnet of the Linux machine
    struct ifaddrs* ifaddr, * ifa;
    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        return;
    }

    printf("\nIP Subnet Information:\n");
    // Iterate through the network interfaces
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == NULL || ifa->ifa_addr->sa_family != AF_INET) {
            continue;
        }

        // Skip loopback interface
        if (strcmp(ifa->ifa_name, "lo") == 0) {
            continue;
        }

        struct sockaddr_in* addr = (struct sockaddr_in*)ifa->ifa_addr;
        struct sockaddr_in* netmask = (struct sockaddr_in*)ifa->ifa_netmask;

        // Convert the IP address and netmask to strings
        const char* ip = inet_ntoa(addr->sin_addr);
        const char* mask = inet_ntoa(netmask->sin_addr);

        // Perform subnet calculation
        struct in_addr subnet;
        subnet.s_addr = addr->sin_addr.s_addr & netmask->sin_addr.s_addr;

        // Convert the subnet to a string in CIDR notation
        int prefix_length = 0;
        uint32_t mask_value = ntohl(netmask->sin_addr.s_addr);
        while (mask_value & 0x80000000) {
            prefix_length++;
            mask_value <<= 1;
        }
        sprintf(subnet_str, "%s/%d", inet_ntoa(subnet), prefix_length);

        printf("Interface: %s\n", ifa->ifa_name);
        printf("IP Address: %s\n", ip);
        printf("Netmask: %s\n", mask);
        printf("Subnet: %s\n\n", subnet_str);
    }

    freeifaddrs(ifaddr);

    // Use the subnet_str for other purposes
    printf("Subnet: %s\n", subnet_str);

    // Other setup code goes here.

    // Perform a ping test on every device on the network
    char scanSubnet[200] = "sudo nmap -v -R -sn -PE -PS80 -PU40,125 ";
    strcat(scanSubnet, subnet_str);
    strcat(scanSubnet, " -oG /usr/local/secureHomeHub/online_hosts.txt && grep \"Status: Up\" /usr/local/secureHomeHub/online_hosts.txt | awk '{print $2}' > /usr/local/secureHomeHub/online_addresses.txt");
    system(scanSubnet);

    printf("%s\n", scanSubnet);


    // Execute a command that measures the latency to the IP address.
    sprintf(command, "ping -c 4 %s | awk -F'/' '/^round-trip/ {print $5}'", ip_address);
    FILE* latency_pipe = popen(command, "r");
    if (latency_pipe == NULL) {
        printf("Error executing latency check command.\n");
        return;
    }
    fgets(result, sizeof(result), latency_pipe);
    float latency = atof(result);
    pclose(latency_pipe);

    // Execute a command that checks for packet loss to the IP address.
    sprintf(command, "ping -c 4 %s | awk -F', ' '/packet loss/ {print $3}'", ip_address);
    FILE* packet_loss_pipe = popen(command, "r");
    if (packet_loss_pipe == NULL) {
        printf("Error executing packet loss check command.\n");
        return;
    }
    fgets(result, sizeof(result), packet_loss_pipe);
    float packet_loss = atof(result);
    pclose(packet_loss_pipe);

    // Need to replace with an actual value. A placeholder
    float jitter = 30.0;
    float some_threshold = 10.0;

    // Check the latency.
    if (latency < 5.0) {
        printf("Latency Check Passed\n");
    }
    else {
        printf("Latency Check Failed\n");
    }

    // Check for packet loss.
    if (packet_loss == 1.0) {
        printf("Packet Loss Check Passed\n");
    }
    else {
        printf("Packet Loss Check Failed\n");
    }

    // Check the jitter.
    if (jitter <= some_threshold) {
        printf("Jitter Check Passed\n");
    }
    else {
        printf("Jitter Check Failed\n");
    }

}

// Perform a ping test on every device on the network
//    sprintf(command, "sudo nmap -v -R -sn -PE -PS80 -PU40,125 192.168.1.0/24 -oG /home/dwl2/Desktop/online_hosts.txt && grep \"Status: Up\" /home/dwl2/Desktop/online_hosts.txt | awk '{print $2}' > /home/dwl2/Desktop/online_addresses.txt"


int main() {
    check_network_requirements();

    return 0;
}