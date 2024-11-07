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
    voltage_P1 = client.read_input_registers(address = convert_address(31319), slave=device_address)
    print ("P1 phase voltages:")
    print(voltage_P1.registers)
    
    voltage_P2 = client.read_input_registers(address = convert_address(31321), slave=device_address)
    print ("L2 phase voltages:")
    print(voltage_P2.registers)

def read_e_total(client):
    e_total = client.read_input_registers(address = convert_address(31305), slave=device_address, count=2)
    print ("E-total:")
    print(e_total.registers)

def read_serial_number(client): #this is model, typo
    serial_number = client.read_input_registers(address = convert_address(31019), slave=device_address, count=8)
    print ("Serial number:") #you get 16 bit intigers, you need to convert it to binary, first 8 bits (counting from the right) is 1 asci character, the other 8 are the second
    print(serial_number.registers)

def battery_error_status(client):
    bat_error_status = client.read_input_registers(address = convert_address(31609), slave=device_address)
    print ("Battery error bits:") #bytemap, returns intiger, convert it to binary to read error code
    print(bat_error_status.registers)

def convert_address(address):
    """Returns the real value of the provided register, please input the exact register address from the Solplanet Modbus documentation"""
    address = int(str(address)[1:]) - 1
    return address


#global values (for communication with Solplanet devices)
baud_rate = 9600
byte_size = 8
parity = "N"
stop_bits = 1
#address of slave device
device_address = 3

#address we want to read (will be formatted automatically to the correct format automatically via "convert_address" function)
register = 31001

print("Connecting to server")
#establishing client connection
try:
    client = ModbusSerialClient(port = s_port, baudrate = baud_rate, bytesize=byte_size, parity = parity, stopbits = stop_bits)
except ModbusException as exc:
    print("Error connecting to server, error: " + str(exc))

try: 
    #result = client.read_input_registers(address = convert_address(register), slave=device_address)
    #print(result.registers)
    read_voltage_AC(client)
    read_voltage_DC(client)
    read_e_total(client)
    read_serial_number(client)
    battery_error_status(client)
except ModbusException as exc:
    print("Error with reading input registers, error: " + str(exc))
