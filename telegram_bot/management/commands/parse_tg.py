from django.core.management.base import BaseCommand, CommandError
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import re


class Command(BaseCommand):
    help = 'Parse telegram channel for fetch required info about reservation'

    def add_arguments(self, parser):
        parser.add_argument('channel_name' , help='parse tg channel')

    def check_new_message(self,chat_name='test'):
        load_dotenv()
        api_id = os.getenv('APP_API_ID')
        api_hash = os.getenv('APP_API_HASH')

        client = TelegramClient('session_name', api_id, api_hash)

        @client.on(events.NewMessage(chats=(chat_name)))
        async def normal_handler(event):
            try:
                new_message = event.message.to_dict()['message']
                regular_expresion = re.findall('(Екатеринбурге|Москву|Москве|Екатеринбург)', new_message)
                if regular_expresion:
                    _, date = new_message.split(':')
                    return date
            except Exception as exc:
                print(exc)

        client.start()

        client.run_until_disconnected()

    def handle(self,*args,**options):
        parse_tg = options['channel_name']
        self.check_new_message(chat_name=parse_tg)


def test_re_expresion():
    message = '🤖 Появлялись места на собеседование в Москве: Tuesday January 21, 2020.'
    assert  re.findall('(Екатеринбурге|Москву|Москве|Екатеринбург)', message)

