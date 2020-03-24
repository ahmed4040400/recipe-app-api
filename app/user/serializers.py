"""To authenticate a given username and password,
use authenticate().It takes two keyword arguments,
username and password,
and it returns a User object if the password is valid
for the given username.If the password is invalid,
authenticate() returns None."""
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


# Serializer for the user object
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')
        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 5,
                         'style': {'input_type': 'password'}
                         }
        }

    # a callback when the serializer to create the object
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    # a callback when the serializer to update the object
    def update(self, instance, validated_data):
        """:param instance : contains the old user object
           :param validated_data contains the new passed data to update
        """


        """
            pop() is  like get() but after getting the object 
            it'll remove it from the original dictionary 
            
            and it requires a default value in case it couldn't 
            get the desired value 
            so we can know if we're gonna update the pass or not 
        """
        password = validated_data.pop('password', None)
        # updating every thing in the user except password
        # using the super.update method
        user = super().update(instance, validated_data)

        # if there is a password in the validated_data we update it
        # using set password method
        if password:
            user.set_password(password)
            # saving the user
            user.save()
        # return the updated user
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # passing the request from the context to authenticate
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = "unable to authenticate with the provided credentials"
            raise serializers.ValidationError(

            )
        # adding the user to the validated data and return it all
        attrs['user'] = user
        return attrs
