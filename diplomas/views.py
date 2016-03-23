from diplomas.geocaching.gc_diplomas import check_geoloto_for_user, check_azbuka_for_user
from diplomas.geocaching.api import get_user_nickname
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def geoloto(request):
    try:
        user_id = request.POST['user']
    except KeyError:
        return render(request, 'diplomas/geoloto.html', {})
    max_score, cards_and_tables, n_caches = check_geoloto_for_user(user_id)

    template = loader.get_template('diplomas/geoloto.html')
    context = {'status': 'ok', 'score': max_score, 'cards_and_tables': cards_and_tables, 'n_caches': n_caches,
               'user_id': user_id, 'username': get_user_nickname(user_id)}
    return HttpResponse(template.render(context, request))

def azbuka(request):
    try:
        user_id = request.POST['user']
    except KeyError:
        return render(request, 'diplomas/azbuka.html', {})
    azbuka_dict, letters_left = check_azbuka_for_user(user_id)

    template = loader.get_template('diplomas/azbuka.html')
    context = {'status': 'ok', 'score': len(azbuka_dict), 'azbuka_dict': sorted(azbuka_dict.items()),
               'letters_left': letters_left,
               'user_id': user_id, 'username': get_user_nickname(user_id)}
    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('diplomas/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
