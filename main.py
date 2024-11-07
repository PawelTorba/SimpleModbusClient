import Solplanet_serial_modbus
#Dependencies: pymodbus, pyserial

#serial port of your device
communication_port = '/dev/ttyUSB0'
#for devices running Windows, please go into Device Manager and find the name of the serial converter/device, should be named like "COMX" where "X" is a number
#for devices running Linux, you need to find the exact path to your serial device/adapter. If you are using a external adapter you can use below command to find the most recently created serial adapter
#ls -tr1 /dev/tty* | tail -n 1 
#(run right after plugging in the device, should be named dev/ttyXXX) where "X"s can be either a number or a number with a prefix like USB1
#program should be run with sudo permissions (at least on arch linux derivatives)

#address of slave device
slave = 3

print("Connecting to server.")
#establishing client connection
try:
    #client = ModbusSerialClient(port = s_port, baudrate = baud_rate, bytesize=byte_size, parity = parity, stopbits = stop_bits)
    client = Solplanet_serial_modbus(device_address = slave, s_port = communication_port)
except ModbusException as exc:
    print("Error connecting to server, error: " + str(exc))
    exit(1)
print("Connection successful.")

try: 
    #function calls here
    pass
except ModbusException as exc:
    print("Error with reading input registers, error: " + str(exc))
