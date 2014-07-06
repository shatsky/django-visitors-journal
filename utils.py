from django.db import transaction

@transaction.commit_on_success # to prevent view failures if journal request causes database error
def journal_event(journal, request, event_dict):
    """Adds journal event"""
    try: journal.objects.create(address=(request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')), agent=request.META.get('HTTP_USER_AGENT'), referer=request.META.get('HTTP_REFERER'), **event_dict)
    except: pass
