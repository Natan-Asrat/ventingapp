from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from .recommendation import get_top_post_ids, updated_post_view_count
from .models import Post, Like, PostView, Save, Comment, LikeComment, PaymentInfo
from .serializers import (
    PostCreateSerializer, 
    CommentCreateSerializer, 
    LikedPostsSerializer, 
    PostSimpleSerializer,
    RepliesSerializer, 
    SavedPostsSerializer,
    CommentsOnPostSerializer,
    PaymentInfoSerializer,
    MyPaymentInfoSerializer,
    MyPostSimpleSerializer
)
from rest_framework.decorators import action
from account.pagination import CustomPagination
from .permissions import IsPostOwner
from django.db.models import F, Case, Count, Exists, OuterRef, Subquery, Value, When
from .query import get_posts_queryset
from django.db.models.functions import Coalesce
from django.conf import settings
from rest_framework.filters import SearchFilter
from django.utils import timezone

class PostViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.filter(archived=False, banned=False).prefetch_related("payment_info_list").select_related("posted_by")
    serializer_class = PostSimpleSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['description']

    @action(detail=False, methods=["get"])
    def recommended_posts(self, request):
        """
        Returns posts ranked by user interests:
        - Top 5 interests weighted by count
        - Random 5 interests outside top 5
        - Excludes posts created by the user
        - Not paginated
        """
        user = request.user
        post_ids = get_top_post_ids(user)

        # Preserve the order of post_ids in the queryset
        posts_qs = self.queryset.filter(id__in=post_ids).order_by(
            Case(*[When(id=pid, then=pos) for pos, pid in enumerate(post_ids)])
        )
        qs = get_posts_queryset(posts_qs, request.user)

        serializer = PostSimpleSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return get_posts_queryset(self.queryset, self.request.user)
        elif self.action in ['unarchive', 'comments']:
            return Post.objects.all()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSimpleSerializer

    def get_permissions(self):
        if self.action in ['update', 'archive', 'unarchive', 'add_payment_info', 'bulk_add_payment_info']:
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
            post.likes = Like.objects.filter(post=post, active=True).count()
            post.save()
            post.posted_by.post_likes = Like.objects.filter(post__posted_by=post.posted_by, active=True).count()
            post.posted_by.save()
            return Response({'message': 'Post liked successfully', 'likes': post.likes}, status=status.HTTP_200_OK)
        return Response({'message': 'Post already liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        if Like.objects.filter(post=post, liked_by=request.user, active=True).exists():
            Like.objects.filter(post=post, liked_by=request.user).update(active=False)
            post.likes = Like.objects.filter(post=post, active=True).count()
            post.save()
            post.posted_by.post_likes = Like.objects.filter(post__posted_by=post.posted_by, active=True).count()
            post.posted_by.save()
            return Response({'message': 'Post unliked successfully', 'likes': post.likes}, status=status.HTTP_200_OK)
        return Response({'message': 'Post not liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_comment = serializer.save(post=post, commented_by=request.user)
            post.comments += 1
            post.save()
            return Response({"post_comments": post.comments, "comment": CommentsOnPostSerializer(new_comment).data}, status=status.HTTP_200_OK)
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
        likes = Like.objects.filter(liked_by=request.user, active=True).prefetch_related("post", "post__payment_info_list", "post__posted_by")
        paginated_likes = self.paginate_queryset(likes)
        if paginated_likes is not None:
            serializer = LikedPostsSerializer(paginated_likes, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(LikedPostsSerializer(likes, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def saved_posts(self, request):
        saves = Save.objects.filter(saved_by=request.user, active=True).prefetch_related("post", "post__payment_info_list", "post__posted_by")
        paginated_saves = self.paginate_queryset(saves)
        if paginated_saves is not None:
            serializer = SavedPostsSerializer(paginated_saves, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(SavedPostsSerializer(saves, many=True).data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=["get"])
    def my_posts(self, request):
        posts = Post.objects.filter(posted_by=request.user, archived=False).prefetch_related("payment_info_list").select_related("posted_by")
        paginated_posts = self.paginate_queryset(posts)
        if paginated_posts is not None:
            serializer = MyPostSimpleSerializer(paginated_posts, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(MyPostSimpleSerializer(posts, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def other_user_posts(self, request):
        user = request.query_params.get("user")
        filtered_posts = Post.objects.filter(posted_by_id=user, archived=False).prefetch_related("payment_info_list").select_related("posted_by")
        posts = get_posts_queryset(filtered_posts, request.user)
        paginated_posts = self.paginate_queryset(posts)
        if paginated_posts is not None:
            serializer = MyPostSimpleSerializer(paginated_posts, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(MyPostSimpleSerializer(posts, many=True).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"])
    def my_archived_posts(self, request):
        posts = Post.objects.filter(posted_by=request.user, archived=True).prefetch_related("payment_info_list").select_related("posted_by")
        paginated_posts = self.paginate_queryset(posts)
        if paginated_posts is not None:
            serializer = MyPostSimpleSerializer(paginated_posts, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(MyPostSimpleSerializer(posts, many=True).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        post = self.get_object()
        if post.archived:
            return Response({'message': 'Post already archived'}, status=status.HTTP_400_BAD_REQUEST)
        post.archived = True
        post.save()
        return Response(MyPostSimpleSerializer(post).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def unarchive(self, request, pk=None):
        post = self.get_object()
        if not post.archived:
            return Response({'message': 'Post not archived'}, status=status.HTTP_400_BAD_REQUEST)
        post.archived = False
        post.save()
        return Response(MyPostSimpleSerializer(post).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments_list.filter(archived=False, reply_to=None).prefetch_related("commented_by").annotate(
            liked=Exists(LikeComment.objects.filter(comment=OuterRef("pk"), liked_by=request.user, active=True))
        ).order_by('-likes', '-created_at')
        paginated_comments = self.paginate_queryset(comments)
        if paginated_comments is not None:
            serializer = CommentsOnPostSerializer(paginated_comments, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(CommentsOnPostSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def add_payment_info(self, request, pk=None):
        post = self.get_object()
        serializer = MyPaymentInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=["post"])
    def bulk_add_payment_info(self, request, pk=None):
        post = self.get_object()
        print("data", request.data)
        serializer = PaymentInfoSerializer(data=request.data, many=True)
        if serializer.is_valid():
            new_data = serializer.save(post=post)
            new_post_data = Post.objects.get(id=post.id)
            return Response({'message': 'Payment info added successfully', 'post': PostSimpleSerializer(new_post_data).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def get_bulk(self, request):
        ids = request.query_params.get("id", "")

        if not ids:
            return Response({"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
        id_list = ids.split(",")
        if not id_list:
            return Response({"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        qs = Post.objects.filter(pk__in=id_list)
        posts = get_posts_queryset(qs, user)
        existing_qs = PostView.objects.filter(user=user, post__in=posts).select_related('post', 'post__posted_by')
        existing = set(
            existing_qs.values_list("post_id", flat=True)
        )
        to_create = [
            PostView(post=post, user=user)
            for post in posts
            if post.id not in existing
        ]
        if to_create:
            PostView.objects.bulk_create(to_create)

            post_view_counts = PostView.objects.filter(
                post_id=OuterRef('id')
            ).values('post_id').annotate(
                count=Count('id')
            ).values('count')

            qs.exclude(id__in=existing).update(
                views=Coalesce(
                    Subquery(post_view_counts),
                    Value(0)
                )
            )

        PostView.objects.filter(
            user=user, post_id__in=id_list
        ).update(count=F("count") + Value(1), updated_at=timezone.now())

        for post_view in existing_qs:
            updated_post_view_count(post_view.post, user)
        
        paginated_posts = self.paginate_queryset(posts)
        if paginated_posts is not None:
            serializer = PostSimpleSerializer(paginated_posts, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(PostSimpleSerializer(posts, many=True).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def post_count(self, request):
        count = Post.objects.filter(archived=False, banned=False).count()
        show_recommended = count > settings.START_RECOMMENDATION_AT_POST_COUNT
        return Response({"count": count, "show_recommended": show_recommended}, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    pagination_class = CustomPagination
    serializer_class = RepliesSerializer

    @action(detail=True, methods=["get"])
    def replies(self, request, pk=None):
        comment = self.get_object()
        replies = comment.replies_list.filter(archived=False).prefetch_related("commented_by").annotate(
            liked=Exists(LikeComment.objects.filter(comment=OuterRef("pk"), liked_by=request.user, active=True))
        )
        paginated_replies = self.paginate_queryset(replies)
        if paginated_replies is not None:
            serializer = RepliesSerializer(paginated_replies, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(RepliesSerializer(replies, many=True).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        replying_to_comment = self.get_object() 
        post = replying_to_comment.post
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            if replying_to_comment.reply_to:
                replying_to_main = replying_to_comment.reply_to
                replying_to_main.replies += 1
                replying_to_main.save()
            else:
                replying_to_main = replying_to_comment

            new_comment = serializer.save(post=post, commented_by=request.user, reply_to=replying_to_main, reply_to_username=replying_to_comment.commented_by.username)
            replying_to_comment.replies += 1
            replying_to_comment.save()
            post.comments += 1
            post.save()
            new_comment_data = RepliesSerializer(new_comment).data
            return Response({'message': 'Comment added successfully', 'comment': new_comment_data, 'replies': replying_to_main.replies, 'post_comments': post.comments}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def like_comment(self, request, pk=None):
        comment = self.get_object()
        if not LikeComment.objects.filter(comment=comment, liked_by=request.user, active=True).exists():
            like, created = LikeComment.objects.get_or_create(comment=comment, liked_by=request.user)
            if not like.active:
                like.active = True
                like.save()
            comment.likes += 1
            comment.save()
            return Response({'message': 'Comment liked successfully', 'likes': comment.likes}, status=status.HTTP_200_OK)
        return Response({'message': 'Comment already liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unlike_comment(self, request, pk=None):
        comment = self.get_object()
        if LikeComment.objects.filter(comment=comment, liked_by=request.user, active=True).exists():
            LikeComment.objects.filter(comment=comment, liked_by=request.user).update(active=False)
            comment.likes -= 1
            comment.save()
            return Response({'message': 'Comment unliked successfully', 'likes': comment.likes}, status=status.HTTP_200_OK)
        return Response({'message': 'Comment not liked'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentInfoViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = PaymentInfo.objects.all()
    serializer_class = MyPaymentInfoSerializer