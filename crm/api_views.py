from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from crm.models.lead import Lead
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import uuid
import os

class BearerTokenAuthentication(BaseAuthentication):
    """
    Custom authentication using a single bearer token from environment variable
    """
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
            
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
            
        token = parts[1]
        env_token = os.environ.get('API_BEARER_TOKEN')
        
        if not env_token or token != env_token:
            raise AuthenticationFailed('Invalid token')
            
        # Use a system user or create a default API user
        try:
            user = User.objects.get(email=os.environ.get('API_USER_EMAIL', 'api@example.com'))
        except User.DoesNotExist:
            # You might want to create a default user here or handle this differently
            raise AuthenticationFailed('API user not configured')
            
        return (user, None)

class B2BProspectCreateView(APIView):
    """
    API endpoint to create new prospects with only an email address
    Authentication: Bearer Token from environment variable
    """
    authentication_classes = [BearerTokenAuthentication]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email address is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'error': 'Invalid email format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if prospect with this email already exists
        if Lead.objects.filter(email=email).exists():
            return Response(
                {'error': 'Prospect with this email already exists'}, 
                status=status.HTTP_409_CONFLICT
            )
        
        # Create a new prospect
        try:
            # Get the API user
            created_by = request.user
            
            # Generate a unique reference ID
            reference_id = f"PROS-{uuid.uuid4().hex[:8].upper()}"
            
            # Create the lead with minimal information
            lead = Lead.objects.create(
                email=email,
                first_name="",  # Can be updated later
                last_name="",   # Can be updated later
                created_by=created_by,
                status="new",
                source="api",
                reference_id=reference_id
            )
            
            return Response({
                'id': lead.id,
                'email': lead.email,
                'reference_id': reference_id,
                'status': 'success',
                'message': 'Prospect created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )