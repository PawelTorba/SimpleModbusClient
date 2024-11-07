from pymodbus.client import ModbusSerialClient, ModbusBaseClient
from pymodbus import ModbusException

#Dependencies: pymodbus, pyserial

#serial port of your device
s_port = '/dev/ttyUSB0'
#for devices running Windows, please go into Device Manager and find the name of the serial converter/device, should be named like "COMX" where "X" is a number
#for devices running Linux, you need to find the exact path to your serial device/adapter. If you are using a external adapter you can use below command to find the most recently created serial adapter
#ls -tr1 /dev/tty* | tail -n 1 
#program should be run with sudo permissions (at least on arch linux derivatives)
#(run right after plugging in the device, should be named dev/ttyXXX) where "X"s can be either a number or a number with a prefix like USB1

###Functions###
def read_voltage_AC(client):
    voltage_L1 = client.read_input_registers(address = convert_address(31359), slave=device_address)
    print ("L1 phase voltages:")
    print(voltage_L1.registers)
    
    voltage_L2 = client.read_input_registers(address = convert_address(31361), slave=device_address)
    print ("L2 phase voltages:")
    print(voltage_L2.registers)

    voltage_L3 = client.read_input_registers(address = convert_address(31363), slave=device_address)
    print ("L3 phase voltages:")
    print(voltage_L3.registers)
 
def read_voltage_DC(client):
    voltage_PV1 = client.read_input_registers(address = convert_address(31319), slave=device_address)
    print ("PV1 phase voltages:")
    print(voltage_PV1.registers)
    
    voltage_PV2 = client.read_input_registers(address = convert_address(31321), slave=device_address)
    print ("PV2 phase voltages:")
    print(voltage_PV2.registers)

def convert_address(address):
    """Returns the real value of the provided register, please input the exact register address from the Solplanet Modbus documentation"""
    address = int(str(address)[1:]) - 1
    return address

#global values (communication parameters)
baud_rate = 9600
byte_size = 8
parity = "N"
stop_bits = 1
#address of slave device
device_address = 3

try:
    client = ModbusSerialClient(port = s_port, baudrate = baud_rate, bytesize=byte_size, parity = parity, stopbits = stop_bits)
except ModbusException as exc:
    print("Error connecting to server, error: " + str(exc))

try: 
    read_voltage_AC(client)

except ModbusException as exc:
    print("Error with reading input registers, error: " + str(exc))
read_voltage_DC(client)