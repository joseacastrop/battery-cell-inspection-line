import time
from pymodbus.client import ModbusTcpClient

START, STOP, BELT = 8, 9, 10    # coils for start_pb, stop_pb, belt_moving
MOTOR, BEACON = 0, 1            # coils for motor_run, start_beacon

client = ModbusTcpClient("localhost", port=502)
if not client.connect():
    raise SystemExit("could not connect to the PLC")

def outputs():
    bits = client.read_coils(0, count=2).bits
    return {"motor_run": bits[MOTOR], "start_beacon": bits[BEACON]}

client.write_coil(STOP, False)
client.write_coil(START, True)     # press Start...
time.sleep(0.2)
client.write_coil(START, False)    # ...and release it

for i in range(10):
    print(f"t={i * 0.5:.1f}s", outputs())
    time.sleep(0.5)

client.write_coil(STOP, True)      # press Stop to leave the PLC idle
time.sleep(0.2)
client.write_coil(STOP, False)
print("after stop:", outputs())
client.close()
