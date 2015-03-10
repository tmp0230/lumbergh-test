from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render

from funfactory.monkeypatches import patch


# Activate funfactory monkeypatches.
patch()


# Autodiscover admin.py files.
admin.autodiscover()


def error_page(request, template, status=None):
    """Render error templates, found in the root /templates directory.

    If no status parameter is explcitedly passed, this function assumes
    your HTTP status code is the same as your template name (i.e. passing
    a template=404 will render 404.html with the HTTP status code 404).
    """
    return render(request, '%d.html' % template, status=(status or template))


handler404 = lambda r: error_page(r, 404)
handler500 = lambda r: error_page(r, 500)


urlpatterns = patterns('',
    (r'', include('careers.careers.urls')),
    (r'', include('careers.university.urls')),
    (r'', include('careers.taobao.urls')),

    # Admin interface.
    (r'^admin/', include(admin.site.urls)),

    # Generate a robots.txt
    (r'^robots\.txt$', lambda r: HttpResponse(
        "User-agent: *\n%s: /" % 'Allow' if settings.ENGAGE_ROBOTS else 'Disallow' ,
        mimetype="text/plain"
    ))
)


## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^404$', handler404),
        (r'^500$', handler500),
    )

