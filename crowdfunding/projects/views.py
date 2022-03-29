from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import Project, Pledge, Category, Comment
from .permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, 
    ProjectSerializer,
    PledgeSerializer, 
    ProjectDetailSerializer, 
    CategorySerializer,
    )

class PledgeList(APIView):
    
    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        is_open = request.query_params.get('is_open', None)
        if is_open:
            projects = projects.filter(is_open=is_open)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
class CommentListApi(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comment.objects.filter( visible=True)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailApi(generics.RetrieveUpdateDestroyAPIView):
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comment.objects.filter( visible=True)
    serializer_class = CommentSerializer

    
class ProjectCommentListApi(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Comment.objects.filter( visible=True)
    serializer_class = CommentSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user,project_id=self.kwargs.get('pk'))

    def get_queryset(self):
        return Comment.objects.filter(project_id=self.kwargs.get('pk'))