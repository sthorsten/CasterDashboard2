from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import FieldError


def parse_request(model, query_data):
    if query_data == [None, None]:
        return {
            "status": "Not Found",
            "code": 404
        }

    if not query_data[0]:
        return {
            "status": "Internal Server Error",
            "code": 500
        }

    return {
        "status": "OK",
        "code": 200,
        "model": model,
        "partition": query_data[1],
        "data": query_data[0]
    }


def send_server_data(group, model, serialized_data):
    channel = get_channel_layer()
    async_to_sync(channel.group_send)(
        group,
        {
            'type': 'server.data',
            'data': parse_request(model, [serialized_data, "single"])
        }
    )


def make_query(model, query, serializer):
    try:
        if not query or len(query) == 0:
            result = model.objects.all()
            return [serializer(result, many=True).data, "full"]

        result = model.objects.filter(**query)
        if result:
            if len(result) == 1:
                return [serializer(result.first()).data, "single"]

            return [serializer(result, many=True).data, "partial"]

    except model.DoesNotExist:
        pass
    except FieldError:
        pass
    except ValueError:
        pass

    return [None, None]
