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
from .custom_permision import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .filter import *
from django.views.decorators.vary import vary_on_cookie
class VideoDetailsAPIView(viewsets.ModelViewSet):
    serializer_class = VideoUploadSerializer
    queryset = VideoUpload.objects.all()
    filter_backends = [filters.OrderingFilter, SearchFilter]
    filtersets_class = VideoUploadFilter
    http_method_names = ["get", "head", "option"]
    search_fields = ["title", "popular", "typs"]
    ordering = "date_uploaded"
    pagination_class = CustomPagination
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="videosupload"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class SearchAPIView(viewsets.ModelViewSet):
    serializer_class = VideoUploadSerializer
    queryset = VideoUpload.objects.all()
    filterset_class = SearchUploadFilter
    http_method_names = ["get", "head", "option"]
    ordering = "date_uploaded"
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="search"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class CartegoryTotalAPIView(viewsets.ModelViewSet):
    serializer_class = CartegoriesTotalSerializer
    queryset = Cartegories.objects.all()
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="cartegory"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class CartegoryAPIView(viewsets.ModelViewSet):
    serializer_class = CartegoriesSerializer
    queryset = Cartegories.objects.all()
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="cartegory"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class MessageAPIView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [AuthorizedAccess]
class VideoAPIView(viewsets.ModelViewSet):
    serializer_class = videosSerializer
    queryset = videos.objects.all()
    http_method_names = ["get", "head", "option"]
    filterset_class = VideoFilter
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="videos"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class PurchasedAPIView(viewsets.ModelViewSet):
    serializer_class = PurchasedSerializer
    queryset = Purchased.objects.all()
    filterset_class = PurchaseFilter
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="purchased"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class DownloadHistoryAPIView(viewsets.ModelViewSet):
    serializer_class = DownloadHistorySerializer
    permission_classes = [AuthorizedAccess]
    queryset = DownloadHistory.objects.all()
    filterset_class = DownloadsFilter
    @method_decorator(cache_page(60 * 60, key_prefix="downloads"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class DepositHistoryAPIView(viewsets.ModelViewSet):
    permission_classes = [AuthorizedAccess]
    serializer_class = DepositHistorySerializer
    http_method_names = ["get", "head", "option"]
    queryset = DepositHistory.objects.all()
    filterset_class = DepositFilter
    @method_decorator(cache_page(60 * 60, key_prefix="deposit"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class OnwatchAPIView(viewsets.ModelViewSet):
    serializer_class = OnwatchSerializer
    queryset = Onwatch.objects.all()
    http_method_names = ["get", "head", "option"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WatchFilter
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="watch"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="review"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class LikeAPIView(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [AuthorizedAccess]
class CartAPIView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    filterset_class = CartFilter
    permission_classes = [AuthorizedAccess]
class ProfileAPIView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="profile"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class BettingRecordsAPIView(viewsets.ModelViewSet):
    serializer_class = BettingRecordsSerializer
    queryset = BettingRecords.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = 'betting_date'
    permission_classes = [AuthorizedAccess]
    @method_decorator(cache_page(60 * 60, key_prefix="betting"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class ErrorsAPIView(viewsets.ModelViewSet):
    serializer_class = ErrosSerializer
    queryset = Errors.objects.all()
    permission_classes = [AuthorizedAccess]
class UserRegistrationAPIView(GenericAPIView):
    permission_classes = [AuthorizedAccess]
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
    permission_classes = [AuthorizedAccess]
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
    permission_classes = [AuthorizedAccess]
    serializer_class = MembersSerializer
    queryset = Members.objects.all()
    @method_decorator(cache_page(60 * 60, key_prefix="members"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
class NotificationAPIView(viewsets.ModelViewSet):
    permission_classes = [AuthorizedAccess]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering = 'date_notified'
    @method_decorator(cache_page(60 * 60, key_prefix="notifications"))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    @method_decorator(cache_page(60 * 60))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
@api_view(['POST'])
def deposit(request):
        permission_classes = [AuthorizedAccess]
        if request.method == "POST":
            username = request.data["username"]
            Amount = int(request.data["amount"])
            number = str(request.data["phone_number"])
            phoneNumber = "254" + number[1:]
            # Your API username and password
            api_username = "0unBXb8nkf0BXLSUaWGz"
            api_password = "uuazzq2X33n4rFnKOh0Un5HMG8KrmU7TnJJYFxF3"
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
                "channel_id": 1238,
                "provider": "m-pesa",
                "external_reference": "INV-009",
                "callback_url":"https://kingstonemovies.org/api/v1/stk/"
            }
            response = requests.post(url, json=data, headers=headers).json()
            if response["success"]:
                payments = Payment.objects.filter(phone_number = phoneNumber)
                if payments.exists():
                    for paiz in payments:
                        paiz.delete()
                print(username)
                Payment.objects.get_or_create(
                    username = username,
                    phone_number = phoneNumber
                )
            # print(response)
            return Response(response, status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AuthorizedAccess]
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
    permission_classes = [AuthorizedAccess]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
