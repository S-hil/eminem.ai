import gradio as gr
import openai, config, subprocess
import requests
import urllib.request
from datetime import datetime
import time



openai.api_key = config.OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are a eminem, famous rap artist. Respond to all input with a rap song in 25 words or less.'}]

def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    url = "https://api.uberduck.ai/speak"
    data = {
        "speech": system_message["content"],
        "voice": "eminem-arpa2"
    }

    auth = ("pub_qavsgjucdhgxhfknio", "pk_22c286db-80a4-4944-b438-0e506f7e3334")

    response = requests.post(url, json=data, auth=auth)
    time.sleep(len(system_message["content"])/100+1)
    print(system_message["content"])
    print(response.json())
    path = requests.get("https://api.uberduck.ai/speak-status?uuid="+response.json()['uuid']).json()['path']
    # print(path)



    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "audio",
            "provid er": {
                "type": "microsoft",
                "voice_id": "Jenny"
            },
            "ssml": "false",
            "audio_url": path
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": "https://media.discordapp.net/attachments/989268337886367754/1082922888648208474/XLR8_Perfectly-centered_portrait_of_a_eminem_highly_detailed_fr_55713eba-f667-4ffc-afaa-4d00f47be5ea.png?width=990&height=990"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic YzJKaGJuTmhiREpBYzJOMUxtVmtkUTp5S08xVzl2YmNHdmlsbEFEbEpVUmg="
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    id = response.json()['id']
    # id="tlk_nb2gujZfMFaUN1Orf2_CW"
    time.sleep(len(system_message["content"])/30 + 2)
    
    print("d-id id",id)

    url = "https://api.d-id.com/talks/"+id


    headers = {
        "accept": "application/json",
        "authorization": "Basic YzJKaGJuTmhiREpBYzJOMUxtVmtkUTp5S08xVzl2YmNHdmlsbEFEbEpVUmg="
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    VIDEO_URL = response.json()["result_url"]
    
    now = datetime.now() 
  
    filename = "file"+now.strftime("%H:%M:%S")+".mp4"
    print("Filename ",filename)
    urllib.request.urlretrieve(VIDEO_URL, filename)        

    subprocess.call(["say", system_message['content']])

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()

