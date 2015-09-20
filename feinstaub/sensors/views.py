import os.path
import os
import codecs
import json
import datetime
from PIL import Image, ImageDraw, ImageFont

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .authentication import IsSensorValid, OwnerPermission, NodeUidAuthentication
from .serializers import SensorDataSerializer, NodeSerializer, SensorSerializer

from .models import (
    Node,
    Sensor,
    SensorData,
    SensorDataValue,
    SensorLocation,
    SensorType,
)


class PostSensorDataView(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """ This endpoint is to POST data from the sensor to the api.
    """
    authentication_classes = (NodeUidAuthentication,)
    permission_classes = (IsSensorValid,)
    serializer_class = SensorDataSerializer
    queryset = SensorData.objects.all()


class SensorView(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ This endpoint is to download sensor data from the api.
    """
    permission_classes = (OwnerPermission,)
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Sensor.objects.filter(node__owner=self.request.user)
        return Sensor.objects.none()


class NodeView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    """ Show all nodes belonging to authenticated user
    """
    permission_classes = (OwnerPermission,)
    serializer_class = NodeSerializer
    queryset = Node.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Node.objects.filter(owner=self.request.user)
        return Node.objects.none()


class StatisticsView(viewsets.ViewSet):

    def list(self, request):
        stats = {
            'user': {
                'count': User.objects.count(),
            },
            'sensor': {
                'count': Sensor.objects.count(),
            },
            'sensor_data': {
                'count': SensorData.objects.count(),
            },
            'sensor_data_value': {
                'count': SensorDataValue.objects.count(),
            },
            'sensor_type': {
                'count': SensorType.objects.count(),
                'list': SensorType.objects.order_by('uid').values_list('name', flat=True)
            },
            'location': {
                'count': SensorLocation.objects.count(),
            }
        }
        return Response(stats)


class CacheView(viewsets.ViewSet):

    def list(self, request):
        cache_list = [{key: cache.get(key)} for key in cache.iter_keys("location_cache_*")]

        return Response(cache_list)


class KindleView(viewsets.ViewSet):

    font_name = "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono-Bold.ttf"

    def get_font(self, size):
        return ImageFont.truetype(self.font_name, size)

    def gen_palette(self):
        for i in range(0, 256):
            for _ in range(0, 3):
                yield i

    def show_temp_humidity(self, draw):
        # read data from status_info
#        data = json.loads(read_from_statusfile())
        data = {}
        yoffset = 550
        xoffset = 270
        xoffset_small = 200
        fontsize = 16
        draw.text((xoffset, yoffset), u"%d°C" % data.get('temperature', -273),
                  0, font=self.get_font(70))
        draw.text((xoffset + xoffset_small, yoffset + 10),
                  u"sht10: %d°C" % data.get('sht10_temperature', -273),
                  0, font=self.get_font(fontsize))
        draw.text((xoffset + xoffset_small, yoffset + 40),
                  u"  dht: %d°C" % data.get('dht1_temperature', -273),
                  0, font=self.get_font(fontsize))
        draw.text((xoffset + xoffset_small, yoffset + 70),
                  u"  dht: %d°C" % data.get('dht2_temperature', -273),
                  0, font=self.get_font(fontsize))
        draw.text((xoffset, yoffset + 100), u"%d%%" % data.get('humidity', -1),
                  0, font=self.get_font(80))
        draw.text((xoffset + xoffset_small, yoffset + 110),
                  u"sht10: %d%%" % data.get('sht10_humidity', -1),
                  0, font=self.get_font(fontsize))
        draw.text((xoffset + xoffset_small, yoffset + 140),
                  u"  dht: %d%%" % data.get('dht1_humidity', -1),
                  0, font=self.get_font(fontsize))
        draw.text((xoffset + xoffset_small, yoffset + 170),
                  u"  dht: %d%%" % data.get('dht2_humidity', -1),
                  0, font=self.get_font(fontsize))

    def show_weather(self, draw):
        icons = {
            'sun': u"\u2600",
            'cloud': u"\u2601",
            'snow': u"\u2603",
            'rain': u"\u2614",
            '': '',
        }
        mapping = {
            '01': 'sun',
            '02': 'cloud',
            '03': 'cloud',
            '04': 'cloud',
            '09': 'rain',
            '10': 'rain',
            '11': 'rain',
            '13': 'snow',
        }
        draw.text((150, 0), u"Wetter: Stuttgart", 0, font=self.get_font(25))
        try:
            with codecs.open('data/weather', 'r', encoding="utf-8") as fp:
                lines = fp.readlines()
        except IOError:
            lines = []
        yoffset = 20
        pos = 10
        days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

        for line in lines:
            d = json.loads(line)
            dt = None
            if d['dt_txt']:
                dt = datetime.datetime.strptime(
                    d['dt_txt'], "%Y-%m-%d %H:%M:%S")

            if not dt and 'dt' in d:
                dt = datetime.datetime.fromtimestamp(d['dt'])
            print(dt)
            print(datetime.datetime.now())

            if not dt and dt <= datetime.datetime.now() - datetime.timedelta(hours=3):
                continue

            if pos > 600:
                if yoffset == 220:
                    break
                pos = 10
                yoffset = 220

            draw.text((pos + 25, yoffset),
                      icons[mapping[d['weather_icon'][0:2]]],
                      0, font=self.get_font(50))
            draw.text((pos, yoffset + 50),
                      d['weather_desc'],
                      0, font=self.get_font(8))
            draw.text((pos + 10, yoffset + 80),
                      u'%d°C' % d.get('temp'),
                      0, font=self.get_font(25))
            draw.text((pos, yoffset + 120),
                      days[dt.weekday()],
                      0, font=self.get_font(18))
            draw.text((pos + 30, yoffset + 120),
                      str(dt)[-8:-3],
                      0, font=self.get_font(18))
            draw.text((pos, yoffset + 155),
                      "rain: %d" % d.get('rain', -1),
                      0, font=self.get_font(14))
            draw.text((pos, yoffset + 175),
                      "%s" % str(dt)[:10],
                      0, font=self.get_font(10))
            pos += 100

        for pos in range(0, 600, 100):
            draw.line((pos, 20 + 20, pos, 420), fill=170)
        draw.line((0, 215, 600, 215), fill=170)

#        txt = ' '.join([i for i,j in icons.itervalues()])
#        draw.text((10, 0), txt, 0, font=font(50))

    def get_image(self):
        bgcolor = 255

        dirname = os.path.join('/tmp')
        fn = os.path.join(dirname, "kindle.png")  # FIXME: personalize

        image = Image.new("P", (600, 800), bgcolor)

        image.putpalette(
            list(self.gen_palette())
        )

        draw = ImageDraw.Draw(image)

        self.show_weather(draw)

        self.show_temp_humidity(draw)

        draw.text((270, 770), u"%s" % str(datetime.datetime.now()),
                  0, font=self.get_font(20))

        image.convert('L').save(fn, "png")

        response = HttpResponse(FileWrapper(open(fn, 'rb')), content_type='image/png')
#        response['Content-Disposition'] = 'attachment; filename="%s"' % 'kindle.png'
        return response

    def list(self, request):
        return self.get_image()
