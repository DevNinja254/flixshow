from rest_framework import viewsets, filters, permissions, generics
from rest_framework.filters import SearchFilter
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .serializers import *
from django.utils.crypto import get_random_string
from multimedia.models import *
from multimedia.serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from Members.serializers import *
import logging, base64, json, requests, jwt
from rest_framework.response import Response
from .pagination import CustomPagination
from .filter import *
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
class VideoDetailsAPIView(viewsets.ModelViewSet):
    serializer_class = VideoUploadSerializer
    queryset = VideoUpload.objects.all()
    filter_backends = [filters.OrderingFilter, SearchFilter]
    filtersets_class = VideoUploadFilter
    http_method_names = ["get", "head", "option"]
    search_fields = ["title", "popular", "typs"]
    ordering = "date_uploaded"
    pagination_class = CustomPagination
class SearchAPIView(viewsets.ModelViewSet):
    serializer_class = VideoUploadSerializer
    queryset = VideoUpload.objects.all()
    filterset_class = SearchUploadFilter
    http_method_names = ["get", "head", "option"]
    ordering = "date_uploaded"
    pagination_class = None
class CartegoryAPIView(viewsets.ModelViewSet):
    serializer_class = CartegoriesSerializer
    queryset = Cartegories.objects.all()
class MessageAPIView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
class VideoAPIView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = videosSerializer
    queryset = videos.objects.all()
    http_method_names = ["get", "head", "option"]
    filterset_class = VideoFilter
class PurchasedAPIView(viewsets.ModelViewSet):
    serializer_class = PurchasedSerializer
    queryset = Purchased.objects.all()
    filterset_class = PurchaseFilter
    # renderer_classes = [JSONRenderer]
    # permission_classes = [IsAuthenticated]
class DownloadHistoryAPIView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = DownloadHistorySerializer
    # http_method_names = ["get", "head", "option"]
    queryset = DownloadHistory.objects.all()
    filterset_class = DownloadsFilter
    # renderer_classes = [JSONRenderer]
class DepositHistoryAPIView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = DepositHistorySerializer
    # http_method_names = ["get", "head", "option"]
    queryset = DepositHistory.objects.all()
    filterset_class = DepositFilter
    # renderer_classes = [JSONRenderer]
class OnwatchAPIView(viewsets.ModelViewSet):
    serializer_class = OnwatchSerializer
    queryset = Onwatch.objects.all()
    http_method_names = ["get", "head", "option"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WatchFilter
    # renderer_classes = [JSONRenderer] # Only return json.
    # permission_classes = [IsAuthenticated]

class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    # permission_classes = [IsAuthenticated]
class LikeAPIView(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    # permission_classes = [IsAuthenticated]
class CartAPIView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    filterset_class = CartFilter
    # permission_classes = [IsAuthenticated]
class ProfileAPIView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    # permission_classes = [IsAuthenticated]
class UserRegistrationAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {
            "refresh": str(token),
            'access': str(token.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)
class UserLoginAPIView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data

        serializer = MembersSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {
            "refresh": str(token),
            'access': str(token.access_token)
        }
        return Response(data, status=status.HTTP_200_OK)
logger = logging.getLogger(__name__)
class UserLogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logger.debug(request.data)
        try: 
            refresh_token = request.data
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Logout Error: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserInfoAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MembersSerializer
    def get_object(self):
        return self.request.user
class MembersAPIView(viewsets.ModelViewSet):
    serializer_class = MembersSerializer
    queryset = Members.objects.all()
class NotificationAPIView(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

@api_view(['POST'])
def deposit(request):
        if request.method == "POST":
            username = request.data["username"]
            Amount = int(request.data["amount"])
            number = str(request.data["phone_number"])
            phoneNumber = "254" + number[1:]
            # Your API username and password
            api_username = "7v1lCadGn6V2AstOB8LD"
            api_password = "CHKjuI9dQdRWgMXAof7ip4rMIkopntZrT3G0zgRc"
            # Concatenating username and password with colon
            credentials = f'{api_username}:{api_password}'
            # Base64 encode the credentials
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            # Creating the Basic Auth token
            basic_auth_token = f'Basic {encoded_credentials}'
            # Output the token
            # print(basic_auth_token)
            url = 'https://backend.payhero.co.ke/api/v2/payments'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': basic_auth_token
            }
            logger.info("sending data")
            data = {
                "amount": Amount,
                "phone_number": phoneNumber,
                "channel_id": 1786,
                "provider": "m-pesa",
                "external_reference": "INV-009",
                "callback_url":"https://smooth-vast-thrush.ngrok-free.app/stk/"
            }
            response = requests.post(url, json=data, headers=headers).json()
            if response["success"]:
                payments = Payment.objects.filter(phone_number = phoneNumber)
                if payments.exists():
                    for paiz in payments:
                        paiz.delete()
                Payment.objects.get_or_create(
                    username = username,
                    phone_number = phoneNumber
                )
            # print(response)
            return Response(response, status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = Members.objects.get(email=serializer.validated_data['email'])
            # Create JWT token
            token = AccessToken.for_user(user)
            plain_text =" password_reset_email.txt"
            html_content = render_to_string('password_reset_email.html', {"token":token})
            # Send email
            subject = 'Password Reset Request'
            send_mail(
                subject,
                message=plain_text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=False,
            )
            return Response({"message": "Reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
