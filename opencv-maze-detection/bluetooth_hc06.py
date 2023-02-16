"""
import bluetooth

print("Performing inquiry...")

nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

print("Found {} devices".format(len(nearby_devices)))

for addr, name in nearby_devices:
    try:
        print("   {} - {}".format(addr, name))
    except UnicodeEncodeError:
        print("   {} - {}".format(addr, name.encode("utf-8", "replace")))

# Set up Bluetooth connection
"""
import serial

# Set up serial connection
s = serial.Serial(
    port="COM5", # the port hc-06 is connected to
    baudrate=9600, # Replace with the correct baud rate
)

# Write data to the HC-06

s.write(b"hello")

# Close the serial connection

for i in range (5):
    response = s.read().decode('ascii').rstrip()
    print(response)
# Close the serial port
s.close()