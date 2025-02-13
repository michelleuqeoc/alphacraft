import ntplib
from time import ctime
import os
import ctypes
import sys

def set_system_time(new_time):
    try:
        if sys.platform.startswith('win'):
            # Convert the time to a SYSTEMTIME structure
            system_time = new_time.timetuple()[:6] + (0, 0)
            win_time = (ctypes.c_uint16 * 8)(*system_time)
            # Call Windows SetLocalTime function
            ctypes.windll.kernel32.SetLocalTime(ctypes.byref(win_time))
            print("System time updated successfully.")
        else:
            raise NotImplementedError("This function is only implemented for Windows.")
    except Exception as e:
        print(f"Failed to set system time: {e}")

def synchronize_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3)
        new_time = response.tx_time

        print("Current NTP Time:", ctime(new_time))
        set_system_time(ctime(new_time))
    except Exception as e:
        print(f"Error synchronizing time: {e}")

if __name__ == "__main__":
    print("Synchronizing system time with internet atomic clocks...")
    synchronize_time()