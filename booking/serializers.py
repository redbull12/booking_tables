from rest_framework import serializers

from booking.models import Table, Booking
from booking.utils import send_confirmation_mail


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class TablesListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='table-detail', lookup_field='slug')

    class Meta:
        model = Table
        fields = ['title', 'slug', 'details']

class BookingSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)
        booking.create_activation_code()
        send_confirmation_mail(booking.user, booking.activation_code)
        return booking
