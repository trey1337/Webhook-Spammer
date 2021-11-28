from logging import *
from ctypes import windll
from os import system, name
from tasksio import TaskPool
from secrets import token_hex
from aiohttp import ClientSession
from asyncio import get_event_loop, sleep


basicConfig(level=INFO, format='[\u001b[34;1m%(asctime)s\u001b[0m] %(message)s', datefmt='%I:%M:%S')


class Info:

    def __init__(self):
        self.Clear = lambda: system('cls' if name == 'nt' else 'clear')
        self.Color = '\u001b[34;1m'
        self.Reset = '\u001b[0m' 
        
    def AppTitle(title: str) -> str: return windll.kernel32.SetConsoleTitleW(title)

    def Ascii() -> str:
        return '''
     
        [38;2;5;189;245m╦[38;2;5;186;245m [38;2;5;183;245m╦[38;2;5;180;245m╔[38;2;5;177;245m═[38;2;5;174;245m╗[38;2;5;171;245m╔[38;2;5;168;245m╗[38;2;5;165;245m [38;2;5;162;245m╦[38;2;5;159;245m [38;2;5;156;245m╦[38;2;5;153;245m╔[38;2;5;150;245m═[38;2;5;147;245m╗[38;2;5;144;245m╔[38;2;5;141;245m═[38;2;5;138;245m╗[38;2;5;135;245m╦[38;2;5;132;245m╔[38;2;5;129;245m═[38;2;5;126;245m [38;2;5;123;245m [38;2;5;120;245m╔[38;2;5;117;245m═[38;2;5;114;245m╗[38;2;5;111;245m╔[38;2;5;108;245m═[38;2;5;105;245m╗[38;2;5;102;245m╔[38;2;5;99;245m═[38;2;5;96;245m╗[38;2;5;93;245m╔[38;2;5;90;245m╦[38;2;5;87;245m╗[38;2;5;84;245m╔[38;2;5;81;245m╦[38;2;5;78;245m╗[38;2;5;75;245m╔[38;2;5;72;245m═[38;2;5;69;245m╗[38;2;5;66;245m╦[38;2;5;63;245m═[38;2;5;60;245m╗
        [38;2;5;189;245m║[38;2;5;186;245m║[38;2;5;183;245m║[38;2;5;180;245m║[38;2;5;177;245m╣[38;2;5;174;245m [38;2;5;171;245m╠[38;2;5;168;245m╩[38;2;5;165;245m╗[38;2;5;162;245m╠[38;2;5;159;245m═[38;2;5;156;245m╣[38;2;5;153;245m║[38;2;5;150;245m [38;2;5;147;245m║[38;2;5;144;245m║[38;2;5;141;245m [38;2;5;138;245m║[38;2;5;135;245m╠[38;2;5;132;245m╩[38;2;5;129;245m╗[38;2;5;126;245m [38;2;5;123;245m [38;2;5;120;245m╚[38;2;5;117;245m═[38;2;5;114;245m╗[38;2;5;111;245m╠[38;2;5;108;245m═[38;2;5;105;245m╝[38;2;5;102;245m╠[38;2;5;99;245m═[38;2;5;96;245m╣[38;2;5;93;245m║[38;2;5;90;245m║[38;2;5;87;245m║[38;2;5;84;245m║[38;2;5;81;245m║[38;2;5;78;245m║[38;2;5;75;245m║[38;2;5;72;245m╣[38;2;5;69;245m [38;2;5;66;245m╠[38;2;5;63;245m╦[38;2;5;60;245m╝
        [38;2;5;189;245m╚[38;2;5;186;245m╩[38;2;5;183;245m╝[38;2;5;180;245m╚[38;2;5;177;245m═[38;2;5;174;245m╝[38;2;5;171;245m╚[38;2;5;168;245m═[38;2;5;165;245m╝[38;2;5;162;245m╩[38;2;5;159;245m [38;2;5;156;245m╩[38;2;5;153;245m╚[38;2;5;150;245m═[38;2;5;147;245m╝[38;2;5;144;245m╚[38;2;5;141;245m═[38;2;5;138;245m╝[38;2;5;135;245m╩[38;2;5;132;245m [38;2;5;129;245m╩[38;2;5;126;245m [38;2;5;123;245m [38;2;5;120;245m╚[38;2;5;117;245m═[38;2;5;114;245m╝[38;2;5;111;245m╩[38;2;5;108;245m [38;2;5;105;245m [38;2;5;102;245m╩[38;2;5;99;245m [38;2;5;96;245m╩[38;2;5;93;245m╩[38;2;5;90;245m [38;2;5;87;245m╩[38;2;5;84;245m╩[38;2;5;81;245m [38;2;5;78;245m╩[38;2;5;75;245m╚[38;2;5;72;245m═[38;2;5;69;245m╝[38;2;5;66;245m╩[38;2;5;63;245m╚[38;2;5;60;245m═
        [0;00m

        '''

class Main:

    def __init__(self, webhook: str, message: str, username: str):
        self.webhook = webhook
        self.message = message
        self.username = username

    async def WebhookSpam(self):
        try:
            async with ClientSession() as session:
                async with session.post(self.webhook, data = {'content': f'{self.message} | `{token_hex(5)}`', 'username': f'{self.username} | {token_hex(5)}'}) as response:
                        if response.status == 204:
                            info(f'[Success] -> Sent a message | {self.message}')
                        elif 'retry_after' in await response.text():
                            json = await response.json()
                            info(f'[Error] Ratelimited, Sleeping for {json["retry_after"]} seconds')
                            await sleep(json["retry_after"])
        except: pass

    async def Start(self, thread, webhook: str, message: str, username: str, amount: int):
      async with TaskPool(thread) as task:
        for _ in range(int(amount)):
          await task.put(Main(webhook, message, username).WebhookSpam())    


if __name__ == '__main__':
    (Info().Clear(), Info.AppTitle('WebhookSpammer - github.com/trey1337'), print(Info.Ascii()))
    threads = input(f'{Info().Color}[Configuration]{Info().Reset} Threads: ')
    webhook = input(f'{Info().Color}[Configuration]{Info().Reset} Webhook Link: ')
    message = input(f'{Info().Color}[Configuration]{Info().Reset} Message to Spam: ')
    username = input(f'{Info().Color}[Configuration]{Info().Reset} Webhook Username: ')
    amount = input(f'{Info().Color}[Configuration]{Info().Reset} Amount: ')
    Info().Clear()
    get_event_loop().run_until_complete(Main(webhook, message, username).Start(int(threads), webhook, message, username, amount));exit(0)
