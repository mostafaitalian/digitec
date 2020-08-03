from django.core.exceptions import PermissionDenied
import functools
from braces.views import LoginRequiredMixin
def can_customer(request):
    if request.user.has_perm("add_customer") or request.user.is_staff:
        request.can__add_customer = True
        return request
    raise PermissionDenied('you do not have the authority to add customer and you are also not the admin')
# decorator to check if the user  is staff or has permission to add customers
def check_can_add_customer(view_func):
    @functools.wraps(view_func)
    def new_func(request,*args,**kwargs):
        request = can_customer(request)
        response = new_func(request,*args,**kwargs)
        return response
    return new_func
