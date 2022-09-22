import ui
from time import sleep

import lostik

ui.static_content()
ui.insert_module_version('v0.6')
ui.insert_module_name('Send File')
ui.insert_firmware_version(lostik.get_ver())
ui.insert_hweui(lostik.get_hweui())
ui.insert_frequency(lostik.get_freq())
sleep(5)