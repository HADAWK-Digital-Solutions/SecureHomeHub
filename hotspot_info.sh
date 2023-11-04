# ======================================================================
# Secure Home Hub Wi-Fi setup script
# Written by Alexander "Alec" Robinson of HADAWK digital solutions.
# Date: 2023-11-04
#
# Contains references from ChatGPT and other sources. 
# Please see project documents for full list of references.
# ======================================================================
# This script displays the default SSID and passphrase based on the same
# system used to generate the default hotspot and password
# ====================================================================== 

# ===== SCRIPT BEGINS =====

# Capture MachineID last 4 characters as "M_ID1"
M_ID1="$(cat /etc/machine-id | tail -c 5)"

# Create the SSID by appending the last 4 digits of the machine's UUID
SSID="SecHomeHub-$M_ID1"


# Capture middle 8 characters from the machine ID as "M_ID2" and create default passphrase
MACHINE_ID=$(cat /etc/machine-id)
M_ID2=$(echo "$MACHINE_ID" | cut -c 13-20)
PASSPHRASE="SecureHome$M_ID2"


# Setup complete message and login info
cat <<EOF

#################################################################
#                                                               #
#  Welcome to the Secure Home Hub by HADAWK Digital Solutions!  #
#                                                               #
#  Your default hotspot information for connecting to this      #
#  Secure Home Hub is below. If these seetings do not work      #
#  try resetting your hotspot by running hotspot_setup.sh       #
#                                                               #
#################################################################

  Network ID: $SSID
  Password  : $PASSPHRASE 

EOF

# ===== END OF SCRIPT =====
