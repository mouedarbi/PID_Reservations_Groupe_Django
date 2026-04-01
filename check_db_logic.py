import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Show, Representation

print(f"{'Show Title':<30} | {'Show Location':<20} | {'Rep Location':<20}")
print("-" * 75)

representations = Representation.objects.select_related('show', 'location', 'show__location').all()

for rep in representations:
    show_loc = rep.show.location.designation if rep.show.location else "None"
    rep_loc = rep.location.designation if rep.location else "None"
    
    status = ""
    if rep.location and rep.show.location and rep.location != rep.show.location:
        status = "!!! INCONSISTENT !!!"
    elif not rep.location and not rep.show.location:
        status = "(No location defined)"
        
    print(f"{rep.show.title[:30]:<30} | {show_loc:<20} | {rep_loc:<20} {status}")
