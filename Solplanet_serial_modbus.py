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
        device_type = self.send_request_ir(31001) 
        return self.decode_string(device_type)
        #TODO add function to decode string value

    def read_slave_modbus_address(self):
        mb_address = self.send_request_ir(31002) 
        return int(mb_address[0])

    def read_serial_number(self):
        serial_number = self.send_request_ir(31003,16) 
        return serial_number
        #TODO add function to decode string value

    def read_machine_type(self): 
        """Returns a string with inverter model"""
        model_name = self.send_request_ir(31019,8) 
        return model_name
        #TODO add function to decode string value

    def read_current_grid_code(self):
        grid_code = self.send_request_ir(31027) 
        return grid_code[0]

    def read_rated_power(self):
        rated_power = self.send_request_ir(31028,2) 
        return rated_power
        #TODO test reponse type
        
    def read_current_software_version(self):
        current_soft_ver = self.send_request_ir(31030,8) 
        return current_soft_ver
        #TODO add function to decode string value

    def read_current_safety_version(self):
        current_safe_ver = self.send_request_ir(31044,7) 
        return current_soft_ver
        #TODO add function to decode string value
    
    def read_manufacturer_name(self):
        name = self.send_request_ir(31057,7) 
        return name
        #TODO add function to decode string value

    def read_brand_name(self):
        name = self.send_request_ir(31065,7) 
        return self.decode_string(name)

    def read_grid_rated_voltage(self):
        rated_vol = self.send_request_ir(31301)
        return float(rated_vol[0]) * 0.1

    def read_grid_rated_frequency(self):
        rated_freq = self.send_request_ir(31302)
        return float(rated_freq[0]) * 0.01

    def read_e_today(self):
        e_today = self.send_request_ir(31303, 2)
        return float(e_today[1]) * 0.1 
        
    def read_e_total(self):
        """Returns floating point number representing production in kWh"""
        e_total = self.send_request_ir(31305,2)
        return float(e_total[1]) * 0.1      

    def read_h_total(self):
        h_total = self.send_request_ir(31307,2)
        return float(h_total[1]) * 1 

    def read_device_state(self):
        state = self.send_request_ir(31309)
        return float(state[0])

    def connect_time(self):
        con_time = self.send_request_ir(31310)
        return int(con_time[0])  

    def read_air_temp(self):
        temp = self.send_request_ir(31311)
        return float(temp[0]) * 0.1 
    
    def read_inverter_phase_temp(self):
        phase_temps = {"L1": 0, "L2": 0, "L3":0}      
        phase_temps["L1"] = self.send_request_ir(31312)
        phase_temps["L2"] = self.send_request_ir(31313)
        phase_temps["L3"] = self.send_request_ir(31314)

        phase_temps["L1"] = float(phase_temps["L1"][0]) * 0.1
        phase_temps["L2"] = float(phase_temps["L2"][0]) * 0.1
        phase_temps["L3"] = float(phase_temps["L3"][0]) * 0.1

        return phase_temps

    def read_boost_temp(self):
        temp = self.send_request_ir(31315)
        return float(temp[0]) * 0.1 

    def read_bidirect_dc_conv_temp(self):
        temp = self.send_request_ir(31316)
        return float(temp[0]) * 0.1 

    def read_bus_voltage(self):
        bus_vol = self.send_request_ir(31317)
        return float(bus_vol[0]) * 0.1

    def read_dc_voltage(self):
        """Returns a dictionary with MPPT1 TO 5 voltage values. Values are already converter to 'real'"""
        #TODO: CHANGE THE WAY VALUES ARE CONVERTER TO "REAL" AND ASSIGNED TO DICT
        dc_voltages = {"PV1": 0, "PV2": 0, "PV3": 0, "PV4": 0, "PV5": 0}
        #PV4 AND PV5 RETURN VALUES 655.XX ????? TODO FIGURE OUT WHY
       
        dc_voltages["PV1"] = self.send_request_ir(31319)
        dc_voltages["PV2"] = self.send_request_ir(31321)
        dc_voltages["PV3"] = self.send_request_ir(31323)
        dc_voltages["PV4"] = self.send_request_ir(31325)
        dc_voltages["PV5"] = self.send_request_ir(31327)

        dc_voltages["PV1"] = float(dc_voltages["PV1"][0]) * 0.1
        dc_voltages["PV2"] = float(dc_voltages["PV2"][0]) * 0.1
        dc_voltages["PV3"] = float(dc_voltages["PV3"][0]) * 0.1
        dc_voltages["PV4"] = float(dc_voltages["PV4"][0]) * 0.1
        dc_voltages["PV5"] = float(dc_voltages["PV5"][0]) * 0.1
        
        return dc_voltages

    def read_dc_current(self):
        #TODO: CHANGE THE WAY VALUES ARE CONVERTER TO "REAL" AND ASSIGNED TO DICT
        dc_current = {"PV1": 0, "PV2": 0, "PV3": 0, "PV4": 0, "PV5": 0}
       
        dc_current["PV1"] = self.send_request_ir(31320)
        dc_current["PV2"] = self.send_request_ir(31322)
        dc_current["PV3"] = self.send_request_ir(31324)
        dc_current["PV4"] = self.send_request_ir(31326)
        dc_current["PV5"] = self.send_request_ir(31328)

        dc_current["PV1"] = float(dc_current["PV1"][0]) * 0.01
        dc_current["PV2"] = float(dc_current["PV2"][0]) * 0.01
        dc_current["PV3"] = float(dc_current["PV3"][0]) * 0.01
        dc_current["PV4"] = float(dc_current["PV4"][0]) * 0.01
        dc_current["PV5"] = float(dc_current["PV5"][0]) * 0.01
        
        return dc_current     

    def read_string_current(self):
        dc_current = {"S1": 0, "S2": 0, "S3": 0, "S4": 0, "S5": 0, "S6": 0, "S7": 0, "S8": 0, "S9": 0, "S10": 0}
        #{'S1': 89.60000000000001, 'S2': 1.4000000000000001, 'S3': 201.60000000000002} TODO figure out why
        dc_current["S1"] = self.send_request_ir(31339)
        dc_current["S2"] = self.send_request_ir(31340)
        dc_current["S3"] = self.send_request_ir(31341)
        dc_current["S4"] = self.send_request_ir(31342)
        dc_current["S5"] = self.send_request_ir(31343)
        dc_current["S6"] = self.send_request_ir(31344)
        dc_current["S7"] = self.send_request_ir(31345)
        dc_current["S8"] = self.send_request_ir(31346)
        dc_current["S9"] = self.send_request_ir(31347)
        dc_current["S10"] = self.send_request_ir(31348)    

        dc_current["S1"] = float(dc_current["S1"][0]) * 0.1
        dc_current["S2"] = float(dc_current["S2"][0]) * 0.1
        dc_current["S3"] = float(dc_current["S3"][0]) * 0.1
        dc_current["S4"] = float(dc_current["S4"][0]) * 0.1
        dc_current["S5"] = float(dc_current["S5"][0]) * 0.1
        dc_current["S6"] = float(dc_current["S6"][0]) * 0.1
        dc_current["S7"] = float(dc_current["S7"][0]) * 0.1
        dc_current["S8"] = float(dc_current["S8"][0]) * 0.1
        dc_current["S9"] = float(dc_current["S9"][0]) * 0.1
        dc_current["S10"] = float(dc_current["S10"][0]) * 0.1       

        return dc_current

    def read_ac_voltage(self):
        """Returns a dictionary with L1, L2 and L3 voltage values. Values are already converter to 'real'"""
        ac_voltages = {"L1": 0, "L2": 0, "L3": 0}
        
        ac_voltages["L1"] = self.send_request_ir(31359)
        ac_voltages["L2"] = self.send_request_ir(31361)
        ac_voltages["L3"] = self.send_request_ir(31363)

        ac_voltages["L1"] = float(ac_voltages["L1"][0]) * 0.1
        ac_voltages["L2"] = float(ac_voltages["L2"][0]) * 0.1
        ac_voltages["L3"] = float(ac_voltages["L3"][0]) * 0.1

        return ac_voltages

    def read_ac_current(self):
        ac_current = {"L1": 0, "L2": 0, "L3": 0}
        
        ac_current["L1"] = self.send_request_ir(31360)
        ac_current["L2"] = self.send_request_ir(31362)
        ac_current["L3"] = self.send_request_ir(31364)

        ac_current["L1"] = float(ac_current["L1"][0]) * 0.1
        ac_current["L2"] = float(ac_current["L2"][0]) * 0.1
        ac_current["L3"] = float(ac_current["L3"][0]) * 0.1

        return ac_current

    def read_rst_lines_voltages(self):
        rst_lines_voltages = {"RS": 0, "RT": 0, "ST": 0}
        
        rst_lines_voltages["RS"] = self.send_request_ir(31365)
        rst_lines_voltages["RT"] = self.send_request_ir(31366)
        rst_lines_voltages["ST"] = self.send_request_ir(31367)

        rst_lines_voltages["RS"] = float(rst_lines_voltages["RS"][0]) * 0.1
        rst_lines_voltages["RT"] = float(rst_lines_voltages["RT"][0]) * 0.1
        rst_lines_voltages["ST"] = float(rst_lines_voltages["ST"][0]) * 0.1

        return rst_lines_voltages

    def read_grid_freq(self):
        grid_freq = self.send_request_ir(31368)
        return float(grid_freq[0]) * 0.01

    def read_apparent_power(self):
        apparent_power = self.send_request_ir(31369,2)
        return apparent_power
        #TODO check return type

    def read_active_power(self):
        active_power = self.send_request_ir(31371,2)
        return active_power
        #TODO check return type

    def read_reactive_power(self):
        reactive_power = self.send_request_ir(31373,2)
        return reactive_power
        #TODO check return type

    def read_power_factor(self):
        power_factor = self.send_request_ir(31375)
        return float(power_factor[0]) * 0.01

    def read_error_message(self):
        error_message = self.send_request_ir(31378)
        return error_message
        #TODO check return type

    def read_warning_message(self):
        war_message = self.send_request_ir(31379)
        return war_message
        #TODO check return type

    def read_pv_total_power(self):
        total = self.send_request_ir(31601,2)
        return total
        #TODO check return type

    def read_pv_e_today(self):
        total = self.send_request_ir(31603,2)
        return total
        #TODO check return type

    def read_pv_e_total(self):
        total = self.send_request_ir(31605,2)
        return total
        #TODO check return type  

    def read_battery_comm_status(self):
        com_status = self.send_request_ir(31607)
        return com_status
        #TODO check return type  

    def read_battery_status(self):
        com_status = self.send_request_ir(31608)
        return com_status
        #TODO check return type  

    def read_battery_error_status(self):
        """Returns a 16 bit binary string, refer to manual of Solplanet Modbus to read the error code it represents"""
        bat_error_status = self.send_request_ir(31609)
        return bin(bat_error_status[0])[2:]

    def read_battery_warning_status(self):
        """Returns a 16 bit binary string, refer to manual of Solplanet Modbus to read the error code it represents"""
        bat_war_status = self.send_request_ir(31613)
        return bin(bat_war_status[0])[2:]

    def read_battery_voltage(self):
        bat_vol = self.send_request_ir(31617)
        return float(bat_vol[0]) * 0.01 

    def read_battery_current(self):
        bat_cur = self.send_request_ir(31618)
        return float(bat_cur[0]) * 0.01 

    def read_battery_power(self):
        bat_power = self.send_request_ir(31619,2)
        return float(bat_power[1]) * 1 

    def read_battery_temp(self):
        temp = self.send_request_ir(31621)
        return float(temp[0]) * 0.1 

    def read_battery_soc(self):
        soc = self.send_request_ir(31622)
        return float(soc[0]) * 0.01 

    def read_battery_soh(self):
        soh = self.send_request_ir(31623)
        return float(soh[0]) * 0.01 

    def read_battery_charging_current_limit(self):
        limit = self.send_request_ir(31624)
        return float(limit[0]) * 0.1

    def read_battery_discharge_current_limit(self):
        limit = self.send_request_ir(31625)
        return float(limit[0]) * 0.1

