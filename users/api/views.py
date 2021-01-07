from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from users.models import Plans
from users.api.serializers import PlanSerializer


@api_view(['GET', ])
def api_detail_plan_view(request, pk):

    try:
        plan = Plans.objects.get(pk=pk)

    except Plans.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PlanSerializer(plan)
    return Response(serializer.data)


@api_view(['PUT', ])
def api_update_plan_view(request, pk):

    try:
        plan = Plans.objects.get(pk=pk)

    except Plans.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PlanSerializer(plan, data=request.data)
    data = {}

    if serializer.is_valid():
        serializer.save()
        data['success'] = 'update successful'
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def api_update_plan_view(request, pk):

    try:
        plan = Plans.objects.get(pk=pk)

    except Plans.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = plan.delete()
        data = {}

       # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
