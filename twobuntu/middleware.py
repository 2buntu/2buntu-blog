from django.shortcuts import render

from twobuntu.routers import ReadOnlyError


class ReadOnlyMiddleware(object):
    """
    Catch ReadOnlyError exceptions and display the appropriate error page.
    """

    def process_exception(self, request, exception):
        if isinstance(exception, ReadOnlyError):
            return render(request, 'error.html', {
                'title': 'Write Error',
                'description': "This operation cannot be performed while operating in read-only mode.",
            })
