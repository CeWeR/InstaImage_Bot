import telepot
import json
from .parser import parseImage, parseVideo
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

token = '228726550:AAGBuuCcf7UCUZ-QNZyH4qBggyZk4ZX4esA'

telegramBot = telepot.Bot(token)

def showHelp():
    return render_to_string('help.md')

class BotView(View):
    def post(self, request, botToken):
        if botToken != token:
            return HttpResponseForbidden('Invalid token')

        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']

            if 'text' in payload['message']:
                cmd = payload['message'].get('text')
                if cmd == '/start' or cmd == '/help':
                    text = showHelp()
                    telegramBot.sendMessage(chat_id=chat_id, text=text)
                else:
                    image = parseImage(cmd)
                    video = parseVideo(cmd)
                    if video != '-1':
                        telegramBot.sendVideo(chat_id=chat_id, video=video)
                    elif image != '-1':
                        telegramBot.sendPhoto(chat_id=chat_id, photo=image)
                    else:
                        telegramBot.sendMessage(chat_id=chat_id, text='Wrong url!')
            else:
                telegramBot.sendMessage(chat_id=chat_id, text='Just send url of photo!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BotView, self).dispatch(request, *args, **kwargs)
