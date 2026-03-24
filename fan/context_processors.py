from django.conf import settings

def theme(request):
    theme = request.session.get('theme', 'light')
    return {'theme': theme}