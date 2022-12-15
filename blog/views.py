# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone
# from django.http import Http404
# from django.contrib.auth.decorators import login_required
# from rest_framework import viewsets
# from .serializers import CommentSerializer
# from .forms import BlogPostListSerializer
#
# from .models import Post, Comment
# from .forms import PostForm, CommentForm
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()
#
#
# class BlogPostViewSet(viewsets.ModelViewSet):
#     serializer_class = BlogPostListSerializer
#     queryset = Post.objects.all()
#
#
# def post_list(request):
#     posts = Post.objects.for_user(user=request.user)
#     return render(request, 'blog/post_list.html', {'posts': posts})
#
#
# def post_add(request):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             form = PostForm(request.POST)
#             if form.is_valid():
#                 post = form.save(commit=False)
#                 post.author = request.user
#                 post.published_date = timezone.now()
#                 post.save()
#                 return redirect('post_detail', id=post.id)
#         else:
#             form = PostForm()
#         return render(request, 'blog/post_edit.html', {'form': form})
#     return redirect('post_list')
#
#
# def post_detail(request, id):
#     post = get_object_or_404(Post, id=id)
#     if not post.is_publish() and not request.user.is_staff:
#         raise Http404("Запись в блоге не найдена")
#     return render(request, 'blog/post_detail.html', {'post': post})
#
#
#
#
#
# @login_required
# def post_edit(request, id=None):
#     post = get_object_or_404(Post, id=id) if id else None
#
#     if post and post.author != request.user:
#         return redirect('post_list')
#
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             if post.is_published:
#                 post.published_date = timezone.now()
#             else:
#                 post.published_date = None
#             post.save()
#             return redirect('post_detail', id=post.id)
#     else:
#         form = PostForm(instance=post)
#     return render(request, "blog/post_edit.html", {'form': form})
#
#
# def post_update(request, id):
#     post = get_object_or_404(Post, id=id) if id else None
#
#     if post and post.author != request.user:
#         return redirect('post_list')
#
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', id=post.id)
#     else:
#         form = PostForm(instance=post)
#     return render(request, "blog/post_edit.html", {'form': form})
#
#
# @login_required()
# def post_publish(request, id):
#     post = get_object_or_404(Post, id=id)
#     post.publish()
#     return redirect('post_detail', id=id)
#
#
# def add_comment(request, id):
#     post = get_object_or_404(Post, id=id)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect('post_detail', id=post.id)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/add_comment.html', {'form': form})
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import permissions
# from .models import Todo
# from .serializers import TodoSerializer
#
# class TodoListApiView(APIView):
#     # add permission to check if user is authenticated
#     permission_classes = [permissions.IsAuthenticated]
#
#     # 1. List all
#     def get(self, request, *args, **kwargs):
#         '''
#         List all the todo items for given requested user
#         '''
#         todos = Todo.objects.filter(user = request.user.id)
#         serializer = TodoSerializer(todos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     # 2. Create
#     def post(self, request, *args, **kwargs):
#         '''
#         Create the Todo with given todo data
#         '''
#         data = {
#             'task': request.data.get('task'),
#             'completed': request.data.get('completed'),
#             'user': request.user.id
#         }
#         serializer = TodoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer

class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Todo.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blog.models import Todo
from .serializers import TodoSerializer
from rest_framework import permissions

class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Todo.objects.get(id=todo_id, user = user_id)
        except Todo.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, todo_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, todo_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )