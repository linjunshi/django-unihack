import json

from django.http import HttpResponse
from django.utils import timezone
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushServerError
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from api.models import ParkingTransaction, TransactionSerializer
import api.config as conf


@api_view(['GET'])
def get_carpark (request, id):
    carpark = ParkingTransaction.objects.get(id=id)
    return HttpResponse( obj_to_json(carpark) )


@api_view(['GET'])
def get_all_records(request):
    all = ParkingTransaction.objects.all()
    return HttpResponse( objs_to_json(all) )


@api_view(['GET'])
def get_car(request, id):
    order = ParkingTransaction.objects.get(id=id)
    if order is not None:
        return HttpResponse( obj_to_json(order) )
    else:
        return HttpResponse( msg_to_json('no such id') )


@api_view(['POST'])
def car_start_parking(request):
    obj = None
    try:
        obj = json.loads( request.body.decode('utf-8') )
    except:
        pass
    
    if obj is not None:
        trans = ParkingTransaction( parkingLotID=obj['parkingLotNum'], carnum=obj['carNum'] )
        send_push_message( conf.TOKEN, msg_with_data( '{"orderID":"%s"}'%(str(trans.id)) ) )
        trans.save()
        return HttpResponse( obj_to_json(trans) )
    else:
        return HttpResponse( msg_to_json('no car parking!') )


@api_view(['POST'])
def car_leave (request):
    obj = None
    try:
        obj = json.loads(request.body.decode('utf-8'))
    except:
        pass

    if obj is not None:
        record = ParkingTransaction.objects.filter(parkingLotID=obj['parkingLotNum']).order_by('timeStartParking').reverse()[0]
        record.timeEndParking = timezone.now()
        record.save()
        return HttpResponse(msg_to_json('update successfully'))
    else:
        return HttpResponse(msg_to_json('no such parkinglot id!'))


@api_view(['POST'])
def pay_order(request):
    obj = None
    try:
        obj = json.loads(request.body.decode('utf-8'))
    except:
        pass
    
    if obj is not None:
        order = ParkingTransaction.objects.get(id=obj['orderNum'])
        if order is not None:
            order.parkingLength, order.paid = obj['parkingLength'], 1
            order.save()
            return HttpResponse( msg_to_json('oder paid') )
        else:
            return HttpResponse( msg_to_json('no such order id') )
    else:
        return HttpResponse( msg_to_json('bad json format') )


# helper functions

def objs_to_json (objs):
    serializer = TransactionSerializer(objs, many=True)
    decodedStr = JSONRenderer().render(serializer.data).decode()
    return msg_with_data( decodedStr )


def obj_to_json (obj):
    serializer = TransactionSerializer(obj)
    decodedStr = JSONRenderer().render(serializer.data).decode()
    return msg_with_data( decodedStr )
 
    
def msg_to_json (message):
    return '{"message":"%s"}' % (message)


def msg_with_data (jsonObj):
    return '{"message":"success", "data":%s}' % (jsonObj)


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):
    try:
        PushClient().publish( PushMessage(to=token, body=message, data=extra) )
    except PushServerError as exc:
        print(exc)
        pass