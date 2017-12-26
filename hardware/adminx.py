from .models import HardwareType, HardwareModel
import xadmin
from xadmin import views, Settings

from xadmin.views import CommAdminView
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Field, Row, Col, Div, AppendedText, Side
from xadmin.plugins.inline import Inline

class HardwareModelInline(object):
    model = HardwareModel
    fk_name = 'hardwareType'
    fields = ('hardwareType', 'cpu')

@xadmin.sites.register(HardwareType)
class HardwareTypeAdmin(object):
    list_display = ('name', 'isVM')
    inlines = [HardwareModelInline, ]

#xadmin.site.register(HardwareType, HardwareTypeAdmin)