#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <stdbool.h> // Include the necessary header for boolean type
#include <dirent.h> // For directory handling
#include <sys/stat.h> // For file information

#define BUFFER_SIZE 1024

// Function to display a fancy welcome screen
void displayWelcomeScreen() {
    printf("\n");
    printf("*************************************************\n");
    printf("*     Welcome to HADAWK Digital Solutions       *\n");
    printf("* --------------------------------------------- *\n");
    printf("*           My Secure Home Hub Setup            *\n");
    printf("*************************************************\n");
    printf("\n");
}

// Function to check for a pre-existing installation in /usr/local/secureHomeHub
bool checkForExistingInstallation(const char* sourcePath, const char* destinationPath) {
    if (access(destinationPath, F_OK) != -1) {
        // The directory exists, indicating a pre-existing installation
        printf("A previous installation has been detected in %s.\n", destinationPath);
        char userInput[10];
        printf("Select an option:\n");
        printf("1. Verify and Repair Files\n");
        printf("2. Perform a Clean Installation\n");
        printf("3. Uninstall Secure Hub\n");
        printf("Enter the number of your choice: ");
        scanf("%s", userInput);


        if (strcmp(userInput, "1") == 0) {
                    // Option 1: Verify and Repair Files (Add your code here)
                    printf("Verifying and repairing files...\n");
                    // Add code for verifying and repairing files
                    DIR *sourceDir = opendir(sourcePath);
                    if (sourceDir == NULL) {
                        perror("Error opening source directory");
                        return 0;
                    }

                    struct dirent *entry;
                    while ((entry = readdir(sourceDir)) != NULL) {
                        // Ignore "." and ".." entries
                        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                            continue;
                        }

                        char sourceFilePath[PATH_MAX];
                        char destinationFilePath[PATH_MAX];
                        sprintf(sourceFilePath, "%s/%s", sourcePath, entry->d_name);
                        sprintf(destinationFilePath, "%s/%s", destinationPath, entry->d_name);

                        // Check if the file in sourcePath exists in destinationPath
                        if (access(destinationFilePath, F_OK) == -1) {
                            // The file is missing in destinationPath, copy it
                            printf("Copying missing file: %s\n", entry->d_name);

                            // Open source file
                            FILE* sourceFile = fopen(sourceFilePath, "rb");
                            if (sourceFile == NULL) {
                                perror("Error opening source file");
                                continue;
                            }

                            // Create destination file
                            FILE* destinationFile = fopen(destinationFilePath, "wb");
                            if (destinationFile == NULL) {
                                perror("Error creating destination file");
                                fclose(sourceFile);
                                continue;
                            }

                            // Copy the contents of the source file to the destination file
                            char buffer[BUFFER_SIZE];
                            size_t bytesRead;
                            while ((bytesRead = fread(buffer, 1, BUFFER_SIZE, sourceFile)) > 0) {
                                fwrite(buffer, 1, bytesRead, destinationFile);
                            }

                            // Close the files
                            fclose(sourceFile);
                            fclose(destinationFile);

                            printf("File copied: %s\n", entry->d_name);
                        }
                    }

                    closedir(sourceDir);      



                    printf("Files verified and repaired.\n");

                } else if (strcmp(userInput, "2") == 0) {
                    // Option 2: Perform a Clean Installation
                    printf("Performing a clean installation...\n");
                    char removeCommand[200];
                    sprintf(removeCommand, "sudo rm -r %s", destinationPath);
                    system(removeCommand);
                    if (!(access(destinationPath, F_OK) != -1)) {
                        printf("Previous installation has been successfully Clean installation completed successfully.\n");
                    } else {
                        printf("Error uninstalling Secure Home Hub.\n");
                    return true; // Return true to exit the script
                    }
                    
                } else if (strcmp(userInput, "3") == 0) {
                    // Option 3: Uninstall Secure Hub
                    printf("Uninstalling Secure Hub...\n");
                    char removeCommand[200];
                    sprintf(removeCommand, "sudo rm -r %s", destinationPath);
                    system(removeCommand);
                    if (!(access(destinationPath, F_OK) != -1)) {
                        printf("Secure Home Hub has been successfully uninstalled.\n");
                        exit(EXIT_SUCCESS);
                    } else {
                        printf("Error uninstalling Secure Home Hub. Please try again later.\n");
                        exit(EXIT_SUCCESS);
                    }
                } else {
                    printf("Invalid choice. Stopping setup.\n");
                    return true; // Return true to exit the script
            }
    }
    return false; // No pre-existing installation found
}

