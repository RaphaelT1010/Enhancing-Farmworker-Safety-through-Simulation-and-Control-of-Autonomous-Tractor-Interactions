#!/usr/bin/python3.7

import serial
import time
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

mainloop = None
ser = None

def movement_signal_received(m_state):
    global ser
    command = None
    if m_state == 117:
        command = b'w\r\n'
    elif m_state == 108:
        command = b'a\r\n'
    elif m_state == 114:
        command = b'd\r\n'
    elif m_state == 100:
        command = b's\r\n'
    elif m_state == 0:
        ser.close()
        mainloop.quit()
        return
    else:
        return
    ser.write(command)

def main():

    ser = serial.Serial('/dev/ttyUSB1/', 9600)
    time.sleep(2)

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    bus.add_signal_receiver(movement_signal_received, dbus_interface='tractorsquad.dummy.Movement', signal_name='MoveStateSignal')

    mainloop = Glib.MainLoop()
    mainloop.run()

if __name__ == '__main__':
    main()