###dodać zabezpiecznie przed pustą listą

    def read_battery_e_charge_today(self):
        e_today = self.send_request_ir(31626,2)
        return float(e_today[0]) * 1 

    def read_battery_e_discharge_today(self):
        e_today = self.send_request_ir(31628,2)
        return float(e_today[1]) * 1

    def read_e_consumption_today_ac(self):
        e_today = self.send_request_ir(31630,2)
        return float(e_today[1]) * 1

    def read_e_generation_today_ac(self):
        e_today = self.send_request_ir(31632,2)
        return float(e_today[1]) * 1

    def read_eps_load_voltage(self):
        eps_voltage = self.send_request_ir(31634)
        return float(eps_voltage[0]) * 0.1 

    def read_eps_load_current(self):
        eps_curr = self.send_request_ir(31635)
        return float(eps_curr[0]) * 0.1 

    def read_eps_load_freq(self):
        eps_freq = self.send_request_ir(31636)
        return float(eps_freq[0]) * 0.01

    def read_eps_load_active_power(self):
        eps_active_power = self.send_request_ir(31637,2)
        return float(eps_active_power[1]) * 1

    def read_eps_load_reactive_power(self):
        eps_reactive_power = self.send_request_ir(31639,2)
        return float(eps_reactive_power[1]) * 1

    def read_e_consumption_today_eps(self):
        e_today = self.send_request_ir(31641, 2)
        return float(e_today[1]) * 0.1

    def read_e_consumption_total_eps(self):
        e_today = self.send_request_ir(31643, 2)
        return float(e_today[1]) * 0.1







###Functions for decoding addresses, strings, etc###
    def send_request_ir(self, address, count = 1):
        address = int(address)
        count = int(count)
        result = self.read_input_registers(address = self.convert_address(address), slave=self.slave, count=count)
        return result.registers


    def convert_address(self, address):
        """Returns the real value of the provided register, please input the exact register address from the Solplanet Modbus documentation"""
        address = int(str(address)[1:]) - 1
        return address

    def decode_string(self, s_input):
        """Decoded the 16 bit values of reponses into strings you can test the functionality with commented code"""
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

    def change_address_for_connection(self,new_address):
        self.slave = new_address
