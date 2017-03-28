from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from polls.models import Restaurant
from .serializers import (
    PollsSerializers,
    PollsDetailSerializers,
    PollsCreateSerializers
)

class PollsListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = PollsSerializers

class PollsCreateAPIView(CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = PollsCreateSerializers
    permission_classes = [
        IsAuthenticated,                            # way to limit permission of user
    ]
    def perform_create(self, serializer):           # add info, who (user) are doing this stuff
        serializer.save(user=self.request.user)

class PollsDetailAPIView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = PollsDetailSerializers
    lookup_field = "pk"
    #lookup_url_kwarg = "abc"
#def get_queryset():