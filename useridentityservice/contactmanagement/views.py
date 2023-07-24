from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactManageSerializer
from rest_framework import status
from rest_framework.decorators import api_view

'''
Sample Payload:

{
    "email": "mcfly@hillvalley.edu",
    "phoneNumber": "123456"
}

'''

'''
Sample Response:


{
    "contact":{
        "primaryContatctId": 1,
        "emails": ["lorraine@hillvalley.edu","mcfly@hillvalley.edu"]
        "phoneNumbers": ["123456"]
        "secondaryContactIds": [23]
    }
}

'''

class ContactManagement(APIView):
    # seriliazer_class=[ContactManageSerializer]
    http_method_names=['post']

    def post(self,request,*args,**kwargs):
        try:
            payload={
                        'email':request.data.get('email'),
                        'phoneNumber':request.data.get('phoneNumber')

                    }
            serilaizer=ContactManageSerializer(data=payload)
            if not serilaizer.is_valid():
                return Response(data={'error':serilaizer.errors},status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data=serilaizer.save(),status=status.HTTP_200_OK)

        except Exception as err:
            print(err)
            return Response(data={'error':'Server Error Occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['get'])
def probe(request):
    return Response(data={'status':'Server is Reachable'},status=status.HTTP_200_OK)
        

        


        


