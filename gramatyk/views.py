from django.shortcuts import render
from gramatyk.models import Solution
from django.http import HttpResponse
from django.template import Context, loader
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from gramatyk.gramma import Gramma


def index(request):
    latest_solution_list = Solution.objects.all().order_by('-pub_date')[:15]
    context_dict = {'latest_solution_list': latest_solution_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits += 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits

    response = render(request, 'gramatyk/index.html', context_dict)

    return response


def about(request):  # zwraca about
    return render(
        request,
        'gramatyk/about.html')


def profile(request):  # zwraca podglad profilu
    return render(
        request,
        'gramatyk/profile.html')


def detail(request, solution_id):  # zwraca solucje
    try:
        p = Solution.objects.get(id=solution_id)
    except solution_id.DoesNotExist:
        raise Http404
    return render(request, 'gramatyk/detail.html', {'solution': p})


@login_required
def like_solution(request):  # zwraca ilość lajków solucji
    sol_id = None
    if request.method == 'GET':
        sol_id = request.GET['solution_id']

    likes = 0
    if sol_id:
        sol = Solution.objects.get(id=int(sol_id))
        if sol:
            likes = sol.likes + 1
            sol.likes = likes
            sol.save()
    return HttpResponse(likes)


def get_solution_list(max_results=0, starts_with=''):  # zwraca listę solucji dla wyszukiwania solucji
        sol_list = []
        if starts_with:
                sol_list = Solution.objects.filter(name__istartswith=starts_with)

        if max_results > 0:
                if len(sol_list) > max_results:
                        sol_list = sol_list[:max_results]

        return sol_list


def suggest_solution(request):  # zwraca widok wyszukiwania solucji
        sol_list = []
        res = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        sol_list = get_solution_list(8, starts_with).values('name')
        for l in sol_list:
            res += l['name'] + " "

        return HttpResponse(res)


def check_gramma(request):  # sprawdza gramatyke i zwraca ew. bledy
    grm = Gramma()
    if request.method == 'GET':
        grm.prepare_data(request.GET['gramma'])
    grm.check_syntax()
    if grm.get_error():
        return HttpResponse('BŁĄD! '+grm.get_error())  # bląd.
    else:
        if not grm.get_rules():
            return HttpResponse(grm.get_instructions())  # brak regul
        else:
            return HttpResponse(grm.get_response())

