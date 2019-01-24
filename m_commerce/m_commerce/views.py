from django.shortcuts import render

from commodity.models import Carousel, Activity_zone


def index(request):
    if request.method == 'GET':
        # 查询轮播表全部信息
        carousel = Carousel.objects.all()
        # 查询活动专区
        activity = Activity_zone.objects.all()

        context = {
            'carousel':carousel,
            'activity':activity,
        }
        return render(request,'common/index.html',context=context)