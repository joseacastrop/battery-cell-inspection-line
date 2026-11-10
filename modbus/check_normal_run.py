
import time
from pymodbus.client import ModbusTcpClient

START, STOP, BELT = 8, 9, 10
MOTOR, BEACON, NO_MOTION = 0, 1, 2


def pulse(client, coil, seconds=0.2):
    client.write_coil(coil, True)
    time.sleep(seconds)
    client.write_coil(coil, False)


client = ModbusTcpClient("localhost", port=502)
if not client.connect():
    raise SystemExit("could not connect to the PLC")

readings = []  # (seconds, motor_run, belt_no_motion)
belt_set = False
try:
    client.write_coil(BELT, False)   # belt sensor starts off
    pulse(client, STOP)              # reset to a known state
    time.sleep(0.5)
    pulse(client, START)
    t0 = time.time()
    while time.time() - t0 < 7:
        result = client.read_coils(0, count=3)
        if result.isError():
            raise SystemExit(f"Modbus error: {result}")
        t = time.time() - t0
        motor, no_motion = result.bits[MOTOR], result.bits[NO_MOTION]
        if motor and not belt_set:
            client.write_coil(BELT, True)   # belt starts moving
            belt_set = True
        readings.append((t, motor, no_motion))
        print(f"t={t:.1f}s motor_run={motor} belt_no_motion={no_motion} belt_moving_sent={belt_set}")
        time.sleep(0.5)
finally:
    client.write_coil(BELT, False)   # always reset the sensor
    pulse(client, STOP)              # always leave the PLC idle
    client.close()

motor_ran = False
alarm_seen = False
for t, m, nm in readings:
    if m:
        motor_ran = True
    if nm:
        alarm_seen = True

if motor_ran and not alarm_seen:
    print("PASS")
else:
    print(f"FAIL: motor_ran={motor_ran} alarm_seen={alarm_seen}")