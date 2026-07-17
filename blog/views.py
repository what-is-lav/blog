from rest_framework import viewsets, generics, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(is_published=True) | Post.objects.filter(author=self.request.user)
        return Post.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.author != request.user:
                raise PermissionDenied("Вы можете изменять или удалять только свои посты.")


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(id=self.kwargs.get('post_id'))
        except Post.DoesNotExist:
            raise NotFound("Пост не найден.")
        
        serializer.save(author=self.request.user, post=post)