#######################################################################################
# Yourname: Jirathip Kapanya
# Your student ID: 66070030
# Your GitHub Repo: https://github.com/FriedStan/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

from dotenv import load_dotenv
import os
import time
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

import restconf_final
import netconf_final
import netmiko_final
import ansible_final

load_dotenv()

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ROOM_ID = os.environ.get("ROOM_ID")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    ROOM_ID
)

# default function will not use restconf or netconf until specified
restconf_selected = False
netconf_selected = False

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": "Bearer {}".format(ACCESS_TOKEN)}


# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)


    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070030 "):

        # extract the command
        full_command = message[len("/66070030 "):]
        parts = full_command.split()
        
        if len(parts) == 2 and all(part.isdigit() for part in parts[0].split('.')):
            ip_address = parts[0]
            command = parts[1]
            print(f"Extracted IP: {ip_address}")
            print(f"Command: {command}")
        else:
            if all(part.isdigit() for part in full_command.split('.')):
                ip_address = full_command
                command = None
                print(f"Extracted IP: {ip_address}")
                print("No command provided.")
            else:
                command = full_command
                ip_address = None
                print(f"Command only: {command}")

# 5. Complete the logic for each command
        if command == "restconf":
            responseMessage = "Ok: Restconf"
            print("Now using Restconf")
            restconf_selected = True
            netconf_selected = False
        elif command == "netconf":
            responseMessage = "Ok: Netconf"
            print("Now using Netconf")
            restconf_selected = False
            netconf_selected = True
        elif (restconf_selected == False and netconf_selected == False) or (restconf_selected == True and netconf_selected == True):
            responseMessage = "Error: No method specified"
            print("Error: No method specified")
        elif restconf_selected == True and ip_address:
            # use restconf_final.py for the commands 
            if command == "create":
                responseMessage = restconf_final.create(ip_address)
            elif command == "delete":
                responseMessage = restconf_final.delete(ip_address)
            elif command == "enable":
                responseMessage = restconf_final.enable(ip_address)
            elif command == "disable":
                responseMessage = restconf_final.disable(ip_address)
            elif command == "status":
                responseMessage = restconf_final.status(ip_address)
            elif command == "gigabit_status":
                responseMessage = netmiko_final.gigabit_status(ip_address)
            elif command == "showrun":
                responseMessage = ansible_final.showrun(ip_address)
            else:
                responseMessage = "Error: No command or unknown command"
        elif netconf_selected == True and ip_address:
            # use netconf_final.py for the commands
            if command == "create":
                responseMessage = netconf_final.create(ip_address)
            elif command == "delete":
                responseMessage = netconf_final.delete(ip_address)
            elif command == "enable":
                responseMessage = netconf_final.enable(ip_address)
            elif command == "disable":
                responseMessage = netconf_final.disable(ip_address)
            elif command == "status":
                responseMessage = netconf_final.status(ip_address)
            elif command == "gigabit_status":
                responseMessage = netmiko_final.gigabit_status(ip_address)
            elif command == "showrun":
                responseMessage = ansible_final.showrun(ip_address)
            else:
                responseMessage = "Error: No command or unknown command"
        else:
            responseMessage = "Error: No IP specified"
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            filename = "show_run_66070030_R4.txt"
            fileobject = open(filename, "rb")
            filetype = "text/plain"
            # build multipart/form-data payload including the file
            postData = MultipartEncoder(
                fields={
                    "roomId": ROOM_ID,
                    "text": "show running config",
                    "files": (filename, fileobject, filetype),
                }
            )
            HTTPHeaders = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": postData.content_type,
            }
        # other commands only send text, or no attached file.
        else:
            postData = json.dumps({"roomId": ROOM_ID, "text": responseMessage})
            HTTPHeaders = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )

        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
