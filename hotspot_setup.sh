# ======================================================================
# Secure Home Hub Wi-Fi setup script
# Written by Alexander "Alec" Robinson of HADAWK digital solutions.
# Date: 2023-10-28
#
# Contains references from ChatGPT and other sources. 
# Please see project documents for full list of references.
# ======================================================================
# This script uses Network Manager commands to set up a Wi-fi Hotspot
# on the hub, generating a unique SSID and passphrase based on the 
# Machine id.
# ====================================================================== 

# ===== SCRIPT BEGINS =====
# notification for user to wait while hotspot is set up.
cat <<EOF

#################################################################
#                                                               #
#      Please wait. Secure Home Hub is setting up Wi-Fi.        #
#                                                               #
#            This will take take about 2 minutes.               #
#       We'll let you know as soon as it should be done!        #
#                                                               #
#################################################################

EOF

# Capture MachineID last 4 characters as "M_ID1"
M_ID1="$(cat /etc/machine-id | tail -c 5)"

# Create the SSID by appending the last 4 digits of the machine's UUID
SSID="SecHomeHub-$M_ID1"

# Use nmcli to create the Wi-Fi hotspot connection named "Hotspot"
nmcli connection add type wifi ifname wlan0 con-name Hotspot autoconnect no ssid "$SSID"

# Capture middle 8 characters from the machine ID as "M_ID2" and create default passphrase
MACHINE_ID=$(cat /etc/machine-id)
M_ID2=$(echo "$MACHINE_ID" | cut -c 13-20)
PASSPHRASE="SecureHome$M_ID2"

# modify Hotspot configuration to Access Point (ap), share IPv4, disable IPv6
nmcli connection modify Hotspot 802-11-wireless.mode ap ipv4.method shared ipv6.method disabled

# configure Wi-Fi security (minus passphrase)
nmcli connection modify Hotspot wifi-sec.group ccmp wifi-sec.key-mgmt wpa-psk wifi-sec.proto rsn 

# add passphrase and pairing method
nmcli connection modify Hotspot wifi-sec.psk "$PASSPHRASE" wifi-sec.pairwise ccmp

# set Hotspot to auto-connect at start-up and activate connection
nmcli connection modify Hotspot autoconnect yes
nmcli connection up Hotspot
cat <<EOF
#################################################################

     Almost done! Just giving everything time to start up.
	 Please wait for the next message. 

#################################################################

EOF

# Delay to allow Hotspot to finish Setup
sleep 120

# Setup complete message and login info
cat <<EOF

#################################################################
#                                                               #
#  Welcome to the Secure Home Hub by HADAWK Digital Solutions!  #
#                                                               #
#  Please connect your phone or tablet to this network so you   #
#  can add your smart devices to the hub.                       #
#                                                               #
#################################################################

  Network ID: $SSID
  Password  : $PASSPHRASE 

EOF

# ===== END OF SCRIPT =====
