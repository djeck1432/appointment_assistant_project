from django.core.management.base import BaseCommand, CommandError
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
import re
from anyio import create_task_group,run

PATTERN = r'(Екатеринбурге|Екатеринбург|Москву|Москве|Владивостоке|Владивосток)'

class Command(BaseCommand):
    help = 'Parse telegram channel for fetch required info about reservation'

    def add_arguments(self, parser):
        parser.add_argument('channel_name' , help='parse tg channel')


    def handle(self,*args,**options):
        parse_tg = options['channel_name']
        run(start_telegram_client,parse_tg)


def get_city_name(message):
    result_match = re.search(PATTERN, message)
    if not result_match:
        return None

    city_name = result_match[0]
    if city_name in ('Москву','Москве'):
        return 'Москва'
    elif city_name in ('Екатеринбурге','Екатеринбург'):
        return 'Екатеринбург'
    elif city_name in ('Владивостоке','Владивосток'):
        return 'Владивосток'


async def check_new_message(client,chat_name='test'):
    async with client:
        @client.on(events.NewMessage(chats=(chat_name)))
        async def normal_handler(event):
            try:
                new_message = event.message.to_dict()['message']
                print('work')
                city_name = get_city_name(new_message)
                return city_name
            except Exception as exc:
                print(exc)

        await client.run_until_disconnected()


async def start_telegram_client(channel_name):
    load_dotenv()
    api_id = os.getenv('APP_API_ID')
    api_hash = os.getenv('APP_API_HASH')

    client = TelegramClient('session_name', api_id, api_hash)

    async with create_task_group() as tg:
        await tg.spawn(check_new_message,client,channel_name)



def test_re_expression():
    message = '🤖 Появлялись места на собеседование в Москве: Tuesday January 21, 2020.'
    assert  re.findall(PATTERN, message)

    message = 'Открыто немного мест в Pony Express в Москву'
    assert re.findall(PATTERN, message)

    message = 'Открыт почти весь апрель в Екатеринбурге'
    assert  re.findall(PATTERN, message)

    message = 'Открыто немного мест в Pony Express в Екатеринбург'
    assert re.findall(PATTERN, message)

    message = 'С 16 марта консульство США во Владивостоке временно отменяет собеседования на неиммиграционные визы.'
    assert  re.findall(PATTERN,message)

    message = '🎉 Открыт Владивосток'
    assert re.findall(PATTERN,message)

    message = 'Подача на визу семьей. Как внести родственников в личный кабинет?'
    assert  not re.findall(PATTERN,message)
