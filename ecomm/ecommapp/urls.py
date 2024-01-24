from django.urls import path
from ecommapp import views
from ecommapp.views import SimpleView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('home',views.home),
    path('home2',views.home2),
    path('home3',views.home3),
    path('catfilter/<cv>',views.catfilter),
    path('range',views.range),
    path('sort/<sv>',views.sort),
    path('registration',views.registration),
    path('d',views.dummyregistration),
    path('login',views.login_user),
    path('logout',views.user_logout),
    path('pd/<pid>',views.product_detail),
    path('addtocart/<pid>',views.addtocart),
    path('po',views.place_order),
    path('cart',views.cart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail),
    path('about',views.about),
    path('contact',views.contact),
    path('add/<a>/<b>',views.addition),
    path('myview',SimpleView.as_view()),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)