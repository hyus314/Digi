from django.shortcuts import render

def chat(request):
    chat_id = request.GET.get('id')
    return render(request, 'chat.html', {'chat_id': chat_id})
