#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Christian Quest 2024                                       ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge_Point, SourceDataGouv, CSV, Load_XY, Conflate, Select, Mapping


class Analyser_Merge_Places_PMR_Angers(Analyser_Merge_Point):
    def __init__(self, config, logger = None):
        Analyser_Merge_Point.__init__(self, config, logger)
        self.def_class_missing_official(item = 8130, id = 21, level = 3, tags = ['merge', 'parking', 'fix:imagery', 'fix:survey'],
            title = T_('Disabled parking space not integrated'))

        self.init(
            "https://www.data.gouv.fr/fr/datasets/places-de-stationnement-pmr-angers",
            "Places de stationnement PMR - Angers",
            CSV(
                SourceDataGouv(
                    attribution="Angers Loire Métropole",
                    encoding="utf-8-sig",
                    dataset="63c228dc74f7a378cef0b7db",
                    resource="00e7b442-9569-4009-8470-6e8daa21c962")),
            Load_XY("longitude", "latitude"),
            Conflate(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = [
                      {"amenity": "parking", "capacity:disabled": "yes"},
                      {"amenity": "parking_space", "capacity:disabled": "yes"},
                      {"amenity": "parking_space", "capacity:disabled": "1"},
                      {"amenity": "parking_space", "wheelchair": "yes"}
                      ]),
                osmRef = "ref:FR:Angers",
                conflationDistance = 20,
                mapping = Mapping(
                    static1 = {"amenity": "parking_space",
                               "parking_space": "disabled",
                               "wheelchair": "yes"}),
                    static2 = {"source": self.source},
                    mapping1 = {"ref:FR:Angers": "id"},
                    text = lambda tags, fields: T_("Disabled parking space {0} {1}", fields["nombre","adresse_1"]) ))

