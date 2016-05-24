# -*- coding: utf-8 -*-

__author__ = 'Vitor Chen'

import XlWorkers.Utils as Utils
from XlWorkers.Entities import TransEntity
from lxml import etree
import os


class StrResXml(object):
    _STR_TAG = 'string'
    _NAME_ATTR = 'name'

    def __init__(self, filename):
        # super().__init__()
        self._filename = filename
        self._str_ele_map = {}
        parser = etree.XMLParser(strip_cdata=False)
        self._xml_tree = etree.parse(filename, parser=parser)
        self.root_resource = self._xml_tree.getroot()
        self.lastNode = None
        for str_node in self.root_resource.findall(self._STR_TAG):
            self.lastNode = str_node
            node_attrib = str_node.attrib
            res_name = node_attrib.get(self._NAME_ATTR)
            if Utils.is_str_valid(res_name):
                self._str_ele_map[res_name] = str_node

    def getIdentify(self):
        return os.path.basename(self._filename)

    def get_res_value(self, res_name):
        result = ''
        str_node = self.get_res_node(res_name)
        if str_node is not None:
            result = str_node.text
        return result

    def get_res_node(self, res_name):
        str_node = self._str_ele_map.get(res_name)
        return str_node

    def hasNode(self,res_name):
        str_node = self.get_res_node(res_name)
        if str_node is not None:
            return True
        return False

    def gen_trans_entities(self):
        entities = []
        keys = self._str_ele_map.keys()
        if keys is not None:
            for key in keys:
                trans_str = self._str_ele_map.get(key).text
                trans_entity = TransEntity(key, trans_str)
                entities.append(trans_entity)
        return entities

    def update_res_node(self, res_name, trans_str):
        str_node = self.get_res_node(res_name)
        if str_node is not None:
            str_node.text = trans_str

    def insert_or_update_res_node(self, res_name, trans_str):
        # print("update res_name:{0},trans_str:{1}".format(res_name,trans_str))
        str_node = self.get_res_node(res_name)
        if str_node is not None:
            str_node.text = trans_str
        else :
            if self.lastNode is not None:
                self.lastNode.tail = "\n\t"
            #insert node
            # str_node = etree.Element(self._STR_TAG)
            str_node = self.root_resource.makeelement(self._STR_TAG,{self._NAME_ATTR:res_name})
            # str_node.set(self._NAME_ATTR,res_name)
            str_node.text = trans_str
            str_node.tail = "\n"
            
            self.root_resource.append(str_node)

            self.lastNode = str_node

    def save(self, file_or_filename=None):
        if not file_or_filename:
            file_or_filename = self._filename
        self._xml_tree.write(file_or_filename, encoding="utf-8", xml_declaration=True, pretty_print=False)
