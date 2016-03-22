from diplomas.main import get_user_result
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def geoloto(request):
    try:
        user_id = request.POST['user']
    except KeyError:
        return render(request, 'diplomas/geoloto.html', {})
    max_score, cards_and_tables, n_caches = get_user_result(user_id)

    template = loader.get_template('diplomas/geoloto.html')
    context = {'status': 'ok', 'score': max_score, 'cards_and_tables': cards_and_tables, 'n_caches': n_caches,
               'user_id': user_id}
    return HttpResponse(template.render(context, request))
