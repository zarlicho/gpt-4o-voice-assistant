# from subprocess import *
# import os

# error = open('error.txt', 'w')
# command = fr'arduino-cli compile --upload "F:\python project\whatsapp-bot\waWhisper\voiceAssistant\tools\Arduino\ESP32_Project" --port COM7 --fqbn esp32:esp32:esp32-poe-iso'
# run(command,shell=True)

# import pyduinocli,json

# arduino = pyduinocli.Arduino("arduino-cli")
# brds = arduino.board.list()

# try:
#     print(arduino.monitor(port="COM5",fqbn="arduino:avr:uno"))
# except Exception as e:
#     print(e.result['__stderr'])

# # arduino.compile(fqbn=fqbn, sketch="upload_me")
# try:
#     result = arduino.compile(fqbn="esp32:esp32:esp32-poe-iso", sketch=r"F:\python project\whatsapp-bot\waWhisper\voiceAssistant\tools\Arduino\ESP32_Project\ESP32_Project.ino")
#     results = arduino.upload(fqbn="esp32:esp32:esp32-poe-iso", sketch=r"F:\python project\whatsapp-bot\waWhisper\voiceAssistant\tools\Arduino\ESP32_Project\ESP32_Project.ino", port="COM7")
    
#     print(results)
# except Exception as e:
#     if e.result['result'] == '':
#         print(e.result['__stderr'])
#     else:
#         x = [(err['message'],err['line']) for err in e.result['result']['builder_result']['diagnostics']]

    
import time

i = 15
while True:
    print('\r' + ' ' * 4, end='')  # Clear the line
    print(f'\r{i}s', end='', flush=True)
    i -= 1
    time.sleep(1)
    if i < 0:  # Condition to break the loop
        break
