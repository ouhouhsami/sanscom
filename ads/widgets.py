#-*- coding: utf-8 -*-
from leaflet.forms.widgets import LeafletWidget

class ExtendedLeafletWidget(LeafletWidget):
    geometry_field_class = 'NoRectangleGeometryField'
    template_name = 'widgets/leaflet_extended.html'
