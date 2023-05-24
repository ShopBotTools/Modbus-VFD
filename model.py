import threading
import minimalmodbus
import modbus_settings as MB
import user_inputs

lock = threading.Lock()

class VFDModel:
    def __init__(self, com_port):
        self.disconnected = False
        # Create "instrument" that can perform read and write
        # operations and import it's settings from the modbus settings module
        try:
            self.vfd = minimalmodbus.Instrument(com_port, MB.MB_ADDRESS)
            self.vfd.mode = minimalmodbus.MODE_RTU
            self.vfd.serial.parity = minimalmodbus.serial.PARITY_NONE
            self.vfd.serial.baudrate = MB.BAUDRATE
            self.vfd.serial.bytesize = MB.BYTESIZE
            self.vfd.serial.stopbits = MB.STOPBITS
            self.vfd.serial.timeout  = MB.TIMEOUT
            self.vfd.clear_buffers_before_each_transaction = MB.CLEAR_BUFFERS_BEFORE_CALL
            self.vfd.close_port_after_each_call = MB.CLEAR_BUFFERS_AFTER_CALL
            self.vfd.debug = MB.DEBUG
        except minimalmodbus.ModbusException as e:
            # Handle modbus communication error
            print("Modbus Exception:", e)
        except Exception as e:
            print("Exception: ", e)
            self.disconnected = True

    def write_VFD(self, user_input):
        speed_set = False
        speed_package = user_inputs.set_user_speed(user_input)

        if speed_package != "NaN" and speed_package != "OL":
            speed_set = True

        ## Send the request to the vfd
        def send_to_vfd(register, data, function_code, decimals = 0, signed = False):
            with lock:
                self.vfd.write_register(register, data, decimals, function_code, signed)
                self.vfd.serial.close()

        # If the speed has been set correctly then pass on the speed package as
        # well as the register position to the function to send to the VFD
        if speed_set:
            print("Attempting unlock drive")
            send_to_vfd(MB.UNLOCK_DRIVE, MB.PASSWORD, MB.WRITE_SINGLE_REGISTER)
            print("Attempting unlock parameters")
            send_to_vfd(MB.UNLOCK_PARAMETERS, MB.PASSWORD, MB.WRITE_SINGLE_REGISTER)
            print("Attempting set frequency")
            send_to_vfd(MB.SET_FREQUENCY, speed_package, MB.WRITE_SINGLE_REGISTER)

    def read_VFD(self):
        # Read data from the device
        with lock:
            try:
                # Read data from the device
                data = self.vfd.read_registers(MB.READ_FREQUENCY, MB.READ_LENGTH, MB.READ_REGISTER)
                self.vfd.serial.close()
                return data

            except minimalmodbus.ModbusException as e:
                # Handle modbus communication error
                print("Modbus Exception:", e)
            except Exception as e:
                # Handle other exceptions
                print("Exception:", e)
