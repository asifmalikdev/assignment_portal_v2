from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DistrictSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import District


class District_List(APIView):
    print("asif 1 ===================================")
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    print("asif 2 ===================================")
    def get(self, request, pk=None, format=None):
        print("hello")
        id = pk
        if id:
            try:

                print("this is request.data  : ", request.data)
                dist = District.objects.get(pk = id)
                serilizer = DistrictSerializer(dist)
                return Response(serilizer.data)
            except District.DoesNotExist:
                return Response(serilizer.errors)
        else:
            dist = District.objects.all()
            serilizer = DistrictSerializer(dist, many=True)
            return Response(serilizer.data)
class District_Post(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request, format = None ):
        serializer = DistrictSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "District is Added"})
        return Response(serializer.errors)
class DistrictPut(APIView):
    def put(self, request, pk=None, format=None):
        id = pk
        dist = District.objects.get(pk = id)
        serializer = DistrictSerializer(dist, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "data updated via put"})
        return Response({"msg": serializer.errors})
class DistrictDelete(APIView):
    def delete(self, request, pk=None):
        id = pk
        if id:
            try:
                dist = District.objects.get(pk=id)
                dist.delete()
                return Response({"msg":f"{dist.name} is deleted"})
            except District.DoesNotExist:
                return Response({"msg":"we don't have any district with this id"})
        else:
            return Response({"msg":"can't find the student"})




