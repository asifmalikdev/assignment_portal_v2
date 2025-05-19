from django.contrib.admin.templatetags.admin_list import pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DistrictSerializer, SchoolSerializer, ClassRoomSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import District, School, ClassRoom
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsAdminUser,IsStudentUser,IsTeacherUser

class DistrictListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        districts = District.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(districts, request)


        serializer = DistrictSerializer(result_page, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DistrictSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "District added"}, status=201)
        return Response(serializer.errors, status=400)

class DistrictDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_object(self, name):
        try:
            return District.objects.get(name__iexact=name)
        except District.DoesNotExist:
            return None

    def get(self, request, name, format=None):
        district = self.get_object(name)
        if not district:
            return Response({"msg": "District not found"}, status=404)
        serializer = DistrictSerializer(district)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        district = self.get_object(name)
        if not district:
            return Response({"msg": "District not found"}, status=404)
        serializer = DistrictSerializer(district, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "District updated"}, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, name, format=None):
        district = self.get_object(name)
        if not district:
            return Response({"msg": "District not found"}, status=404)
        name_val = district.name
        district.delete()
        return Response({"msg": f"{name_val} is deleted"})

class SchoolListCreateViwe(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        schools= School.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size=3
        result_page=paginator.paginate_queryset(schools, request)

        serializer = SchoolSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        schol = request.data
        print(schol)
        serializer = SchoolSerializer(data = schol)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"School Saved"})
        return Response(serializer.errors)

class SchoolDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get_object(self, name):
        try:
            return School.objects.get(name__iexact=name)
        except School.DoesNotExist:
            return None
    def get(self, request, name):

        schol=self.get_object(name)
        if not schol:
            return Response({"msg":"school not exist"}, status=404)
        serializer = SchoolSerializer(schol)
        return Response(serializer.data)
    def put(self,request, name):
        schol=self.get_object(name)
        if not schol:
            return Response({"msg":"school not found"})
        serializer = SchoolSerializer(schol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":f"{schol.name} is updated to "}, status=201)
        return Response(serializer.error)
    def delete(self,request, name):
        schol=self.get_object(name)
        if schol:
            name_val=schol.name
            schol.delete()
            return Response({"msg":f"{name_val} is deleted"})
        return Response({"msg":"School did not found"}, status=404)

from .permissions import AllowPostForAnon
class ClassRoomListCreateView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [ AllowAny]

    def get(self, request):
        classes = ClassRoom.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(classes, request)

        serializer = ClassRoomSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        print("request data : ",request.data)
        serializer = ClassRoomSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            print("serilizer data ;", serializer.data)
            return Response({"msg":"Data save"}, status=201)
        return Response(serializer.errors)
