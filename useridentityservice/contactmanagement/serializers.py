from rest_framework import serializers
from .models import Contact
from django.db.models import Q


class ContactManageSerializer(serializers.ModelSerializer):

    class Meta:
        model=Contact
        fields='__all__'

    def contact_query_updated(self,validated_data,for_update=True):

        if for_update:

            return Contact.objects.select_for_update().filter(
                                                Q(email=validated_data['email'])
                                                |
                                                Q(phoneNumber=validated_data['phoneNumber'])
                                                ).order_by('id')
        else:
            return Contact.objects.select_related().filter(
                                                Q(email=validated_data['email'])
                                                |
                                                Q(phoneNumber=validated_data['phoneNumber'])
                                                ).order_by('id')

    def createresponse(self,validated_data):

        contact_query=self.contact_query_updated(validated_data,False)
        '''
            In the below json 
            instead of distinct why `dict.fromkeys` 
            has been used is, django backend sqllite 
            doesnot support distinct.
            Incase of other distinct is working.

        '''
        return {
                "contact":{
                            "primaryContatctId":contact_query.first().id,
                            "emails": list(dict.fromkeys(contact_query.values_list('email',flat=True))),
                            "phoneNumbers": list(dict.fromkeys(contact_query.values_list('phoneNumber',flat=True))),
                            "secondaryContactIds": list(contact_query.values_list('id',flat=True))[1:]
                        }
                }
    
    def validate(self,data):

        if any(data[field]==None or data[field]=='' for field in ['email','phoneNumber']):
            raise serializers.ValidationError('Mandatory Fields are missing!')
        return data
    
    def create(self,validated_data):
        # entry - refers to row

        contact_query=self.contact_query_updated(validated_data)
        # if no entry exist with that mail and phone number
        if not contact_query.exists():
            validated_data['linkPrecedence']='primary'
            Contact.objects.create(**validated_data)
        else:
            validated_data['linkedId']=contact_query.first()
            validated_data['linkPrecedence']='secondary'

            em_q=contact_query.filter(email=validated_data['email'])
            p_q=contact_query.filter(phoneNumber=validated_data['phoneNumber'])
            em_p_q=contact_query.filter(email=validated_data['email'],
                                        phoneNumber=validated_data['phoneNumber'])
            # if an entry exist with combination of email and phone number
            if em_p_q.exists():
                pass
            # if either an entry with email and entry with phone number exist
            elif em_q.exists() and p_q.exists():
                contact_query.exclude(id=validated_data['linkedId'].id).update(linkedId=validated_data['linkedId'],
                                                                               linkPrecedence=validated_data['linkPrecedence'])
                pass
            # if no entry exist with phone number 
            else:
                Contact.objects.create(**validated_data)
                pass
        return self.createresponse(validated_data)