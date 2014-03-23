from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

def canonical(model):
    """Enforce a canonical URL for a resource."""
    def outer(view):
        def inner(request, id, slug):
            instance = get_object_or_404(model, pk=id)
            if not request.path == instance.get_absolute_url():
                return redirect(instance, permanent=True)
            return view(request, instance)
        return inner
    return outer

def protect(fn):
    """Protect a resource with a lambda."""
    def outer(view):
        def inner(*args, **kwargs):
            if not fn(*args, **kwargs):
                raise Http404
            return view(*args, **kwargs)
        return inner
    return outer
