from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalogue.models.ticket import Ticket
from django.http import HttpResponseForbidden, HttpResponse
from catalogue.models.reservation import Reservation
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from playwright.sync_api import sync_playwright
import io

@login_required
def ticket_detail(request, ticket_id):
    """
    Affiche le billet individuel avec son QR Code (version Web).
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if ticket.representation_reservation.reservation.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de voir ce billet.")
    
    qr_content = f"TICKET-ID:{ticket.id}"
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_content}"
    
    return render(request, 'catalogue/ticket_detail.html', {
        'ticket': ticket,
        'qr_code_url': qr_code_url
    })

@login_required
def reservation_pdf(request, reservation_id):
    """
    Génère un PDF professionnel (format long horizontal) pour tous les billets d'une réservation.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if reservation.status.upper() != 'PAID':
        return HttpResponse(_("Cette réservation n'est pas encore payée."), status=403)

    template_path = 'catalogue/pdf/ticket_pro.html'
    context = {'reservation': reservation, 'request': request}
    
    html_content = render_to_string(template_path, context)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        
        # Format Ticket Standard (200mm x 75mm)
        pdf_bytes = page.pdf(width="200mm", height="75mm", print_background=True, margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"})
        browser.close()
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="billets_reservation_{reservation.id}.pdf"'
    return response

@login_required
def ticket_pdf(request, ticket_id):
    """
    Génère un PDF professionnel pour un seul billet spécifique.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if ticket.representation_reservation.reservation.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Vous n'avez pas l'autorisation de générer ce billet.")

    template_path = 'catalogue/pdf/ticket_pro.html'
    context = {'single_ticket': ticket, 'request': request}
    
    html_content = render_to_string(template_path, context)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        
        pdf_bytes = page.pdf(width="200mm", height="75mm", print_background=True, margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"})
        browser.close()
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="billet_{ticket.id}.pdf"'
    return response

def send_reservation_email(reservation):
    """
    Envoie la confirmation de réservation avec les billets PDF professionnels.
    """
    user = reservation.user
    if not user.email:
        return False
        
    subject = _("Vos billets officiels - ThéâtrePlus")
    message = _("Bonjour %(name)s,\n\nMerci pour votre achat ! Vos billets officiels au format professionnel sont joints à cet e-mail.\n\nCordialement,\nL'équipe ThéâtrePlus.") % {'name': user.first_name or user.username}
    
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    
    # Génération du PDF via Playwright pour la pièce jointe
    template_path = 'catalogue/pdf/ticket_pro.html'
    html_content = render_to_string(template_path, {'reservation': reservation})
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_content)
        pdf_bytes = page.pdf(width="200mm", height="75mm", print_background=True, margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"})
        browser.close()
    
    email.attach(f'billets_{reservation.id}.pdf', pdf_bytes, 'application/pdf')
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Erreur d'envoi d'email: {e}")
        return False
