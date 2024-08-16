import pyduinocli
import json
import re,os
from subprocess import *

class MyArduino:
    def __init__(self):
        self.sketch = None
        self.arduinoPath = r'F:\python project\whatsapp-bot\waWhisper\voiceAssistant\tools\Arduino\arduino-cli.exe'
        self.arduino = pyduinocli.Arduino(self.arduinoPath)
        self.port = None
        self.fqbn = None
        self.Setup()

    def Setup(self):
        try:
            brds = self.arduino.board.list()
            self.port = brds['result']['detected_ports'][0]['port']['address']
            if "matching_boards" not in brds['result']['detected_ports'][0]:
                self.fqbn = "esp32:esp32:esp32-poe-iso"
            else:
                self.fqbn = brds['result']['detected_ports'][0]['matching_boards'][0]['fqbn']
        except Exception as e:
            pass      

    def CreateNewSketch(self,NewSketchName):
        print(f"Create new {NewSketchName} Sketch...")
        sketchfile = os.path.join(os.getcwd(),f"tools\Arduino\{NewSketchName}\{NewSketchName}.ino")
        try:
            self.arduino.sketch.new(os.path.join(os.getcwd(),f"tools\Arduino\{NewSketchName}"))
            self.sketch = sketchfile
            return self.sketch
        except Exception as e:
            return "failled create new sketch, file already exist!"
        
    def WriteCodeToSketch(self,SketchFileName,Code):
        print(f"Writing code to {SketchFileName} Sketch...")
        directory = os.path.join(os.getcwd(),"tools\Arduino")
        pathDir = os.listdir(directory)
        pattern = re.compile(SketchFileName,re.IGNORECASE)
        for index,dirpath in enumerate(pathDir):
            if pattern.search(dirpath):
                if os.path.exists(os.path.join(directory,f'{pathDir[index]}')):
                    with open(os.path.join(directory,f'{pathDir[index]}/{pathDir[index]}.ino'),'w') as f:
                        f.write(Code)
                    return "success to write sketch!"
                else:
                    return "sketch doesn't exists!"
    
    def GetLib(self):
        liblist = []
        for lib in self.arduino.lib.list()['result']['installed_libraries']:
            liblist.append(lib['library']['name'])
        return liblist
    
    def CheckLib(self,libname):
        print(f"Checking {libname}...")
        liblist = None
        result = []
        if "," in libname:
            liblist = libname.split(",")
        else:
            liblist = [libname]
        for libQuery in liblist:
            pattern = re.compile(libQuery,re.IGNORECASE)
            print(liblist)
            lib = self.GetLib()
            # print(lib)
            for index, libs in enumerate(lib):
                if pattern.search(libs):
                    # print(index)
                    result.append(lib[index])
        return str(result)
            
    def DownloadLib(self,libname):
        print(f"Downloading {libname}...")
        liblist = None
        result = []
        if "," in libname:
            liblist = libname.split(",")
        else:
            liblist = [libname]
        for LibNames in liblist:
            try:
                self.arduino.lib.install(libraries=[LibNames])
                result.append(f"installing the {LibNames} librarry was successfully!")
            except Exception as e:
                result.append(e.result['__stderr'])
        return str(result)
    
    def Upload(self,sketchFileName):
        directory = os.path.join(os.getcwd(),"tools\Arduino")
        pathDir = os.listdir(directory)
        pattern = re.compile(sketchFileName,re.IGNORECASE)
        for index,dirpath in enumerate(pathDir):
            if pattern.search(dirpath):
                # print(os.path.join(directory,pathDir[index]))
                if os.path.exists(os.path.join(directory,pathDir[index])):
                    try:
                        print(f"Compiling {sketchFileName} sketch...")
                        self.arduino.compile(fqbn=self.fqbn, sketch=os.path.join(directory,f'{pathDir[index]}\{pathDir[index]}.ino'))
                        print(f"Uploading {sketchFileName} to board...")
                        self.arduino.upload(fqbn=self.fqbn, sketch=os.path.join(directory,f'{pathDir[index]}\{pathDir[index]}.ino'), port=self.port)
                        return "success to uploading sketch to board"
                    except Exception as e:
                        if e.result['result'] == '':
                            return str(e.result['__stderr'])
                        else:
                            return [(err['message'],err['line']) for err in e.result['result']['builder_result']['diagnostics']]
                else:
                    return "sketch not exists"
        
    def OpenMonitor(self):
        try:
            command = f'start cmd.exe /C "arduino-cli monitor --port COM7 --fqbn {self.fqbn}"'
            Popen(command,shell=True)
        except Exception as e:
            return "failed when opening serial monitor"
        
