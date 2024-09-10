import ipaddress
import subprocess
import time
import sys

# Function to validate IPv6 address format
def is_valid_ipv6(address):
    try:
        ipaddress.IPv6Address(address)
        return True
    except ipaddress.AddressValueError:
        return False

# Function to ping the IPv6 address
def ping_ipv6(address):
    try:
        # Use the subprocess module to execute the ping command
        # Note: On Windows, `ping` uses `-6` to specify IPv6
        # On Unix-like systems, it may require `ping6` or `ping -6`
        result = subprocess.run(
            ["ping", "-6", "-c", "4", address],
            capture_output=True,
            text=True
        )
        print(f"Ping to {address} was successful.")
        print("Response Times (ms):")
        print(result.stdout)
    except subprocess.CalledProcessError:
        print(f"Ping to {address} failed.")

# Define the IPv6 address of the host you want to ping
ipv6_address = "2001:db8::1"  # Replace this with the actual IPv6 address

# Loop to check the IPv6 address every 30 minutes
while True:
    # Validate the IPv6 address
    if is_valid_ipv6(ipv6_address):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] The IPv6 address {ipv6_address} is valid.")
        ping_ipv6(ipv6_address)
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] The IPv6 address {ipv6_address} is invalid.")

    # Wait for 30 minutes before the next check
    time.sleep(1800)  # 1800 seconds = 30 minutes
