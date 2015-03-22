from django.core.urlresolvers import resolve

def namespace(request):
    current_app = {'namespace': request.resolver_match.namespace}
    if current_app['namespace'] == 'rent':
        current_app['rent'] = True
    elif current_app['namespace'] == 'sale':
        current_app['sale'] = True
    return current_app
