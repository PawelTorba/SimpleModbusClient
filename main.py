from Solplanet_serial_modbus import Solplanet_Serial_Modbus
from pymodbus import ModbusException
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
#establishing client connection

#client = ModbusSerialClient(port = s_port, baudrate = baud_rate, bytesize=byte_size, parity = parity, stopbits = stop_bits)
client = Solplanet_Serial_Modbus(device_address = slave, s_port = communication_port)

try: 
    print(client.read_device_state())
    #function calls in here
    pass
except ModbusException as exc:
    print("Error with reading input registers, error: " + str(exc))


###STRING CONVERSION TESTING
#test_input = [8224,8224,16723,22321,12363,11596,21536,8224]
#print(client.decode_string(test_input))