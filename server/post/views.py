from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Like, Save
from .serializers import (
    PostCreateSerializer, 
    CommentCreateSerializer, 
    LikedPostsSerializer, 
    PostSimpleSerializer, 
    SavedPostsSerializer,
    CommentsOnPostSerializer
)
from rest_framework.decorators import action
from account.pagination import CustomPagination
from .permissions import IsPostOwner

class PostViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        # return PostListSerializer

    def get_permissions(self):
        if self.action in ['update', 'archive', 'unarchive']:
            self.permission_classes = [IsPostOwner]
        return super().get_permissions()


    def create(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(posted_by=request.user)
            return Response(PostSimpleSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        if not Like.objects.filter(post=post, liked_by=request.user, active=True).exists():
            like, created = Like.objects.get_or_create(post=post, liked_by=request.user)
            if not like.active:
                like.active = True
                like.save()
            post.likes += 1
            post.save()
            return Response({'message': 'Post liked successfully', 'likes': post.likes}, status=status.HTTP_200_OK)
        return Response({'message': 'Post already liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        if Like.objects.filter(post=post, liked_by=request.user, active=True).exists():
            Like.objects.filter(post=post, liked_by=request.user).update(active=False)
            post.likes -= 1
            post.save()
            return Response({'message': 'Post unliked successfully', 'likes': post.likes}, status=status.HTTP_200_OK)
        return Response({'message': 'Post not liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, commented_by=request.user)
            post.comments += 1
            post.save()
            return Response({'message': 'Comment added successfully', 'comments': post.comments}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["post"])
    def save(self, request, pk=None):
        post = self.get_object()
        if not Save.objects.filter(post=post, saved_by=request.user, active=True).exists():
            save_obj, created = Save.objects.get_or_create(post=post, saved_by=request.user)
            if not save_obj.active:
                save_obj.active = True
                save_obj.save()
            post.saves += 1
            post.save()
            return Response({'message': 'Post saved successfully', 'saves': post.saves}, status=status.HTTP_200_OK)
        return Response({'message': 'Post already saved'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["post"])
    def unsave(self, request, pk=None):
        post = self.get_object()
        if Save.objects.filter(post=post, saved_by=request.user, active=True).exists():
            Save.objects.filter(post=post, saved_by=request.user).update(active=False)
            post.saves -= 1
            post.save()
            return Response({'message': 'Post unsaved successfully', 'saves': post.saves}, status=status.HTTP_200_OK)
        return Response({'message': 'Post not saved'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def liked_posts(self, request):
        likes = Like.objects.filter(liked_by=request.user, active=True).prefetch_related("post", "post__payment_info_list")
        paginated_likes = self.paginate_queryset(likes)
        if paginated_likes is not None:
            serializer = LikedPostsSerializer(paginated_likes, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(LikedPostsSerializer(likes, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def saved_posts(self, request):
        saves = Save.objects.filter(saved_by=request.user, active=True).prefetch_related("post", "post__payment_info_list")
        paginated_saves = self.paginate_queryset(saves)
        if paginated_saves is not None:
            serializer = SavedPostsSerializer(paginated_saves, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(SavedPostsSerializer(saves, many=True).data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=["get"])
    def my_posts(self, request):
        posts = Post.objects.filter(posted_by=request.user, archived=False).prefetch_related("payment_info_list")
        paginated_posts = self.paginate_queryset(posts)
        if paginated_posts is not None:
            serializer = PostSimpleSerializer(paginated_posts, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(PostSimpleSerializer(posts, many=True).data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=["get"])
    def my_archived_posts(self, request):
        posts = Post.objects.filter(posted_by=request.user, archived=True).prefetch_related("payment_info_list")
        paginated_posts = self.paginate_queryset(posts)
        if paginated_posts is not None:
            serializer = PostSimpleSerializer(paginated_posts, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(PostSimpleSerializer(posts, many=True).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        post = self.get_object()
        if post.archived:
            return Response({'message': 'Post already archived'}, status=status.HTTP_400_BAD_REQUEST)
        post.archived = True
        post.save()
        return Response({'message': 'Post archived successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def unarchive(self, request, pk=None):
        post = self.get_object()
        if not post.archived:
            return Response({'message': 'Post not archived'}, status=status.HTTP_400_BAD_REQUEST)
        post.archived = False
        post.save()
        return Response({'message': 'Post unarchived successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments_list.filter(archived=False).prefetch_related("commented_by")
        paginated_comments = self.paginate_queryset(comments)
        if paginated_comments is not None:
            serializer = CommentsOnPostSerializer(paginated_comments, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(CommentsOnPostSerializer(comments, many=True).data, status=status.HTTP_200_OK)
