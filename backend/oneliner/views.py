from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from . import chatbotModels

@csrf_exempt
def simple_chat_bot_view(request):
    if request.method == 'POST':
        chatbot = chatbotModels.ChatbotModels()
        data = json.loads(request.body)
        response = chatbot.handle_chat(data['prompt'])
        return JsonResponse({'response': response})
    else:
        return HttpResponseBadRequest()
    
@csrf_exempt
def simple_chat_bot_with_history_view(request):
    if request.method == 'POST':
        chatbot = chatbotModels.ChatbotModels()
        data = json.loads(request.body)
        response = chatbot.handle_chat_with_history(data['prompt'], request.headers.get('session-id'))
        return JsonResponse({'response': response})
    else:
        return HttpResponseBadRequest()