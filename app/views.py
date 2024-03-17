from django.shortcuts import render
from .models import Restuarant
from django.views import View

# Create your views here.


class GetOneRestaurantByIdView(View):

    def get_obj(self, id):

        try:
            obj = Restuarant.objects.get(id = id)
        except:
            raise ValueError(f"Restaurant not exist with id: {id}")
        
        return obj
    

    def get(self, request, id):

        restaurant_details = self.get_obj(id = id)

        context = {
            'restaurant_details': restaurant_details
        }

        return render(request,"one_restaurant.html", context=context)
        