// Function to check for available updates in Parrot OS and packages
void updateChecker() {
    char buffer[BUFFER_SIZE];
    FILE *fp;

    printf("Checking for available updates in Parrot OS...\n");

    // Run 'sudo apt-get update' to update the package lists
    fp = popen("sudo apt-get update", "r");
    if (fp == NULL) {
        perror("Error running 'apt-get update'");
        exit(EXIT_FAILURE);
    }
    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        // Print update progress (optional)
        printf("%s", buffer);
    }
    pclose(fp);

    // Run 'apt-get -s dist-upgrade' to check for available updates
    printf("Checking for available updates...\n");
    fp = popen("sudo apt-get -s dist-upgrade", "r");
    if (fp == NULL) {
        perror("Error running 'apt-get -s dist-upgrade'");
        exit(EXIT_FAILURE);
    }
    int updatesAvailable = 0;
    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        // Search for lines indicating available updates
        if (strstr(buffer, "upgraded,") != NULL) {
            updatesAvailable = 1;
            break;
        }
    }
    pclose(fp);

    if (updatesAvailable) {
        printf("Updates are available for Parrot OS.\n");
        // Prompt the user to update
        int validInput = 0; // Flag to track if the input is valid
        while (!validInput) { // Continue looping until validInput is true (1)
            char userInput[10];
            printf("Do you want to update Parrot OS? (yes/no): ");
            scanf("%s", userInput);

            if (strcmp(userInput, "yes") == 0 || strcmp(userInput, "y") == 0) {
                // User wants to update, so run the update command
                printf("Updating Parrot OS...\n");
                system("sudo apt-get dist-upgrade -y ");
                printf("Parrot OS updated successfully.\n");
                validInput = 1; // Set the flag to true to exit the loop
            } else if (strcmp(userInput, "no") == 0 || strcmp(userInput, "n") == 0) {
                // User doesn't want to update
                printf("Stopping setup.\n");
                exit(EXIT_SUCCESS); // Exit the script gracefully
            } else {
                // Invalid input
                printf("Invalid input. Please enter 'yes' or 'no'.\n");
            }
        }
    } else {
        printf("No updates are available for Parrot OS.\n");
    }
}

// Function to create a log file in the "Logs" subfolder with a timestamped name
void createLogFileWithTimestamp(const char* logFolderPath) {
    char logFilePath[200];

    // Get the current timestamp
    time_t rawTime;
    struct tm* timeInfo;
    char timestamp[100];

    time(&rawTime);
    timeInfo = localtime(&rawTime);
    strftime(timestamp, sizeof(timestamp), "%a %b %d %H:%M:%S %Y", timeInfo);

    // Create the log file with the timestamped name
    sprintf(logFilePath, "%s/SecureHomeHub_Log [%s].log", logFolderPath, timestamp);
    FILE* logFile = fopen(logFilePath, "w");
    if (logFile == NULL) {
        printf("Error creating log file.\n");
    }
    
}

