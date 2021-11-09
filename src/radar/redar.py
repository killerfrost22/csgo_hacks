import pymem
import re

pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle,'client.dll')

clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
address = client.lpBaseOfDll + re.search(rb'\x83\xE0\x0F\x80\xBF',clientModule).start() + 9

pm.write_uchar(address, 0 if pm.read_uchar(address) != 0 else 2)
pm.close_process()