from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'country', 'photo_400_orig')),
                                                access_token=response['access_token'],
                                                v='5.131')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        user.userprofile.gender = UserProfile.MALE if data['sex'] == 2 else UserProfile.FEMALE

    if data['about']:
        user.userprofile.about_me = data['about']

    if data['country']:
        user.lange = data['country']['title']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        user.age = age
        # одновременно с - DEBUG = False
        # if age < 100:
        #     user.delete()
        #     raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['photo_400_orig']:
        photo_response = requests.get(data['photo_400_orig'])
        photo_path = f'user_image/vk_user{user.pk}.jpg'
        with open(f'media/{photo_path}', 'wb') as vk_photo:
            vk_photo.write(photo_response.content)
        user.image = photo_path

    user.save()