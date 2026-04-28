import factory
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from users.models import Profile, UserToken

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True

    profile = factory.RelatedFactory(
        'apps.users.factories.ProfileFactory',
        factory_related_name='user',
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = model_class._default_manager
        return manager.create_user(*args, **kwargs)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
    bio = factory.Faker('paragraph')
    verified = factory.Faker('boolean')
    color_bg = factory.Faker('hex_color')
    role = Profile.Role.USER
    avatar = factory.django.ImageField(color='green')


class UserTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserToken

    user = factory.SubFactory(UserFactory)
    type = factory.Iterator([
        UserToken.TokenType.VERIFY_EMAIL,
        UserToken.TokenType.CHANGE_PASSWORD,
        UserToken.TokenType.ACTIVATE_ACCOUNT
    ])
    
    expires_at = factory.LazyFunction(lambda: timezone.now() + timedelta(days=1))
