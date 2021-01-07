from rest_framework import serializers

from users.models import Plans


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ['name', 'date', 'c_goal', 'c_current', 'goal_reached']
