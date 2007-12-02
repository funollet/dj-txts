from django.views.generic import date_based
from txts.views import section_aware


@section_aware
def archive_index (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_index (request, **kwargs)

@section_aware
def archive_year (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_year (request, **kwargs)

@section_aware
def archive_month (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_month (request, **kwargs)

@section_aware
def archive_week (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_week (request, **kwargs)

@section_aware
def archive_day (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_day (request, **kwargs)

@section_aware
def archive_today (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.archive_today (request, **kwargs)

@section_aware
def object_detail (request, **kwargs):
    """Wrapped generic view, per-section customization."""
    return date_based.object_detail (request, **kwargs)


