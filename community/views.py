from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from community.serializers import BoardPhotoSerializer, FreeBoardListSerializer
from community.models import FreeBoard, User

class BasicPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'

class FreeBoardListView(viewsets.ModelViewSet):
    queryset = FreeBoard.objects.all()
    serializer_class = FreeBoardListSerializer, BoardPhotoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BasicPagination

    # def post(self, request):
    #     id = request.data['id']
    #     board = get_object_or_404(FreeBoard, pk=id)
    #     if request.user.is_authenticated:
    #         user = request.user
    #         profile = User

    def get(self, request):
        qs = self.get_queryset()
        search = request.GET.get('search', '')
        search_list = qs.filter(Q(title__icontains=search))
        page = self.paginate_queryset(search_list)

        if page is not None:
            serializer = self.get_paginated_response(
                self.get_serializer(page, many=True).data)
        else:
            serializer = self.get_serializer(page, many=True)
        return Response({
            'status' : 'success',
            'data' : serializer.data
        }, status=status.HTTP_200_OK)