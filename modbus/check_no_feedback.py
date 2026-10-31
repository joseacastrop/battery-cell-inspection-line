import time
from pymodbus.client import ModbusTcpClient

START, STOP = 8, 9
MOTOR, BEACON, NO_MOTION = 0, 1, 2


def pulse(client, coil, seconds=0.2):
    client.write_coil(coil, True)
    time.sleep(seconds)
    client.write_coil(coil, False)


client = ModbusTcpClient("localhost", port=502)
if not client.connect():
    raise SystemExit("could not connect to the PLC")

readings = []  # (seconds, motor_run, belt_no_motion)
try:
    pulse(client, STOP)        # reset to a known state
    time.sleep(0.5)            # let the timers clear
    pulse(client, START)       # press Start; belt_moving is never set
    t0 = time.time()
    while time.time() - t0 < 7:
        result = client.read_coils(0, count=3)
        if result.isError():
            raise SystemExit(f"Modbus error: {result}")
        t = time.time() - t0
        motor, no_motion = result.bits[MOTOR], result.bits[NO_MOTION]
        readings.append((t, motor, no_motion))
        print(f"t={t:.1f}s motor_run={motor} belt_no_motion={no_motion}")
        time.sleep(0.5)
finally:
    pulse(client, STOP)        # always leave the PLC idle
    client.close()

motor_ran = any(m for t, m, nm in readings)
early_alarm = any(nm for t, m, nm in readings if t < 4.0)
final_alarm = readings[-1][2]

if motor_ran and final_alarm and not early_alarm:
    print("PASS")
else:
    print(f"FAIL: motor_ran={motor_ran} early_alarm={early_alarm} final_alarm={final_alarm}")
