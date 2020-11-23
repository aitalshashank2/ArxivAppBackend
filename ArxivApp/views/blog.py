from rest_framework import viewsets

from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from ArxivApp.models import Blog
from ArxivApp.serializers import BlogGetSerializer, BlogPostSerializer


class BlogViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial":
            return BlogPostSerializer
        else:
            return BlogGetSerializer
    queryset = Blog.objects.all().order_by('-votes')

    # Implement search based on the initial characters of the blog titles and author's full name
    filter_backends = [filters.SearchFilter]
    search_fields = ['$title', '$author__full_name', '$body']


    @action(detail=True, methods=['get', ])
    def vote(self, request, pk=None):
        """
        Update the vote count for a blog
        """
        if pk == None:
            return Response({'Error': 'Blog id not provided'}, status=status.HTTP_400_BAD_REQUEST)

        vote = request.query_params.get('vote', None)
        blog = Blog.objects.get(pk=pk)

        if vote == "up":
            blog.votes = blog.votes + 1
            blog.save()
            return Response({'Status': f'Upvoted {blog.title}'}, status=status.HTTP_200_OK)
        elif vote == "down":
            blog.votes = blog.votes - 1
            blog.save()
            return Response({'Status': f'Downvoted {blog.title}'}, status=status.HTTP_200_OK)

        return Response({'status': 'Invalid query parameter'}, status=status.HTTP_400_BAD_REQUEST)
