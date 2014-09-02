from django.shortcuts import get_object_or_404, redirect


def canonical(model):
    """
    Enforce a canonical URL for a resource.
    """
    def outer(view):
        def inner(request, id, slug=''):
            instance = get_object_or_404(model, pk=id)
            if not request.path == instance.get_absolute_url():
                return redirect(instance, permanent=True)
            return view(request, instance)
        return inner
    return outer
