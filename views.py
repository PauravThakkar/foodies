from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserSetting

@login_required
def settings(request):
    user_setting = UserSetting.objects.filter(user=request.user).first()
    if not user_setting:
        user_setting = UserSetting.objects.create(user=request.user)

    if request.method == 'POST':
        user_setting.favorite_cuisine = request.POST.get('favorite_cuisine')
        user_setting.notifications_enabled = 'on' in request.POST.getlist('notifications_enabled')
        user_setting.email_frequency = request.POST.get('email_frequency')
        user_setting.save()
        return redirect('settings')

    return render(request, 'settings.html', {'user_setting': user_setting})
