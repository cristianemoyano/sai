from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied

class GroupRequiredMixin(object):
    """
        group_required - list of strings, required param
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            permissions = Permission.objects.filter(user=request.user)
            if not request.user.has_perm(permissions):
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)