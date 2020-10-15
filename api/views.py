import random

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail

from api.filters import CustomFilterBackend
from api.models import UserCode, Category, Genre, Title, Review, Comment
from api.permissions import IsAdmin, IsAuthor, IsAdminOrReadOnly, \
    IsStaffOrAuthorOrReadOnly
from api.serializers import UserCodeSerializer, MyTokenObtainPairSerializer, \
    UsersSerializer, SpecificUserSerializer, CategorySerializer, \
    GenresSerializer, TitleSerializer, ReviewSerializer, CommentSerializer
from users.models import CustomUser


class UserCodeViewSet(generics.CreateAPIView):
    serializer_class = UserCodeSerializer
    queryset = UserCode.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            email = self.request.data['email']
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            self.send_code(email, code)
            serializer.save(email=email, confirmation_code=code)

    @staticmethod
    def send_code(email, code):
        send_mail(
            'Код доступа для регистрации на ресурсе YAMDB',
            f'{code}',
            'yamdb@google.com',
            [f'{email}'],
            fail_silently=False,
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        if not email:
            return Response("Email is required field.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not confirmation_code:
            return Response("Confirmation code is required field.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not UserCode.objects.filter(email=email,
                                       confirmation_code=confirmation_code):
            return Response("Confirmation code for your email isn't valid.",
                            status=status.HTTP_400_BAD_REQUEST)

        if not CustomUser.objects.filter(email=email):
            CustomUser.objects.create(email=email)
        if serializer.is_valid(raise_exception=True):
            UserCode.objects.get(email=email).delete()
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)


class UsersViewSet(generics.ListCreateAPIView):
    serializer_class = UsersSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]


class SpecificUserViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SpecificUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.queryset.get(username=self.kwargs["username"])


class MeUserViewSet(generics.RetrieveUpdateAPIView):
    serializer_class = SpecificUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        if 'role' in request.data and not (
                request.user.role == 'admin' or request.user.is_superuser):
            return Response("You can't change your role.",
                            status=status.HTTP_400_BAD_REQUEST)
        return self.partial_update(request, *args, **kwargs)


class CategoriesViewSet(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class CategoryViewSet(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdmin]

    def get_object(self):
        return self.queryset.get(slug=self.kwargs["slug"])

    def delete(self, request, *args, **kwargs):
        if not Category.objects.filter(slug=self.kwargs["slug"]):
            return Response("Genre with this slug doesn't exist.",
                            status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(request, *args, **kwargs)


class GenresViewSet(generics.ListCreateAPIView):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class GenreViewSet(generics.DestroyAPIView):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdmin]

    def get_object(self):
        return self.queryset.get(slug=self.kwargs["slug"])

    def delete(self, request, *args, **kwargs):
        if not Genre.objects.filter(slug=self.kwargs["slug"]):
            return Response("Genre with this slug doesn't exist.",
                            status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [CustomFilterBackend]
    filterset_fields = ['year', 'category', 'genre', 'name']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def perform_create(self, serializer):
        if serializer.is_valid:
            serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title

    def get_queryset(self):
        queryset = Review.objects.filter(title=self.get_title()).all()
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrAuthorOrReadOnly]

    def perform_create(self, serializer):
        if serializer.is_valid:
            serializer.save(author=self.request.user, review=self.get_review())

    def get_review(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review

    def get_queryset(self):
        queryset = Comment.objects.filter(review=self.get_review()).all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
