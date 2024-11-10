from pymodbus.client import ModbusSerialClient, ModbusBaseClient

class Solplanet_Serial_Modbus(ModbusSerialClient):
    def __init__(self, baud_rate = 9600, byte_size = 8, parity = "N", stop_bits = 1, s_port = ""):
        super().__init__(port = s_port, baudrate = baud_rate, bytesize=byte_size, parity = parity, stopbits = stop_bits)

    def read_device_type(self, device_address = 3):
        device_type = self.send_request_ir(31001, slave = device_address) 
        return self.decode_string(device_type)

    def read_slave_modbus_address(self, device_address = 3):
        mb_address = self.send_request_ir(31002, slave = device_address) 
        return int(mb_address[0])

    def read_serial_number(self, device_address = 3):
        serial_number = self.send_request_ir(31003,16, slave = device_address) 
        return self.decode_string(serial_number)

    def read_machine_type(self, device_address = 3): 
        """Returns a string with inverter model"""
        model_name = self.send_request_ir(31019,8, slave = device_address) 
        return self.decode_string(model_name)

    def read_current_grid_code(self, device_address = 3):
        grid_code = self.send_request_ir(31027, slave = device_address) 
        grid_code_dict = {
                    8: "GR PPC",
                    35: "NB/T32004:2018",
                    47: "AU AS 4777.2:2015",
                    48: "NZ AS 4777.2:2015",
                    49: "ENG5-50Hz",
                    50: "ENGG-60Hz",
                    51: "TOR Erzeuger Typ A V1.1",
                    54: "CNS15382:2018",
                    59: "EN 50549-1",
                    65: "NL EN50549-1:2019",
                    66: "BR NBR 16149:2013",
                    67: "VDE0126-1-1/A1/VFR",
                    68: "IEC 61727 50Hz",
                    69: "C10/11:2019",
                    70: "VDE-AR-N4105:2018",
                    71: "IEC 61727 60Hz",
                    72: "G98/1",
                    73: "G99/1",
                    74: "AU AS/NZS4777.2:2020 A",
                    75: "AU AS/NZS4777.2:2020 B",
                    76: "AU AS/NZS4777.2:2020 C",
                    77: "NZ AS/NZS4777.2:2020 A",
                    78: "IL 54177.3",
                    79: "KK KS C 8565:2020",
                    80: "ES UNE206007-1",
                    81: "CY EN50549-1",
                    82: "CS PPDS A1",
                    83: "PL EN50549-1",
                    84: "CEI 0-21:2019",
                    85: "DK EN50549-1",
                    86: "CH NA/EEA-NE7",
                    87: "SE EIFS:2018",
                    88: "FI EN50549-1",
                    89: "RO Order208",
                    90: "SI EN50549-1",
                    91: "LV EN50549-1",
                    92: "VDE0126/VFR2019 IS (50Hz)",
                    93: "VDE0126/VFR2019 IS (60Hz)",
                    94: "ZA NRS 097-2-1:2017",
                    95: "BR PORTARIA No.140",
                    96: "NTS 631 Type A",
                    97: "NTS 631 Type B",
                    98: "NO EN50549-1",
                    99: "VDE-AR-N 4110",
                    100: "EN 50549-2",
                    101: "DEWA:2016",
                    102: "DK1 EN50549-1",
                    103: "ZA RPPs"
                }

        for key in grid_code_dict.keys():
            if key == int(grid_code[0]):
                grid_code = grid_code_dict[key]
                break
    
        return grid_code

    def read_rated_power(self, device_address = 3):
        rated_power = self.send_request_ir(31028,2, slave = device_address) 
        return int(rated_power[1]) * 1.0
        
    def read_current_software_version(self, device_address = 3):
        current_soft_ver = self.send_request_ir(31030,8, slave = device_address) 
        return self.decode_string(current_soft_ver)

    def read_current_safety_version(self, device_address = 3):
        current_safe_ver = self.send_request_ir(31044,7, slave = device_address) 
        return self.decode_string(current_safe_ver)
    
    def read_manufacturer_name(self, device_address = 3):
        name = self.send_request_ir(31057,7, slave = device_address) 
        return self.decode_string(name)

    def read_brand_name(self, device_address = 3):
        name = self.send_request_ir(31065,7, slave = device_address) 
        return self.decode_string(name)

    def read_inverter_model(self, device_address = 3):
        model = self.send_request_ir(31073, slave = device_address)
        model_dict = {
                1: "PV Single phase1-3kW",
                2: "PV Single phase3-6kW",
                3: "PV Three phase3-10kW",
                4: "PV Three phase15-23kW",
                5: "PV Three phase50-60kW",
                11: "HY Single phase1-3kW",
                12: "HY Single phase3-6kW",
                13: "HY Three phase5-12kW",
                14: "HY Single phase<1kW (Compass)",
                15: "HY Three phase without EPS5-12kW",
                16: "HY Three phase with diesel5-12kW"
            }
        for key in model_dict.keys():
            if key == int(model[0]):
                model = model_dict[key]
                break
        return model

    def read_grid_rated_voltage(self, device_address = 3):
        rated_vol = self.send_request_ir(31301, slave = device_address)
        return float(rated_vol[0]) * 0.1

    def read_grid_rated_frequency(self, device_address = 3):
        rated_freq = self.send_request_ir(31302, slave = device_address)
        return float(rated_freq[0]) * 0.01

    def read_e_today(self, device_address = 3):
        e_today = self.send_request_ir(31303, 2, slave = device_address)
        return float(e_today[1]) * 0.1 
        
    def read_e_total(self, device_address = 3):
        """Returns floating point number representing production in kWh"""
        e_total = self.send_request_ir(31305,2, slave = device_address)
        return float(e_total[1]) * 0.1      

    def read_h_total(self, device_address = 3):
        h_total = self.send_request_ir(31307,2, slave = device_address)
        return float(h_total[1]) * 1 

    def read_device_state(self, device_address = 3):
        state = self.send_request_ir(31309, slave = device_address)
        return float(state[0])

    def connect_time(self, device_address = 3):
        con_time = self.send_request_ir(31310, slave = device_address)
        return int(con_time[0])  

    def read_internal_temp(self, device_address = 3):
        temp = self.send_request_ir(31311, slave = device_address)
        return float(temp[0]) * 0.1 
    
    def read_inverter_phase_temp(self, device_address = 3):
        phase_temps = {"L1": 0, "L2": 0, "L3":0}      
        phase_temps["L1"] = self.send_request_ir(31312, slave = device_address)
        phase_temps["L2"] = self.send_request_ir(31313, slave = device_address)
        phase_temps["L3"] = self.send_request_ir(31314, slave = device_address)

        phase_temps["L1"] = float(phase_temps["L1"][0]) * 0.1
        phase_temps["L2"] = float(phase_temps["L2"][0]) * 0.1
        phase_temps["L3"] = float(phase_temps["L3"][0]) * 0.1

        return phase_temps

    def read_boost_temp(self, device_address = 3):
        temp = self.send_request_ir(31315, slave = device_address)
        return float(temp[0]) * 0.1 

    def read_bidirect_dc_conv_temp(self, device_address = 3):
        temp = self.send_request_ir(31316)
        return float(temp[0]) * 0.1 

    def read_bus_voltage(self, device_address = 3):
        bus_vol = self.send_request_ir(31317)
        return float(bus_vol[0]) * 0.1

    def read_dc_voltage(self, device_address = 3):
        """Returns a dictionary with MPPT1 TO 5 voltage values. Values are already converter to 'real'"""
        #TODO: CHANGE THE WAY VALUES ARE CONVERTER TO "REAL" AND ASSIGNED TO DICT
        dc_voltages = {"PV1": 0, "PV2": 0, "PV3": 0, "PV4": 0, "PV5": 0}
        #PV4 AND PV5 RETURN VALUES 655.XX ????? TODO FIGURE OUT WHY
       
        dc_voltages["PV1"] = self.send_request_ir(31319, slave = device_address)
        dc_voltages["PV2"] = self.send_request_ir(31321, slave = device_address)
        dc_voltages["PV3"] = self.send_request_ir(31323, slave = device_address)
        dc_voltages["PV4"] = self.send_request_ir(31325, slave = device_address)
        dc_voltages["PV5"] = self.send_request_ir(31327, slave = device_address)

        dc_voltages["PV1"] = float(dc_voltages["PV1"][0]) * 0.1
        dc_voltages["PV2"] = float(dc_voltages["PV2"][0]) * 0.1
        dc_voltages["PV3"] = float(dc_voltages["PV3"][0]) * 0.1
        dc_voltages["PV4"] = float(dc_voltages["PV4"][0]) * 0.1
        dc_voltages["PV5"] = float(dc_voltages["PV5"][0]) * 0.1
        
        return dc_voltages

    def read_dc_current(self, device_address = 3):
        #TODO: CHANGE THE WAY VALUES ARE CONVERTER TO "REAL" AND ASSIGNED TO DICT
        dc_current = {"PV1": 0, "PV2": 0, "PV3": 0, "PV4": 0, "PV5": 0}
       
        dc_current["PV1"] = self.send_request_ir(31320, slave = device_address)
        dc_current["PV2"] = self.send_request_ir(31322, slave = device_address)
        dc_current["PV3"] = self.send_request_ir(31324, slave = device_address)
        dc_current["PV4"] = self.send_request_ir(31326, slave = device_address)
        dc_current["PV5"] = self.send_request_ir(31328, slave = device_address)

        dc_current["PV1"] = float(dc_current["PV1"][0]) * 0.01
        dc_current["PV2"] = float(dc_current["PV2"][0]) * 0.01
        dc_current["PV3"] = float(dc_current["PV3"][0]) * 0.01
        dc_current["PV4"] = float(dc_current["PV4"][0]) * 0.01
        dc_current["PV5"] = float(dc_current["PV5"][0]) * 0.01
        
        return dc_current     

    def read_string_current(self, device_address = 3):
        dc_current = {"S1": 0, "S2": 0, "S3": 0, "S4": 0, "S5": 0, "S6": 0, "S7": 0, "S8": 0, "S9": 0, "S10": 0}
        #{'S1': 89.60000000000001, 'S2': 1.4000000000000001, 'S3': 201.60000000000002} TODO figure out why
        dc_current["S1"] = self.send_request_ir(31339, slave = device_address)
        dc_current["S2"] = self.send_request_ir(31340, slave = device_address)
        dc_current["S3"] = self.send_request_ir(31341, slave = device_address)
        dc_current["S4"] = self.send_request_ir(31342, slave = device_address)
        dc_current["S5"] = self.send_request_ir(31343, slave = device_address)
        dc_current["S6"] = self.send_request_ir(31344, slave = device_address)
        dc_current["S7"] = self.send_request_ir(31345, slave = device_address)
        dc_current["S8"] = self.send_request_ir(31346, slave = device_address)
        dc_current["S9"] = self.send_request_ir(31347, slave = device_address)
        dc_current["S10"] = self.send_request_ir(31348, slave = device_address)    

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

    def read_ac_voltage(self, device_address = 3):
        """Returns a dictionary with L1, L2 and L3 voltage values. Values are already converter to 'real'"""
        ac_voltages = {"L1": 0, "L2": 0, "L3": 0}
        
        ac_voltages["L1"] = self.send_request_ir(31359, slave = device_address)
        ac_voltages["L2"] = self.send_request_ir(31361, slave = device_address)
        ac_voltages["L3"] = self.send_request_ir(31363, slave = device_address)

        ac_voltages["L1"] = float(ac_voltages["L1"][0]) * 0.1
        ac_voltages["L2"] = float(ac_voltages["L2"][0]) * 0.1
        ac_voltages["L3"] = float(ac_voltages["L3"][0]) * 0.1

        return ac_voltages

    def read_ac_current(self, device_address = 3):
        ac_current = {"L1": 0, "L2": 0, "L3": 0}
        
        ac_current["L1"] = self.send_request_ir(31360, slave = device_address)
        ac_current["L2"] = self.send_request_ir(31362, slave = device_address)
        ac_current["L3"] = self.send_request_ir(31364, slave = device_address)

        ac_current["L1"] = float(ac_current["L1"][0]) * 0.1
        ac_current["L2"] = float(ac_current["L2"][0]) * 0.1
        ac_current["L3"] = float(ac_current["L3"][0]) * 0.1

        return ac_current

    def read_rst_lines_voltages(self, device_address = 3):
        rst_lines_voltages = {"RS": 0, "RT": 0, "ST": 0}
        
        rst_lines_voltages["RS"] = self.send_request_ir(31365, slave = device_address)
        rst_lines_voltages["RT"] = self.send_request_ir(31366, slave = device_address)
        rst_lines_voltages["ST"] = self.send_request_ir(31367, slave = device_address)

        rst_lines_voltages["RS"] = float(rst_lines_voltages["RS"][0]) * 0.1
        rst_lines_voltages["RT"] = float(rst_lines_voltages["RT"][0]) * 0.1
        rst_lines_voltages["ST"] = float(rst_lines_voltages["ST"][0]) * 0.1

        return rst_lines_voltages

    def read_grid_freq(self, device_address = 3):
        grid_freq = self.send_request_ir(31368, slave = device_address)
        return float(grid_freq[0]) * 0.01

    def read_apparent_power(self, device_address = 3):
        #TODO CHECK THE FIRST VALUE IN THE RETURN REGISTERS MOST LIKELY CAN BE OMMITED
        apparent_power = self.send_request_ir(31369,2, slave = device_address)
        return int(apparent_power[1]) * 1.0

    def read_active_power(self, device_address = 3):
        #TODO CHECK THE FIRST VALUE IN THE RETURN REGISTERS MOST LIKELY CAN BE OMMITED
        active_power = self.send_request_ir(31371,2, slave = device_address)
        return int(active_power[1]) * 1.0

    def read_reactive_power(self, device_address = 3):
        #TODO CHECK THE FIRST VALUE IN THE RETURN REGISTERS MOST LIKELY CAN BE OMMITED
        reactive_power = self.send_request_ir(31373,2, slave = device_address)
        return int(reactive_power[1]) * 1.0

    def read_power_factor(self, device_address = 3):
        power_factor = self.send_request_ir(31375, slave = device_address)
        return float(power_factor[0]) * 0.01

    def read_error_message(self, device_address = 3):
        error_message = self.send_request_ir(31378, slave = device_address)
        return int(error_message[0])

    def read_warning_message(self, device_address = 3):
        war_message = self.send_request_ir(31379, slave = device_address)
        return int(war_message[0])

    def read_pv_total_power(self, device_address = 3):
        #NOTE I DO NOT KNOW WHAT THIS IS
        #TODO check first register, most likely can be ommited
        total = self.send_request_ir(31601,2, slave = device_address)
        return float(total[1]) * 0.1
        
    def read_pv_e_today(self, device_address = 3):
        #TODO check first register, most likely can be ommited
        total = self.send_request_ir(31603,2, slave = device_address)
        return float(total[1]) * 0.1

    def read_pv_e_total(self, device_address = 3):
        #TODO check first register, most likely can be ommited
        total = self.send_request_ir(31605,2, slave = device_address)
        return float(total[1]) * 0.1

