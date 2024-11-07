from pymodbus.client import ModbusSerialClient, ModbusBaseClient

class Solplanet_Serial_Modbus(ModbusSerialClient):
    def __init__(self, baud_rate = 9600, byte_size = 8, parity = "N", stop_bits = 1, device_address = 3, s_port = ""):
        """Initialize basic communication parameters, defaults are: bd = 9600, byte size = 8, parity = none, stop_bits = 1"""
        #self.port
        #self.baudrate
        #self.bytesize 
        #self.parity 
        #self.stopbits
        self.slave = device_address
        super().__init__(port = s_port, baudrate = baud_rate, bytesize=byte_size, parity = parity, stopbits = stop_bits)

######INPUT REGISTERS######
    def read_device_type(self):
        device_type = self.read_input_registers(address = self.convert_address(31001), slave=self.slave) 
        return device_type.registers
        #TODO add function to decode string value

    def read_slave_modbus_address(self):
        mb_address = self.read_input_registers(address = self.convert_address(31002), slave=self.slave) 
        return int(mb_address.registers[0])

    def read_serial_number(self):
        serial_number = self.read_input_registers(address = self.convert_address(31003), slave=self.slave, count=16) 
        return serial_number.registers
        #TODO add function to decode string value

    def read_machine_type(self): 
        """Returns a string with inverter model"""
        model_name = self.read_input_registers(address = self.convert_address(31019), slave=self.slave, count=8) 
        return model_name.registers
        #TODO add function to decode string value

    def read_current_grid_code(self):
        grid_code = self.read_input_registers(address = self.convert_address(31027), slave=self.slave) 
        return grid_code.registers[0]

    def read_rated_power(self):
        rated_power = self.read_input_registers(address = self.convert_address(31028), slave=self.slave, count=2) 
        return rated_power.registers
        #TODO test reponse type
        
    def read_current_software_version(self):
        current_soft_ver = self.read_input_registers(address = self.convert_address(31030), slave=self.slave, count=8) 
        return current_soft_ver.registers
        #TODO add function to decode string value

    def read_current_safety_version(self):
        current_safe_ver = self.read_input_registers(address = self.convert_address(31044), slave=self.slave, count=7) 
        return current_soft_ver.registers
        #TODO add function to decode string value
    
    def read_manufacturer_name(self):
        name = self.read_input_registers(address = self.convert_address(31057), slave=self.slave, count=7) 
        return name.registers
        #TODO add function to decode string value

    def read_brand_name(self):
        name = self.read_input_registers(address = self.convert_address(31065), slave=self.slave, count=7) 
        return name.registers
        #TODO add function to decode string value

    def read_grid_rated_voltage(self):
        rated_vol = self.read_input_registers(address = self.convert_address(31301), slave=self.slave)
        return float(rated_vol.registers[0]) * 0.1

    def read_grid_rated_frequency(self):
        rated_freq = self.read_input_registers(address = self.convert_address(31302), slave=self.slave)
        return float(rated_freq.registers[0]) * 0.01

    def read_e_today(self):
        e_today = self.read_input_registers(address = self.convert_address(31303), slave=self.slave, count = 2)
        return float(e_today.registers[1]) * 0.1 
        
    def read_e_total(self):
        """Returns floating point number representing production in kWh"""
        e_total = self.read_input_registers(address = self.convert_address(31305), slave=self.slave, count=2)
        return float(e_total.registers[1]) * 0.1      

    def read_h_total(self):
        h_total = self.read_input_registers(address = self.convert_address(31307), slave=self.slave, count=2)
        return float(h_total.registers[1]) * 1 

    def read_device_state(self):
        state = self.read_input_registers(address = self.convert_address(31309), slave=self.slave)
        return float(state.registers)

    def connect_time(self):
        con_time = self.read_input_registers(address = self.convert_address(31310), slave=self.slave)
        return int(con_time.registers[0])  

    def read_air_temp(self):
        temp = self.read_input_registers(address = self.convert_address(31311), slave=self.slave)
        return float(temp.registers[0]) * 0.1 
    
    def read_inverter_phase_temp(self):
        phase_temps = {"L1": 0, "L2": 0, "L3":0}      
        phase_temps["L1"] = self.read_input_registers(address = self.convert_address(31312), slave=self.slave)
        phase_temps["L2"] = self.read_input_registers(address = self.convert_address(31313), slave=self.slave)
        phase_temps["L3"] = self.read_input_registers(address = self.convert_address(31314), slave=self.slave)

        phase_temps["L1"] = float(phase_temps["L1"].registers[0]) * 0.1
        phase_temps["L2"] = float(phase_temps["L2"].registers[0]) * 0.1
        phase_temps["L3"] = float(phase_temps["L3"].registers[0]) * 0.1

        return phase_temps

    def read_boost_temp(self):
        temp = self.read_input_registers(address = self.convert_address(31315), slave=self.slave)
        return float(temp.registers[0]) * 0.1 

    def read_bidirect_dc_conv_temp(self):
        temp = self.read_input_registers(address = self.convert_address(31316), slave=self.slave)
        return float(temp.registers[0]) * 0.1 

    def read_bus_voltage(self):
        bus_vol = self.read_input_registers(address = self.convert_address(31317), slave=self.slave)
        return float(bus_vol.registers[0]) * 0.1

    def read_dc_voltage(self):
        """Returns a dictionary with MPPT1 TO 5 voltage values. Values are already converter to 'real'"""
        #TODO: CHANGE THE WAY VALUES ARE CONVERTER TO "REAL" AND ASSIGNED TO DICT
        dc_voltages = {"PV1": 0, "PV2": 0, "PV3": 0, "PV4": 0, "PV5": 0}
       
        dc_voltages["PV1"] = self.read_input_registers(address = self.convert_address(31319), slave=self.slave)
        dc_voltages["PV2"] = self.read_input_registers(address = self.convert_address(31321), slave=self.slave)
        dc_voltages["PV3"] = self.read_input_registers(address = self.convert_address(31323), slave=self.slave)
        dc_voltages["PV4"] = self.read_input_registers(address = self.convert_address(31325), slave=self.slave)
        dc_voltages["PV5"] = self.read_input_registers(address = self.convert_address(31327), slave=self.slave)

        dc_voltages["PV1"] = float(dc_voltages["PV1"].registers[0]) * 0.1
        dc_voltages["PV2"] = float(dc_voltages["PV2"].registers[0]) * 0.1
        dc_voltages["PV3"] = float(dc_voltages["PV3"].registers[0]) * 0.1
        dc_voltages["PV4"] = float(dc_voltages["PV4"].registers[0]) * 0.1
        dc_voltages["PV5"] = float(dc_voltages["PV5"].registers[0]) * 0.1
        
        return dc_voltages

    def read_dc_current(self):
        #TODO: CHANGE THE WAY VALUES ARE CONVERTER TO "REAL" AND ASSIGNED TO DICT
        dc_current = {"PV1": 0, "PV2": 0, "PV3": 0, "PV4": 0, "PV5": 0}
       
        dc_current["PV1"] = self.read_input_registers(address = self.convert_address(31320), slave=self.slave)
        dc_current["PV2"] = self.read_input_registers(address = self.convert_address(31322), slave=self.slave)
        dc_current["PV3"] = self.read_input_registers(address = self.convert_address(31324), slave=self.slave)
        dc_current["PV4"] = self.read_input_registers(address = self.convert_address(31326), slave=self.slave)
        dc_current["PV5"] = self.read_input_registers(address = self.convert_address(31328), slave=self.slave)

        dc_current["PV1"] = float(dc_current["PV1"].registers[0]) * 0.01
        dc_current["PV2"] = float(dc_current["PV2"].registers[0]) * 0.01
        dc_current["PV3"] = float(dc_current["PV3"].registers[0]) * 0.01
        dc_current["PV4"] = float(dc_current["PV4"].registers[0]) * 0.01
        dc_current["PV5"] = float(dc_current["PV5"].registers[0]) * 0.01
        
        return dc_current     

    def read_string_current(self):
        dc_current = {"S1": 0, "S2": 0, "S3": 0, "S4": 0, "S5": 0, "S6": 0, "S7": 0, "S8": 0, "S9": 0, "S10": 0}

        dc_current["S1"] = self.read_input_registers(address = self.convert_address(31339), slave=self.slave)
        dc_current["S2"] = self.read_input_registers(address = self.convert_address(31340), slave=self.slave)
        dc_current["S3"] = self.read_input_registers(address = self.convert_address(31341), slave=self.slave)
        dc_current["S4"] = self.read_input_registers(address = self.convert_address(31342), slave=self.slave)
        dc_current["S5"] = self.read_input_registers(address = self.convert_address(31343), slave=self.slave)
        dc_current["S6"] = self.read_input_registers(address = self.convert_address(31344), slave=self.slave)
        dc_current["S7"] = self.read_input_registers(address = self.convert_address(31345), slave=self.slave)
        dc_current["S8"] = self.read_input_registers(address = self.convert_address(31346), slave=self.slave)
        dc_current["S9"] = self.read_input_registers(address = self.convert_address(31347), slave=self.slave)
        dc_current["S10"] = self.read_input_registers(address = self.convert_address(31348), slave=self.slave)    

        dc_current["S1"] = float(dc_current["S1"].registers[0]) * 0.1
        dc_current["S2"] = float(dc_current["S2"].registers[0]) * 0.1
        dc_current["S3"] = float(dc_current["S3"].registers[0]) * 0.1
        dc_current["S4"] = float(dc_current["S4"].registers[0]) * 0.1
        dc_current["S5"] = float(dc_current["S5"].registers[0]) * 0.1
        dc_current["S6"] = float(dc_current["S6"].registers[0]) * 0.1
        dc_current["S7"] = float(dc_current["S7"].registers[0]) * 0.1
        dc_current["S8"] = float(dc_current["S8"].registers[0]) * 0.1
        dc_current["S9"] = float(dc_current["S9"].registers[0]) * 0.1
        dc_current["S10"] = float(dc_current["S10"].registers[0]) * 0.1       

        return dc_current

    def read_ac_voltage(self):
        """Returns a dictionary with L1, L2 and L3 voltage values. Values are already converter to 'real'"""
        ac_voltages = {"L1": 0, "L2": 0, "L3": 0}
        
        ac_voltages["L1"] = self.read_input_registers(address = self.convert_address(31359), slave=self.slave)
        ac_Voltages["L2"] = self.read_input_registers(address = self.convert_address(31361), slave=self.slave)
        ac_voltages["L3"] = self.read_input_registers(address = self.convert_address(31363), slave=self.slave)

        voltages["L1"] = float(ac_voltages["L1"].registers[0]) * 0.1
        voltages["L2"] = float(ac_voltages["L2"].registers[0]) * 0.1
        voltages["L3"] = float(ac_voltages["L3"].registers[0]) * 0.1

        return ac_voltages

    def read_ac_current(self):
        ac_current = {"L1": 0, "L2": 0, "L3": 0}
        
        ac_current["L1"] = self.read_input_registers(address = self.convert_address(31360), slave=self.slave)
        ac_current["L2"] = self.read_input_registers(address = self.convert_address(31362), slave=self.slave)
        ac_current["L3"] = self.read_input_registers(address = self.convert_address(31364), slave=self.slave)

        ac_current["L1"] = float(ac_current["L1"].registers[0]) * 0.1
        ac_current["L2"] = float(ac_current["L2"].registers[0]) * 0.1
        ac_current["L3"] = float(ac_current["L3"].registers[0]) * 0.1

        return ac_current

    def read_rst_lines_voltages(self):
        rst_lines_voltages = {"RS": 0, "RT": 0, "ST": 0}
        
        rst_lines_voltages["RS"] = self.read_input_registers(address = self.convert_address(31365), slave=self.slave)
        rst_lines_voltages["RT"] = self.read_input_registers(address = self.convert_address(31366), slave=self.slave)
        rst_lines_voltages["ST"] = self.read_input_registers(address = self.convert_address(31367), slave=self.slave)

        rst_lines_voltages["RS"] = float(rst_lines_voltages["RS"].registers[0]) * 0.1
        rst_lines_voltages["RT"] = float(rst_lines_voltages["RT"].registers[0]) * 0.1
        rst_lines_voltages["ST"] = float(rst_lines_voltages["ST"].registers[0]) * 0.1

        return rst_lines_voltages

    def read_grid_freq(self):
        grid_freq = self.read_input_registers(address = self.convert_address(31368), slave=self.slave)
        return float(grid_freq.registers[0]) * 0.01

    def read_apparent_power(self):
        apparent_power = self.read_input_registers(address = self.convert_address(31369), slave=self.slave, count=2)
        return apparent_power.registers
        #TODO check return type

    def read_active_power(self):
        active_power = self.read_input_registers(address = self.convert_address(31371), slave=self.slave, count=2)
        return active_power.registers
        #TODO check return type

    def read_reactive_power(self):
        reactive_power = self.read_input_registers(address = self.convert_address(31373), slave=self.slave, count=2)
        return reactive_power.registers
        #TODO check return type

    def read_power_factor(self):
        power_factor = self.read_input_registers(address = self.convert_address(31375), slave=self.slave)
        return float(power_factor.registers[0]) * 0.01

    def read_error_message(self):
        error_message = self.read_input_registers(address = self.convert_address(31378), slave=self.slave)
        return error_message.registers
        #TODO check return type

    def read_warning_message(self):
        war_message = self.read_input_registers(address = self.convert_address(31379), slave=self.slave)
        return war_message.registers
        #TODO check return type

    def read_pv_total_power(self):
        total = self.read_input_registers(address = self.convert_address(31601), slave=self.slave, count=2)
        return total.registers
        #TODO check return type

    def read_pv_e_today(self):
        total = self.read_input_registers(address = self.convert_address(31603), slave=self.slave, count=2)
        return total.registers
        #TODO check return type

    def read_pv_e_total(self):
        total = self.read_input_registers(address = self.convert_address(31605), slave=self.slave, count=2)
        return total.registers
        #TODO check return type  

    def read_battery_comm_status(self):
        com_status = self.read_input_registers(address = self.convert_address(31607), slave=self.slave)
        return com_status.registers
        #TODO check return type  

    def read_battery_status(self):
        com_status = self.read_input_registers(address = self.convert_address(31608), slave=self.slave)
        return com_status.registers
        #TODO check return type  

    def read_battery_error_status(self):
        """Returns a 16 bit binary string, refer to manual of Solplanet Modbus to read the error code it represents"""
        bat_error_status = self.read_input_registers(address = self.convert_address(31609), slave=self.slave)
        return bin(bat_error_status.registers[0])[2:]

    def read_battery_warning_status(self):
        """Returns a 16 bit binary string, refer to manual of Solplanet Modbus to read the error code it represents"""
        bat_war_status = self.read_input_registers(address = self.convert_address(31613), slave=self.slave)
        return bin(bat_war_status.registers[0])[2:]

    def read_battery_voltage(self):
        bat_vol = self.read_input_registers(address = self.convert_address(31617), slave=self.slave)
        return float(bat_vol.registers[0]) * 0.01 

    def read_battery_current(self):
        bat_cur = self.read_input_registers(address = self.convert_address(31618), slave=self.slave)
        return float(bat_cur.registers[0]) * 0.01 

    def read_battery_power(self):
        bat_power = self.read_input_registers(address = self.convert_address(31619), slave=self.slave, count=2)
        return float(bat_power.registers[1]) * 1 

    def read_battery_temp(self):
        temp = self.read_input_registers(address = self.convert_address(31621), slave=self.slave)
        return float(temp.registers[0]) * 0.1 

    def read_battery_soc(self):
        soc = self.read_input_registers(address = self.convert_address(31622), slave=self.slave)
        return float(soc.registers[0]) * 0.01 

    def read_battery_soh(self):
        soh = self.read_input_registers(address = self.convert_address(31623), slave=self.slave)
        return float(soh.registers[0]) * 0.01 

    def read_battery_charging_current_limit(self):
        limit = self.read_input_registers(address = self.convert_address(31624), slave=self.slave)
        return float(limit.registers[0]) * 0.1

    def read_battery_discharge_current_limit(self):
        limit = self.read_input_registers(address = self.convert_address(31625), slave=self.slave)
        return float(limit.registers[0]) * 0.1

    def read_battery_e_charge_today(self):
        e_today = self.read_input_registers(address = self.convert_address(31626), slave=self.slave, count=2)
        return float(e_today.registers[1]) * 1 

    def read_battery_e_discharge_today(self):
        e_today = self.read_input_registers(address = self.convert_address(31628), slave=self.slave, count=2)
        return float(e_today.registers[1]) * 1

    def read_e_consumption_today_ac(self):
        e_today = self.read_input_registers(address = self.convert_address(31630), slave=self.slave, count=2)
        return float(e_today.registers[1]) * 1

    def read_e_generation_today_ac(self):
        e_today = self.read_input_registers(address = self.convert_address(31632), slave=self.slave, count=2)
        return float(e_today.registers[1]) * 1

    def read_eps_load_voltage(self):
        eps_voltage = self.read_input_registers(address = self.convert_address(31634), slave=self.slave)
        return float(eps_voltage.registers[0]) * 0.1 

    def read_eps_load_current(self):
        eps_curr = self.read_input_registers(address = self.convert_address(31635), slave=self.slave)
        return float(eps_curr.registers[0]) * 0.1 

    def read_eps_load_freq(self):
        eps_freq = self.read_input_registers(address = self.convert_address(31636), slave=self.slave)
        return float(eps_freq.registers[0]) * 0.01

    def read_eps_load_active_power(self):
        eps_active_power = self.read_input_registers(address = self.convert_address(31637), slave=self.slave, count=2)
        return float(eps_active_power.registers[1]) * 1

    def read_eps_load_reactive_power(self):
        eps_reactive_power = self.read_input_registers(address = self.convert_address(31639), slave=self.slave, count=2)
        return float(eps_reactive_power.registers[1]) * 1

    def read_e_consumption_today_eps(self):
        e_today = self.read_input_registers(address = self.convert_address(31641), slave=self.slave, count=2)
        return float(e_today.registers[1]) * 0.1

    def read_e_consumption_total_eps(self):
        e_today = self.read_input_registers(address = self.convert_address(31643), slave=self.slave, count=2)
        return float(e_today.registers[1]) * 0.1


###Functions for decoding addresses, strings, etc

    def convert_address(self, address):
        """Returns the real value of the provided register, please input the exact register address from the Solplanet Modbus documentation"""
        address = int(str(address)[1:]) - 1
        return address

    def decode_string(self, s_input):
        """Decoded the 16 bit values of reponses into strings you can test the functionality with commented code"""
        
        #test_input = [8224,8224,16723,22321,12363,11596,21536,8224]
        #print(decode_string(test_input))
        #run the aboce code in you main file (or were you want to test this)

        s_input = self.into_binary(s_input)
        string_result = ""
        for element in s_input:
            temp1 = element[:8]
            temp2 = element[8:]
            string_result = string_result + chr(int(temp1,2)) + chr(int(temp2,2))
            
        return string_result
    
    def into_binary(self, input_array):
        for i in range(0,len(input_array)):
            input_array[i] = bin(input_array[i])[2:]
            input_array[i] = ('0' * (16 - len(input_array[i]))) + input_array[i]
        return input_array