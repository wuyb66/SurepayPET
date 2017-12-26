from ajax_select import register, LookupChannel
from .models import Country,State,City
from django.db.models import Q

@register('countries')
class CountryLookup(LookupChannel):
    model = Country

    def get_query(self, q, request):
        return Country.objects.filter(Q(name__icontains=q))

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "<div class='lookups'>%s<div></div></div>" %(obj.name)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "<div>%s</div>" %(obj.name)

@register("states")
class StateLookup(LookupChannel):
    model = State

    def get_query(self, q, request):
        countryId = request.GET['idUpset'] # This information is get in request by javascript in templates
        retorno = State.objects.filter(Q(country__id=countryId)).filter(Q(name__icontains=q)).order_by('name')
        return retorno

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.name

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return "<div class='lookups'>%s<div></div></div>" %(obj.name)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return "<div>%s</div>" %(obj.name)