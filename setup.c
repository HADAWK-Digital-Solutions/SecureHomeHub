#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

void createUser() {
    // CREATE USERS
    char rootPassword[50];
    printf("Enter password for SecureHomeHub Admin: ");
    scanf("%s", rootPassword);
    createUser("root", rootPassword, 1);  // Set isAdmin to 1 for root user (admin)

    char user1[50];
    printf("Enter new username: ");
    scanf("%s", user1);
    createUser(user1, NULL, 0);  // Set isAdmin to 0 for regular users

    // Set password for root user
    system("sudo passwd root");
    char command[100];
    if (password != NULL) {
        sprintf(command, "sudo useradd -m -p %s %s", password, username);
    }
    else {
        sprintf(command, "sudo useradd -m %s", username);
    }

    if (isAdmin) {
        strcat(command, " -G sudo");
    }

    system(command);

}

void enableUpdates() {
    // Enable automatic updates
    system("sudo apt-get install unattended-upgrades apt-listchanges");
}

void createFolder(const char* folderPath) {
    char command[100];
    sprintf(command, "mkdir %s", folderPath);
    system(command);
}

void copyFiles(const char* sourcePath, const char* destinationPath) {
    char command[200];
    sprintf(command, "cp -R %s/* %s", sourcePath, destinationPath);
    system(command);
}

void enableAutoRun() {
    FILE* file = fopen("/etc/rc.local", "a");
    if (file == NULL) {
        printf("Error opening rc.local file.\n");
        exit(1);
    }
    fprintf(file, "/usr/local/secureHomeHub/secureHomeHub &\n");
    fclose(file);
}

void changeHostname() {
    char newHostname[20];
    const char* prefix = "securehomehub";

    // Generate a random suffix of six numbers for the hostname
    srand(time(NULL));
    int randomNumber = rand() % 900000 + 100000;
    sprintf(newHostname, "%s%d", prefix, randomNumber);

    // Set the new hostname in /etc/hostname
    FILE* file = fopen("/etc/hostname", "w");
    if (file == NULL) {
        printf("Error opening /etc/hostname file.\n");
        exit(1);
    }
    fprintf(file, "%s\n", newHostname);
    fclose(file);

    // Update the /etc/hosts file with the new hostname
    file = fopen("/etc/hosts", "a");
    if (file == NULL) {
        printf("Error opening /etc/hosts file.\n");
        exit(1);
    }
    fprintf(file, "127.0.0.1\t%s\n", newHostname);
    fclose(file);

    // Set the new hostname for the current session
    char command[40];
    sprintf(command, "sudo hostname %s", newHostname);
    system(command);
}

void configureNetwork() {
    printf("Configure network settings:\n");
    printf("1. DHCP\n");
    printf("2. Static IP\n");
    int choice;
    printf("Enter your choice (1 or 2): ");
    scanf("%d", &choice);

    if (choice == 1) {
        printf("Configuring DHCP...\n");
        // Configure DHCP settings
        system("sudo dhclient");
        printf("DHCP configuration completed.\n");
    }
    else if (choice == 2) {
        char ipAddress[16];
        char subnetMask[16];

        printf("Enter the IP address: ");
        scanf("%s", ipAddress);
        printf("Enter the subnet mask: ");
        scanf("%s", subnetMask);

        char command[100];
        sprintf(command, "sudo ifconfig eth0 %s netmask %s up", ipAddress, subnetMask);
        system(command);

        printf("Static IP configuration completed.\n");
    }
    else {
        printf("Invalid choice.\n");
        return;
    }
}

void joinDomain() {
    printf("Join domain:\n");

    int attempts = 0;
    int maxAttempts = 3;
    char domainName[50];
    char domainUser[50];
    char domainPassword[50];

    do {
        printf("Enter the domain name: ");
        scanf("%s", domainName);
        printf("Enter the domain user: ");
        scanf("%s", domainUser);
        printf("Enter the domain password: ");
        scanf("%s", domainPassword);

        // Perform domain join validation here (dummy validation in this example)
        if (strcmp(domainName, "example.com") == 0 && strcmp(domainUser, "admin") == 0 && strcmp(domainPassword, "password") == 0) {
            printf("Domain join successful!\n");
            return;
        }
        else {
            attempts++;
            printf("Invalid domain information. Please try again.\n");
        }
    } while (attempts < maxAttempts);

    printf("Error: Unable to join the domain after multiple attempts.\n");
}

int main() {
    const char* setupFolder = "/usr/local/secureHomeHub";
    const char* sourcePath = "."; // Assumes setup.c is in the same directory as the files to be copied

    createFolder(setupFolder);
    copyFiles(sourcePath, setupFolder);
    enableUpdates();
    enableAutoRun();
    changeHostname();

    configureNetwork();


    char joinDomainChoice;
    printf("Would you like to join a domain? (Y/N): ");
    scanf(" %c", &joinDomainChoice);

    if (joinDomainChoice == 'Y' || joinDomainChoice == 'y') {
        joinDomain();
    }

    printf("Setup completed successfully!\n");

    return 0;
}