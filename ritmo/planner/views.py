from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

from .models import Task, DayData, UserPreference

DEFAULT_TIMES = [
    '5:00 AM','6:00 AM','7:00 AM','8:00 AM','9:00 AM','10:00 AM',
    '11:00 AM','12:00 PM','1:00 PM','2:00 PM','3:00 PM','4:00 PM',
    '5:00 PM','6:00 PM','7:00 PM','8:00 PM','9:00 PM','10:00 PM'
]

def get_theme(request):
    if request.user.is_authenticated:
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        return pref.theme
    return 'dark'


def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        error = 'Invalid username or password.'
    return render(request, 'planner/login.html', {'error': error, 'theme': 'dark'})


def register_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if not username or not password:
            error = 'Username and password are required.'
        elif password != password2:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, password=password)
            UserPreference.objects.create(user=user)
            login(request, user)
            return redirect('home')
    return render(request, 'planner/register.html', {'error': error, 'theme': 'dark'})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    theme = get_theme(request)
    return render(request, 'planner/app.html', {
        'page': 'home',
        'theme': theme,
        'username': request.user.username,
    })


@login_required
def calendar_view(request):
    theme = get_theme(request)
    return render(request, 'planner/app.html', {
        'page': 'calendar',
        'theme': theme,
        'username': request.user.username,
    })


@login_required
def day_view(request, day_key):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', day_key):
        return redirect('home')
    theme = get_theme(request)
    return render(request, 'planner/app.html', {
        'page': 'day',
        'day_key': day_key,
        'theme': theme,
        'username': request.user.username,
    })


# ── API ─────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['GET', 'POST'])
def api_tasks(request):
    TAGS = {
        'urgent': {'id':'urgent','label':'🔥 Urgent','color':'#E8564A','bg':'#FDECEA','dbg':'rgba(232,86,74,.15)'},
        'focus':  {'id':'focus', 'label':'💎 Focus',  'color':'#7060CC','bg':'#EDEAF8','dbg':'rgba(112,96,204,.15)'},
        'health': {'id':'health','label':'🌿 Health', 'color':'#3A9E6A','bg':'#E0F2EA','dbg':'rgba(58,158,106,.15)'},
        'create': {'id':'create','label':'✦ Creative','color':'#D08830','bg':'#FDF3DC','dbg':'rgba(208,136,48,.15)'},
        'social': {'id':'social','label':'💬 Social', 'color':'#C060A0','bg':'#F8E4F4','dbg':'rgba(192,96,160,.15)'},
        'chill':  {'id':'chill', 'label':'🌙 Chill',  'color':'#4890C8','bg':'#E0EEFC','dbg':'rgba(72,144,200,.15)'},
    }
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user).order_by('created_at')
        data = [{'id': t.task_id, 'name': t.name, 'tag': TAGS.get(t.tag_id, TAGS['focus'])} for t in tasks]
        return JsonResponse({'tasks': data})
    elif request.method == 'POST':
        body = json.loads(request.body)
        task_id = body.get('id')
        name = body.get('name', '').strip()[:200]
        tag_id = body.get('tag_id', 'focus')
        if not task_id or not name:
            return JsonResponse({'error': 'invalid'}, status=400)
        Task.objects.get_or_create(
            user=request.user, task_id=task_id,
            defaults={'name': name, 'tag_id': tag_id}
        )
        return JsonResponse({'ok': True})


@login_required
@require_http_methods(['DELETE'])
def api_task_delete(request, task_id):
    Task.objects.filter(user=request.user, task_id=task_id).delete()
    return JsonResponse({'ok': True})


@login_required
@require_http_methods(['GET', 'POST'])
def api_day_data(request, day_key):
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', day_key):
        return JsonResponse({'error': 'invalid key'}, status=400)

    if request.method == 'GET':
        try:
            dd = DayData.objects.get(user=request.user, day_key=day_key)
            return JsonResponse({'times': dd.get_times(), 'sched': dd.get_sched()})
        except DayData.DoesNotExist:
            return JsonResponse({'times': DEFAULT_TIMES, 'sched': {}})

    elif request.method == 'POST':
        body = json.loads(request.body)
        dd, _ = DayData.objects.get_or_create(user=request.user, day_key=day_key)
        if 'times' in body:
            dd.set_times(body['times'])
        if 'sched' in body:
            dd.set_sched(body['sched'])
        dd.save()
        return JsonResponse({'ok': True})


@login_required
@require_http_methods(['POST'])
def api_theme(request):
    body = json.loads(request.body)
    theme = body.get('theme', 'dark')
    pref, _ = UserPreference.objects.get_or_create(user=request.user)
    pref.theme = theme
    pref.save()
    return JsonResponse({'ok': True})
