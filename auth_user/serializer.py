from rest_framework import serializers

from .models import User

fields = ('first_name', 'last_name',
          'username', 'bio', 'email', 'role')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = fields


class UserMeSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = fields

    def get_fields(self):
        fields = super(UserMeSerializers, self).get_fields()
        if self.instance and getattr(self.instance, 'role') == 'user':
            fields['role'].read_only = True
        return fields
