import os
import time
import json
import shelve
from openai import OpenAI
from dotenv import load_dotenv
import requests
import tools.YtMusic.opensong as openSong
import tools.Arduino.openduino as arduino
from colorama import Fore,init

load_dotenv()

class AssistantManager:
    def __init__(self, api_key, tools_file):
        self.client = OpenAI(api_key=api_key)
        self.tools = self.load_tools(tools_file)
        self.assistant = self.create_assistant()
        self.ard = arduino.MyArduino()
        self.SketchFilePath = None
        init(autoreset=True)

    def load_tools(self, tools_file):
        with open(tools_file, 'r') as file:
            tools = json.load(file)
        return tools

    def create_assistant(self):
        assistant = self.client.beta.assistants.create(
            instructions="You name is alexa that helps me to do daily activities, like sending messages, searching song or anything, even help me to build robot. please act like jarvis or edith from iron man movie",
            model="gpt-4o",
            tools=self.tools
        )
        return assistant

    def sendmessage(self, username, message):
        response = requests.get(f"http://localhost:3000/send-message/?name={username}&message={message}") # whatsapp web.js localhost
        if response.status_code == 200:
            return f"pesan berhasil dikirim ke {username}"
        else:
            return "something wrong!"

    def playSong(self,SongName):
        result = openSong.PlaySong(SongName=SongName)
        return result
    
    def CreateNewSketch(self,NewSketchName):
        result = self.ard.CreateNewSketch(NewSketchName=NewSketchName)
        if result != "failled create new sketch, file already exist!":
            self.SketchFilePath = result
            return "success to create new sketch"
        else:
            return result
    
    def WriteCodeToSketch(self,SketchFileName,Code):
        result = self.ard.WriteCodeToSketch(SketchFileName=SketchFileName,Code=Code)
        return str(result)
    
    def CheckLib(self,libname):
        result = self.ard.CheckLib(libname=libname)
        return result
    
    def DownloadLib(self,libname):
        result = self.ard.DownloadLib(libname=libname)
        return result
    
    def Upload(self,sketchFileName):
        result = self.ard.Upload(sketchFileName=sketchFileName)
        return str(result)
    
    def OpenMonitor(self):
        return str(self.ard.OpenMonitor())

    def check_if_thread_exists(self, wa_id):
        with shelve.open("threads_db") as threads_shelf:
            return threads_shelf.get(wa_id, None)

    def store_thread(self, wa_id, thread_id):
        with shelve.open("threads_db", writeback=True) as threads_shelf:
            threads_shelf[wa_id] = thread_id

    def generate_response(self, message_body, wa_id, name, role):
        thread_id = self.check_if_thread_exists(wa_id)
        if thread_id is None:
            # print(f"Creating new thread for {name} with wa_id {wa_id}")
            thread = self.client.beta.threads.create()
            self.store_thread(wa_id, thread.id)
            thread_id = thread.id
        else:
            # print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
            thread = self.client.beta.threads.retrieve(thread_id)

        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=message_body,
        )

        new_message = self.run_assistant(thread)
        return new_message

    def run_assistant(self, thread):
        assistant = self.client.beta.assistants.retrieve(self.assistant.id)
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        # print(Fore.GREEN + "[+] "+run.status)

        while run.status != "completed":
            if run.status == "requires_action":
                action = run.required_action.submit_tool_outputs.model_dump()
                tools_output = []
                for actions in action['tool_calls']:
                    funcname = actions['function']['name']
                    arguments = json.loads(actions['function']['arguments'])
                    if funcname == "sendmessage":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.sendmessage(arguments['username'], arguments['message'])
                        })
                    if funcname == "PlaySong":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.playSong(arguments['SongName'])
                        })
                    if funcname == "CreateNewSketch":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.CreateNewSketch(NewSketchName=arguments['NewSketchName'])
                        })
                    if funcname == "WriteCodeToSketch":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.WriteCodeToSketch(SketchFileName=arguments['SketchFileName'],Code=arguments['Code'])
                        })
                    if funcname == "CheckLib":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.CheckLib(libname=arguments['libname'])
                        })
                    if funcname == "DownloadLib":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.DownloadLib(libname=arguments['libname'])
                        })
                    if funcname == "Upload":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.Upload(sketchFileName=arguments['sketchFileName'])
                        })
                    if funcname == "OpenMonitor":
                        tools_output.append({
                            "tool_call_id": actions['id'],
                            "output": self.OpenMonitor()
                        })

                self.client.beta.threads.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tools_output)
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            # print("Status is:", run.status)
            # print('\r' + ' ' * 4, end='') 
            print(f'Status is: {run.status}')

        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        new_message = messages.data[0].content[0].text.value
        print(f"\nJarvis: {new_message}")
        return new_message

# Example usage
# ast = AssistantManager(api_key="your_openai_api_key", tools_file="tools.json")
# print(ast.generate_response("saya mau pesan nasi goreng", "422", "fatihh", role='user'))
