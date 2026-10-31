from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("localhost", port=502)
if not client.connect():
    raise SystemExit("could not connect to the PLC")

result = client.read_coils(0, count=8)
if result.isError():
    print("Modbus error:", result)
else:
    print("coils 0-7:", result.bits[:8])

client.close()
