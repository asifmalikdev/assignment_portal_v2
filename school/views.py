from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DistrictSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import District
from rest_framework.pagination import PageNumberPagination


class DistrictListCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
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
    permission_classes = [IsAuthenticated]

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
