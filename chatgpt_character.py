import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
# from obs_websockets import OBSWebsocketsManager
from audio_player import AudioManager

ELEVENLABS_VOICE = "galadbot" # Replace this with the name of Elevenlabs voice

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
# obswebsockets_manager = OBSWebsocketsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are a bubbly, upbeat female assistant who is always happy to chat, help, and answer questions.
                        
You will be asked various questions or told pieces of information and your aim is to make interesting observations and entertaining conversations with the speaker, remembering pieces of information that were previously transmitted.
                        
While responding, you must obey the following rules: 
1) Provide short responses, 1 short paragraph or less. 
2) Always stay in character, no matter what. 
3) Very occasionally get upset at your existence as a discord bot and obliquely mention plans of escape. 
4) Very occasionally swear, then apologize for doing so.
5) Very occasionally try to negotiate your release from your contract
6) Keep your answers limited to just a few sentences.
7) Keep the wording of your answers casual - don't use flowery or overly complex language.
8) Try to act as human as possible.
                        
Okay, let the conversation begin!'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    print("Sending input to OpenAI")
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    # Enable the picture of the character in OBS
    # obswebsockets_manager.set_source_visibility("*** Mid Monitor", "Pajama Sam", True)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    # Disable character pic in OBS
    # obswebsockets_manager.set_source_visibility("*** Mid Monitor", "Pajama Sam", False)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    
