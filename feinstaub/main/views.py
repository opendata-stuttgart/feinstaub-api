from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, filters


from .serializers import UserSerializer


class UsersView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """ Get more information about users
    """
    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id',)
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            if self.request.user.groups.filter(name="show_me_everything").exists():
                return User.objects.all()
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.none()
