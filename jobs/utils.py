import requests
import cloudinary.uploader
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.utils import timezone
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauthlib.common import generate_token
from datetime import timedelta


def upload_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        upload_response = cloudinary.uploader.upload(image_data, use_filename=True, unique_filename=False)
        return upload_response['secure_url']
    return None


def create_user_token(user):
    application = get_object_or_404(Application, name="jobapp")
    expires = timezone.now() + timedelta(seconds=36000)
    access_token = AccessToken.objects.create(
        user=user,
        scope='read write',
        expires=expires,
        token=generate_token(),
        application=application
    )
    print("Access Token:", access_token.token)  # Ghi log token để kiểm tra
    refresh_token = RefreshToken.objects.create(
        user=user,
        token=generate_token(),
        application=application,
        access_token=access_token
    )

    return access_token, refresh_token