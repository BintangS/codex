
# Create your views here.
# Import the session_data dictionary from consumers
from codex.consumers import session_data
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Session, Recording
from codex.consumers import session_data


import json
from codex import  chatbotModels

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
@require_http_methods(["GET"])
def heatmap_view(request):
    return render(request, 'heatmap.html')

@require_http_methods(["GET"])
def test_page_view(request):
    return render(request, 'test_page.html')

@require_http_methods(["GET"])
def list_sessions(request):
    sessions = [{'session_id': session.id, 'active': session.active} for session in Session.objects.all()]
    return JsonResponse(sessions, safe=False)

@require_http_methods(["GET"])
def get_heatmap_data(request, session_id):
    if session_id in session_data:
        return JsonResponse(session_data[session_id], safe=False)
    else:
        try:
            recording = Recording.objects.get(session__id=session_id)
            print(recording)
            return JsonResponse(recording.data, safe=False)
        except Recording.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)

@require_http_methods(["DELETE"])
def delete_session(request, session_id):
    try:
        session = Session.objects.get(id=session_id)
        session.delete()
        return JsonResponse({'success': True})
    except Session.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)