from pymodbus.client import ModbusSerialClient, ModbusBaseClient
from pymodbus import ModbusException

#Dependencies: pymodbus, pyserial

#serial port of your device
s_port = "COM8" 
#for devices running Windows, please go into Device Manager and find the name of the serial converter/device, should be named like "COMX" where "X" is a number
#for devices running Linux, you need to find the exact path to your serial device/adapter. If you are using a external adapter you can use below command to find the most recently created serial adapter
#ls -tr1 /dev/tty* | tail -n 1 
#(run right after plugging in the device, should be named dev/ttyXXX) where "X"s can be either a number or a number with a prefix like USB1

#global values (for communication with Solplanet devices)
baud_rate = 9600
byte_size = 8
parity = "N"
stop_bits = 1
#address of slave device
device_address = 3

#address we want to read (will be formatted automatically to the correct format automatically via "convert_address" function)
register = 31001 

def convert_address(address):
    """Returns the real value of the provided register, please input the exact register address from the Solplanet Modbus documentation"""
    address = int(str(address)[1:]) - 1
    return address

print("Connecting to server")
#establishing client connection
try:
    client = ModbusSerialClient(port = s_port, baudrate = baud_rate, bytesize=byte_size, parity = parity, stopbits = stop_bits)
except ModbusException as exc:
    print("Error connecting to server, error: " + str(exc))

#sample repsponse reading from the device (inverter)
try: 
    result = client.read_input_registers(address = convert_address(), slave=device_address)
    print(result.registers)
except ModbusException as exc:
    print("Error with reading input registers, error: " + str(exc))

try:
    print("Reponse to test request is: \n" + str(result.registers))
    #other way to print out a reponse
    #for reg in result:
    #    print(reg)
except NameError:
    print("No response from the device")




###Functions###
def read_voltage_AC(client):
    voltage_L1 = client.read_input_registers(address = convert_address(31359), slave=device_address)
    print ("L1 phase voltages:")
    print(voltage_L1.registers)
    
    voltage_L2 = client.read_input_registers(address = convert_address(31361), slave=device_address)
    print ("L2 phase voltages:")
    print(voltage_L2.registers)

    voltage_l3 = client.read_input_registers(address = convert_address(31363), slave=device_address)
    print ("L3 phase voltages:")
    print(voltage_L3.registers)

def read_production_total_today(client):
    e_today = client.read_input_registers(address = convert_address(31303), slave=device_address, count=2)
    print ("E-today:")
    print(e_today.registers)

def read_device_state(client):
    state = client.read_input_registers(address = convert_address(31309), slave=device_address)
    print ("State of the device: ")
    print(state.registers)

def read_active_power(client):
    active_power = client.read_input_registers(address = convert_address(31371), slave=device_address, count=2)
    print ("Current active power: ")
    print(active_power.registers)