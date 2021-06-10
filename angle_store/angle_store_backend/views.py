from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from angle_store_backend.models import Product
from angle_store_backend.serializers import ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        # Turn on many, since we explicitly want to create lists of objects
        kwargs["many"] = True

        data = kwargs.get("data")
        if "posts" not in data:
            raise APIException("Request body needs to contain 'post' key.")

        kwargs["data"] = data["posts"]
        return super().get_serializer(*args, **kwargs)


class ProductSearchListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def cast_int_or_fail(self, num_str: str, label: str):
        try:
            number = int(num_str)
            if number < 0:
                raise APIException(f"{label} should not be negative. Provided value: {num_str}")
            return number
        except ValueError:
            raise APIException(f"{label} must be valid integer if provided. {label}: {num_str}")

    def get_queryset(self):
        """
        Provides ability to search for products based on following params:
            - keyword (str, required)
            - min_price (number, optional)
            - max_price (number, optional)
        """
        # Validate params
        query_params = self.request.query_params
        keyword = query_params.get('keyword')
        if keyword is None or len(keyword) == 0:
            raise APIException("keyword must be provided.")

        filters = {
            "name__contains": keyword,
        }

        min_price = query_params.get('min_price')
        max_price = query_params.get('max_price')
        if min_price is not None:
            min_price = self.cast_int_or_fail(min_price, "min_price")
            filters["price__gte"] = min_price

        if max_price is not None:
            max_price = self.cast_int_or_fail(max_price, "max_price")
            filters["price__lte"] = max_price

        if min_price is not None and max_price is not None and min_price > max_price:
            raise APIException(f"min_price should not exceed max_price: min_price: {min_price}, max_price: {max_price}")

        return Product.objects.filter(**filters)

    # Override list method to wrap response with "post" key
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "posts": serializer.data
        }
        return Response(response_data)
