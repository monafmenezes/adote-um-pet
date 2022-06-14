from os import stat
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from adocao.email_service import enviar_email_confirmacao
from .serializers import AdocaoSerializer
from .models import Adocao


class AdocaoList(APIView):
    def get(self, request, format=None):
        adocoes = Adocao.objects.all()
        serializer = AdocaoSerializer(adocoes, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, format=None):
        serializer = AdocaoSerializer(data=request.data)

        if serializer.is_valid():
            adocao = serializer.save()
            enviar_email_confirmacao(adocao)
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(
            {
                "errors": serializer.errors,
                "message": "Houveram erros de validação",
            },
            status=HTTP_400_BAD_REQUEST,
        )
