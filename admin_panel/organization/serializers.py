from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import *
from rest_framework import serializers



class OrganizationSerializer(DocumentSerializer):
    class Meta:
        model = Organizations
        fields = '__all__'



class PersonSerializer(DocumentSerializer):
    class Meta:
        model = Person
        fields = '__all__'



# class CombinedSerializer(serializers.Serializer):
#     organization_data = OrganizationSerializer()
#     person_data = PersonSerializer()

#     def create(self, validated_data):
#         organization_data = validated_data.pop('organization_data')
#         person_data = validated_data.pop('person_data')

#         organization_instance = Organizations.objects.create(**organization_data)
#         person_instance = Person.objects.create(**person_data)

#         return {'organization': organization_instance, 'person': person_instance}
        
class CombinedSerializer(serializers.Serializer):
    organization_data = OrganizationSerializer()
    person_data = PersonSerializer()

    def create(self, validated_data):
        organization_data = validated_data.pop('organization_data')
        person_data = validated_data.pop('person_data')

        organization_instance = Organizations.objects.create(**organization_data)
        person_instance = Person.objects.create(**person_data)

        # Save IDs of each other
        organization_instance.person_id = person_instance.id
        # organization_instance.user_ids.add(person_instance.id)
        person_instance.organization_id = organization_instance.id
        organization_instance.save()
        person_instance.save()
    

        return {'organization': organization_instance, 'person': person_instance}