#########################################################################################
###TODO dodać zabezpiecznie przed pustą listą, falowniki zwykłe zwracają pustą wartość###
#########################################################################################        

    def read_battery_comm_status(self, device_address = 3):
        com_status = self.send_request_ir(31607, slave = device_address)
        if (int(com_status[0]) == 10):
            return "Normal"
        else: 
            return "Error"

    def read_battery_status(self, device_address = 3):
        com_status = self.send_request_ir(31608, slave = device_address)
        if int(com_status[0]) == 0: return "Not available"
        elif int(com_status[0]) == 1: return "Idle"
        elif int(com_status[0]) == 2: return "Charging"
        elif int(com_status[0]) == 3: return "Discharging"
        elif int(com_status[0]) == 4: return "Error"

    def read_battery_error_status(self, device_address = 3):
        """Returns a 16 bit binary string, refer to manual of Solplanet Modbus to read the error code it represents"""
        #TODO change so it returns error string the binary values represent
        bat_error_status = self.send_request_ir(31609, slave = device_address)
        return bin(bat_error_status[0])[2:]

    def read_battery_warning_status(self, device_address = 3):
        """Returns a 16 bit binary string, refer to manual of Solplanet Modbus to read the error code it represents"""
        #TODO change so it returns error string the binary values represent
        bat_war_status = self.send_request_ir(31613, slave = device_address)
        return bin(bat_war_status[0])[2:]

    def read_battery_voltage(self, device_address = 3):
        bat_vol = self.send_request_ir(31617, slave = device_address)
        return float(bat_vol[0]) * 0.01 

    def read_battery_current(self, device_address = 3):
        bat_cur = self.send_request_ir(31618, slave = device_address)
        return float(bat_cur[0]) * 0.01 

    def read_battery_power(self, device_address = 3):
        #TODO check first register, most likely can be ommited
        bat_power = self.send_request_ir(31619,2, slave = device_address)
        return float(bat_power[1]) * 1 

    def read_battery_temp(self, device_address = 3):
        temp = self.send_request_ir(31621, slave = device_address)
        return float(temp[0]) * 0.1 

    def read_battery_soc(self, device_address = 3):
        soc = self.send_request_ir(31622, slave = device_address)
        return float(soc[0]) * 0.01 

    def read_battery_soh(self, device_address = 3):
        soh = self.send_request_ir(31623, slave = device_address)
        return float(soh[0]) * 0.01 

    def read_battery_charging_current_limit(self, device_address = 3):
        limit = self.send_request_ir(31624, slave = device_address)
        return float(limit[0]) * 0.1

    def read_battery_discharge_current_limit(self, device_address = 3):
        limit = self.send_request_ir(31625, slave = device_address)
        return float(limit[0]) * 0.1

    def read_battery_e_charge_today(self, device_address = 3):
        e_today = self.send_request_ir(31626,2, slave = device_address)
        return float(e_today[0]) * 1 

    def read_battery_e_discharge_today(self, device_address = 3):
        #TODO check first register, most likely can be ommited
        e_today = self.send_request_ir(31628,2, slave = device_address)
        return float(e_today[1]) * 1

    def read_e_consumption_today_ac(self, device_address = 3):
        #TODO check first register, most likely can be ommited
        e_today = self.send_request_ir(31630,2, slave = device_address)
        return float(e_today[1]) * 1

    def read_e_generation_today_ac(self, device_address = 3):
        #TODO check first register, most likely can be ommited
        e_today = self.send_request_ir(31632,2, slave = device_address)
        return float(e_today[1]) * 1

    def read_eps_load_voltage(self, device_address = 3):
        eps_voltage = self.send_request_ir(31634, slave = device_address)
        return float(eps_voltage[0]) * 0.1 

    def read_eps_load_current(self, device_address = 3):
        eps_curr = self.send_request_ir(31635, slave = device_address)
        return float(eps_curr[0]) * 0.1 

    def read_eps_load_freq(self, device_address = 3):
        eps_freq = self.send_request_ir(31636, slave = device_address)
        return float(eps_freq[0]) * 0.01

    def read_eps_load_active_power(self, device_address = 3):
        eps_active_power = self.send_request_ir(31637,2, slave = device_address)
        return float(eps_active_power[1]) * 1

    def read_eps_load_reactive_power(self, device_address = 3):
        eps_reactive_power = self.send_request_ir(31639,2, slave = device_address)
        return float(eps_reactive_power[1]) * 1

    def read_e_consumption_today_eps(self, device_address = 3):
        e_today = self.send_request_ir(31641, 2, slave = device_address)
        return float(e_today[1]) * 0.1

    def read_e_consumption_total_eps(self, device_address = 3):
        e_today = self.send_request_ir(31643, 2, slave = device_address)
        return float(e_today[1]) * 0.1

###Functions for decoding addresses, strings, etc###
    def send_request_ir(self, address, count = 1, slave = 3):
        """Read input registers (code 0x04)."""
        address = int(address)
        count = int(count)
        result = self.read_input_registers(address = self.convert_address(address), slave=slave, count=count)
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
