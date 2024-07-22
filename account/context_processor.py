from django.contrib.auth.models import Group

def user_roles(request):
    if request.user.is_authenticated:
        is_manager = request.user.groups.filter(name='Manager').exists()
        is_owner = request.user.groups.filter(name='Restaurant Owner').exists()
        is_customer = request.user.groups.filter(name='Customer').exists()
    else:
        is_manager = is_owner = is_customer = False

    return {
        'is_manager': is_manager,
        'is_owner': is_owner,
        'is_customer': is_customer,
    }