// Function to create a folder and a log file in /usr/local/secureHomeHub and install Secure Home Hub files
void installSecureHomeHub(const char* sourcePath, const char* destinationPath) {
char userInput[10];
    int validInput = 0; // Flag to track if the input is valid

    while (!validInput) { // Continue looping until validInput is true (1)
        printf("Would you like to install and set up HADAWK Digital Solutions Secure Home Hub? (yes/no): ");
        scanf("%s", userInput);

        if (strcmp(userInput, "yes") == 0 || strcmp(userInput, "y") == 0) {
            // User wants to install and set up Secure Home Hub
            validInput = 1; // Set the flag to true to exit the loop
        } else if (strcmp(userInput, "no") == 0 || strcmp(userInput, "n") == 0) {
            // User doesn't want to install and set up Secure Home Hub
            printf("Exiting the setup.\n");
            exit(EXIT_SUCCESS); // Exit the script gracefully
        } else {
            // Invalid input
            printf("Invalid input. Please enter 'yes' or 'no'.\n");
        }
    }
    // Continue with the setup process here
    // Create the main folder
    char command[100];
    sprintf(command, "mkdir %s", destinationPath);
    system(command);
    memset(command, '\0', sizeof(command));
    // Copy files to path
    
    sprintf(command, "cp -R %s/* %s", sourcePath, destinationPath);
    system(command);
    memset(command, '\0', sizeof(command));
    // Create the "Logs" subfolder
    
    char logFolderPath[150]; // Create a buffer for the log folder path
    sprintf(logFolderPath, "%s/Logs", destinationPath);
    sprintf(command, "mkdir %s", logFolderPath);
    system(command);

    // Call the function to create a log file with a timestamped name to be writen to throughout the rest of the setup
    createLogFileWithTimestamp(logFolderPath);
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
    } else if (choice == 2) {
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
    } else {
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
        } else {
            attempts++;
            printf("Invalid domain information. Please try again.\n");
        }
    } while (attempts < maxAttempts);

    printf("Error: Unable to join the domain after multiple attempts.\n");
}

void scheduleBackup() {
    char frequency[32];
    char time[8];

    printf("Choose backup frequency:\n");
    printf("1. Daily\n2. Weekly\n3. Bi-weekly\n4. Monthly\n5. Quarterly\n6. Half-yearly\n7. Yearly\n");
    int option;
    do {
        printf("Enter the number corresponding to your choice: ");
        scanf("%d", &option);
    } while (option < 1 || option > 7);

    switch (option) {
        case 1:
            strcpy(frequency, "daily");
            break;
        case 2:
            strcpy(frequency, "weekly");
            break;
        case 3:
            strcpy(frequency, "bi-weekly");
            break;
        case 4:
            strcpy(frequency, "monthly");
            break;
        case 5:
            strcpy(frequency, "quarterly");
            break;
        case 6:
            strcpy(frequency, "half-yearly");
            break;
        case 7:
            strcpy(frequency, "yearly");
            break;
    }

    printf("Enter the time of day for the backup (e.g., 03:00): ");
    scanf("%s", time);

    // Add the cron job
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "(crontab -l ; echo \"%s %s /usr/local/secureHomeHub/backup.c\") | crontab -", time, frequency);
    if (system(cmd) == -1) {
        perror("Failed to schedule backup");
    } else {
        printf("Backup scheduled successfully.\n");
    }
}

void executeCommand(const char *command) {
    printf("Executing: %s\n", command);
    system(command);
}

