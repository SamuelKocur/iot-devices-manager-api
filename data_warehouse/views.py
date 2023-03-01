from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from data_warehouse.data_filtering import filter_data
from data_warehouse.serializers import FilterDataRequestSerializer, FilterDataResponseSerializer


class FilterDataListView(GenericAPIView):
    serializer_class = (FilterDataRequestSerializer, FilterDataResponseSerializer)

    def post(self, request):
        request_serializer = self.serializer_class[0](data=request.data)
        request_serializer.is_valid(raise_exception=True)

        if request_serializer.is_valid():
            data = filter_data(request_serializer.data)
            response_serializer = self.serializer_class[1](data, many=True)
            final_data = {"data": response_serializer.data}
            return Response(final_data)

        return Response(status=status.HTTP_400_BAD_REQUEST)
