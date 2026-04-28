from rest_framework import authentication
from rest_framework import exceptions
from catalogue.models import Affiliate, ApiRequestLog
from django.utils import timezone

class ApiKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return None

        try:
            affiliate = Affiliate.objects.select_related('tier', 'user').get(api_key=api_key, is_active=True)
        except Affiliate.DoesNotExist:
            raise exceptions.AuthenticationFailed('Clé API invalide ou compte inactif.')

        if not affiliate.tier:
            raise exceptions.AuthenticationFailed('Aucun plan (tier) n\'est associé à ce compte API.')

        # VÉRIFICATION DU QUOTA (Optionnel mais recommandé)
        today = timezone.now().date()
        requests_today = ApiRequestLog.objects.filter(
            affiliate=affiliate, 
            created_at__date=today
        ).count()

        if requests_today >= affiliate.tier.api_limit_daily:
            raise exceptions.PermissionDenied('Quota quotidien atteint pour votre plan.')

        # ENREGISTREMENT DU LOG
        ApiRequestLog.objects.create(
            affiliate=affiliate,
            endpoint=request.path,
            method=request.method,
            status_code=200
        )

        request.affiliate = affiliate
        return (affiliate.user, None)
