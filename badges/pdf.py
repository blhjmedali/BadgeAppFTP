from __future__ import annotations

import os
from io import BytesIO

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from xhtml2pdf import pisa


def _xhtml2pdf_link_callback(uri: str, rel: str | None = None) -> str:
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.removeprefix(settings.MEDIA_URL))
        return path

    if uri.startswith(settings.STATIC_URL):
        static_path = uri.removeprefix(settings.STATIC_URL)
        found = finders.find(static_path)
        if found:
            return found

    if os.path.exists(uri):
        return uri

    return uri


def render_to_pdf(*, html: str, filename: str = 'badge.pdf') -> HttpResponse:
    out = BytesIO()
    result = pisa.CreatePDF(src=BytesIO(html.encode('utf-8')), dest=out, link_callback=_xhtml2pdf_link_callback)
    if result.err:
        return HttpResponse('PDF generation error', status=500)

    response = HttpResponse(out.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

