from diplomas.geocaching.gc_diplomas import check_geoloto_for_user, check_azbuka_for_user, check_regions_for_user
from diplomas.geocaching.api import get_user_nickname, MyConnectionError
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def geoloto(request):
    try:
        user_id = request.POST['user']
    except KeyError:
        return render(request, 'diplomas/geoloto.html', {})
    try:
        max_score, cards_and_tables, n_caches = check_geoloto_for_user(user_id)
        nickname = get_user_nickname(user_id)
    except MyConnectionError as e:
        context = {'error': 'Something went wrong during connection to Geocaching.su website: %s' % str(e)}
    else:
        context = {'status': 'ok', 'score': max_score, 'cards_and_tables': cards_and_tables, 'n_caches': n_caches,
                   'user_id': user_id, 'username': nickname}

    template = loader.get_template('diplomas/geoloto.html')
    return HttpResponse(template.render(context, request))


def azbuka(request):
    try:
        user_id = request.POST['user']
    except KeyError:
        return render(request, 'diplomas/azbuka.html', {})
    try:
        azbuka_dict, letters_left = check_azbuka_for_user(user_id)
        nickname = get_user_nickname(user_id)
    except MyConnectionError as e:
        context = {'error': 'Something went wrong during connection to Geocaching.su website: %s' % str(e)}
    else:
        context = {'status': 'ok', 'score': len(azbuka_dict), 'azbuka_dict': sorted(azbuka_dict.items()),
                   'letters_left': letters_left,
                   'user_id': user_id, 'username': nickname}

    template = loader.get_template('diplomas/azbuka.html')
    return HttpResponse(template.render(context, request))


def regions(request):
    try:
        user_id = request.POST['user']
    except KeyError:
        return render(request, 'diplomas/regions.html', {})

    try:
        result_dict = check_regions_for_user(user_id)
        nickname = get_user_nickname(user_id)
    except MyConnectionError as e:
        context = {'error': 'Something went wrong during connection to Geocaching.su website: %s' % str(e)}
    else:
        n_diplomas_to_get = 0
        for region in result_dict:
            if result_dict[region]['can_get']:
                n_diplomas_to_get += 1
        context = {'status': 'ok',
                   'result_dict': sorted(result_dict.items(),
                                         key=lambda x: x[1]['max_score'] - x[1]['total_score'] - 1000 * x[1]['can_get']),
                   'n_diplomas_to_get': n_diplomas_to_get,
                   'user_id': user_id, 'username': nickname}

    template = loader.get_template('diplomas/regions.html')
    return HttpResponse(template.render(context, request))


def index(request):
    template = loader.get_template('diplomas/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