void setupWiFi() {
    // notification for the user to wait while the hotspot is set up.
    printf("\n#################################################################\n");
    printf("#                                                               #\n");
    printf("#      Please wait. Secure Home Hub is setting up Wi-Fi.        #\n");
    printf("#                                                               #\n");
    printf("#            This will take about 2 minutes.                   #\n");
    printf("#       We'll let you know as soon as it should be done!        #\n");
    printf("#                                                               #\n");
    printf("#################################################################\n");

    // Capture MachineID last 4 characters as "M_ID1"
    char command[100];
    snprintf(command, sizeof(command), "tail -c 5 /etc/machine-id");
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        perror("Error capturing machine ID");
        exit(1);
    }
    char M_ID1[5];
    fgets(M_ID1, sizeof(M_ID1), fp);
    pclose(fp);
    M_ID1[4] = '\0';

    // Create the SSID by appending the last 4 digits of the machine's UUID
    char SSID[20];
    snprintf(SSID, sizeof(SSID), "SecHomeHub-%s", M_ID1);

    // Use nmcli to create the Wi-Fi hotspot connection named "Hotspot"
    snprintf(command, sizeof(command), "nmcli connection add type wifi ifname wlan0 con-name Hotspot autoconnect no ssid \"%s\"", SSID);
    executeCommand(command);

    // Capture middle 8 characters from the machine ID as "M_ID2" and create the default passphrase
    char MACHINE_ID[40];
    fp = fopen("/etc/machine-id", "r");
    if (fp == NULL) {
        perror("Error opening machine ID file");
        exit(1);
    }
    fgets(MACHINE_ID, sizeof(MACHINE_ID), fp);
    fclose(fp);

    char M_ID2[9];
    strncpy(M_ID2, MACHINE_ID + 12, 8);
    M_ID2[8] = '\0';

    char PASSPHRASE[20];
    snprintf(PASSPHRASE, sizeof(PASSPHRASE), "SecureHome%s", M_ID2);

    // Modify Hotspot configuration to Access Point (ap), share IPv4, disable IPv6
    executeCommand("nmcli connection modify Hotspot 802-11-wireless.mode ap ipv4.method shared ipv6.method disabled");

    // Configure Wi-Fi security (minus passphrase)
    executeCommand("nmcli connection modify Hotspot wifi-sec.group ccmp wifi-sec.key-mgmt wpa-psk wifi-sec.proto rsn");

    // Add passphrase and pairing method
    snprintf(command, sizeof(command), "nmcli connection modify Hotspot wifi-sec.psk \"%s\" wifi-sec.pairwise ccmp", PASSPHRASE);
    executeCommand(command);

    // Set Hotspot to auto-connect at start-up and activate connection
    executeCommand("nmcli connection modify Hotspot autoconnect yes");
    executeCommand("nmcli connection up Hotspot");

    printf("\n#################################################################\n");
    printf("#                                                               #\n");
    printf("#     Almost done! Just giving everything time to start up.    #\n");
    printf("#     Please wait for the next message.                        #\n");
    printf("#                                                               #\n");
    printf("#################################################################\n");

    // Delay to allow Hotspot to finish setup
    sleep(120);

    // Setup complete message and login info
    printf("\n#################################################################\n");
    printf("#                                                               #\n");
    printf("#  Welcome to the Secure Home Hub by HADAWK Digital Solutions!  #\n");
    printf("#                                                               #\n");
    printf("#  Please connect your phone or tablet to this network so you   #\n");
    printf("#  can add your smart devices to the hub.                       #\n");
    printf("#                                                               #\n");
    printf("#################################################################\n");
    printf("  Network ID: %s\n", SSID);
    printf("  Password  : %s \n", PASSPHRASE);
}

int main() {
    // Display the welcome screen
    displayWelcomeScreen();

    const char* setupFolder = "/usr/local/secureHomeHub";
    const char* sourcePath = "."; // Assumes setup.c is in the same directory as the files to be copied
    // Check for pre-existing installation and handle it
    checkForExistingInstallation(sourcePath, setupFolder);

    // Check for updates
    updateChecker();

     // Install Secure Home Hub
    installSecureHomeHub(sourcePath, setupFolder);

    // Enable autorun at system startup 
    enableAutoRun();
    
    // Change the system hostname
    changeHostname();

    // Configure network settings
    configureNetwork();

    // Prompt the user to join a domain
    char joinDomainChoice;
    printf("Would you like to join a domain? (Y/N): ");
    scanf(" %c", &joinDomainChoice);

    if (joinDomainChoice == 'Y' || joinDomainChoice == 'y') {
        joinDomain();
    }
    

    // Prompt the user to schedule automated backups
    char backupChoice;
    printf("Do you want to automate and schedule backups (y/n)? ");
    scanf(" %c", &backupChoice);

    if (backupChoice == 'y' || backupChoice == 'Y') {
        scheduleBackup();
    } else {
        printf("Backup automation disabled.\n");
    }
    
    setupWiFi();
    
    printf("Setup completed successfully!\n");

    return 0;
}
