from django.shortcuts import render

from commodity.models import Carousel


def index(request):
    if request.method == 'GET':
        # 查询轮播表全部信息
        carousel = Carousel.objects.all()


        context = {
            'carousel':carousel,
        }
        return render(request,'common/index.html',context=context)