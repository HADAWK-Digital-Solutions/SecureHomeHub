#include <stdio.h>
#include <stdlib.h>

void scanNetwork(char *subnet) {
    char command[50];
    
    sprintf(command, "nmap -sP %s", subnet);

    system(command);
}

void scanPorts(char *ip) {
    char command[50];
    
    sprintf(command, "nmap %s", ip);

    system(command);
}

void securityChecks(char *ip) {
    char command[100];
    
    // Check for open ports that should usually be closed.
    // In a real application, you would want to customize this list 
    // to suit the specifics of your network.
    int ports[] = {23, 3389, 22, 445};
    int size = sizeof(ports) / sizeof(ports[0]);
    
    for (int i = 0; i < size; i++) {
        sprintf(command, "nmap -p %d %s | grep open", ports[i], ip);
        if (system(command) == 0) {
            printf("Security warning: port %d is open on %s\n", ports[i], ip);
            printf("Recommendation: Unless necessary for your specific use case, close this port to avoid potential security vulnerabilities.\n");
        }
    }
}

int main() {
    char subnet[20];
    char ip[20];

    printf("Enter the subnet to scan (e.g. 192.168.1.0/24): ");
    scanf("%s", subnet);

    scanNetwork(subnet);
    
    printf("Enter the IP to scan for open ports: ");
    scanf("%s", ip);

    scanPorts(ip);
    
    securityChecks(ip);

    return 0;
}
