# -*- coding: utf-8 -*-
from maperipy import Map
from datetime import date

today = date.today()

#clear all layers
for i, layer in enumerate(Map.layers):
	layer.attribution = " "

copyright_info = "Map by OSM"

Map.layers[len(Map.layers)-1].attribution = copyright_info+"\n"+today.strftime("%B %d, %Y")
