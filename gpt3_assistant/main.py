from gpt3_assistant.clients.google_text_to_speech_client import GoogleTextToSpeechClient
from gpt3_assistant.command_line_parser import CommandLineParser
from gpt3_assistant.computer_voice_responder import ComputerVoiceResponder
from gpt3_assistant.conversation import Conversation
from gpt3_assistant.helpers.get_input_device_from_user import get_input_device_from_user
from gpt3_assistant.helpers.set_keyboard_interrupt_handler import (
    set_keyboard_interrupt_handler,
)
from gpt3_assistant.helpers.set_log_level import set_log_level
from gpt3_assistant.input_devices import InputDevices
from gpt3_assistant.open_ai_text_generator import OpenAITextGenerator
from gpt3_assistant.speech_listener import SpeechListener

if __name__ == "__main__":
    options = CommandLineParser.parse()

    # set log level from CLI options
    set_log_level(options.log_level)

    # get all input devices on the current machine
    input_devices = InputDevices.get_list_of_input_devices()

    # ask the user which input device to use for this session
    input_device = get_input_device_from_user(
        input_devices=input_devices, input_device_name=options.input_device_name
    )

    # service to listen for speech and convert it to text
    listener = SpeechListener(input_device)

    # service to generate text given an input
    text_generator = OpenAITextGenerator(options.open_ai_key)

    google_text_to_speech_client = GoogleTextToSpeechClient(options.lang, options.tld)

    # service to respond to the user the generated text
    responder = ComputerVoiceResponder(google_text_to_speech_client, "temp.mp3")

    # set interrupt to exit the process when Cmd+C / Ctrl+C is hit
    set_keyboard_interrupt_handler()

    conversation = Conversation(
        listener=listener,
        text_generator=text_generator,
        responder=responder,
        safe_word=options.safe_word,
    )

    conversation.start_conversation()
