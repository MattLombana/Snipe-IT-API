#! /usr/bin/env python3

import datetime
import json
import requests


class SnipeAPI(object):
    """
    Class representing a Snipe-It API version 4.8.0
    """

    def __init__(self, server, token):
        """
        init(server, token)

        init creates a new instance of the Snipe-IT API

        Params:
            server : str : The url that the snipe-it server is located at. No trailing slash
                ex. 'https://develop.snipeitapp.com'
            token : str : Your API token
                ex. 'eyJ0eXAiOiJKV1QiLCJhb...'
        """
        self._server = server
        self._token = token
        self._session = requests.Session()

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self._headers = headers
        self._session.headers.update(headers)


####################################################################################################
#                                       Precondition Methods                                       #
####################################################################################################


    def _precondition_error(self, s):
        """
        _precondition_error(s)

        _precondition_error raises a ValueError with the message s

        Params:
            s : str : the error message to raise
        """
        raise ValueError(s)

    def _precondition_str(self, s):
        """
        _precondition_str(s)

        Verifies that s is a string, or NoneType. Calls precondition_error otherwise

        Params:
            s : the argument to check
        """
        if s is None:
            return
        if type(s) != str:
            self._precondition_error('{} is not a string!'.format(s))

    def _precondition_int(self, i):
        """
        _precondition_int(i)

        Verifies that i is a int, or NoneType. Calls precondition_error otherwise

        Params:
            i : the argument to check
        """
        if i is None:
            return
        if type(i) != int:
            self._precondition_error('{} is not a string!'.format(i))

    def _precondition_float(self, f):
        """
        _precondition_float(f)

        Verifies that f is a float, or NoneType. Calls precondition_error otherwise

        Params:
            f : the argument to check
        """
        if f is None:
            return
        if type(f) != float:
            self._precondition_error('{} is not a float!'.format(f))

    def _precondition_bool(self, b):
        """
        _precondition_bool(b)

        Verifies that b is a bool, or NoneType. Calls precondition_error otherwise

        Params:
            b : the argument to check
        """
        if b is None:
            return
        if type(b) != bool:
            self._precondition_error('{} is not a boolean!'.format(b))

    def _precondition_enum(self, s, enum):
        """
        _precondition_enum(s, enum)

        Verifies that s is a string that exists in enum, or NoneType. Calls precondition_error otherwise

        Params:
            s : the argument to check
            enum : list : a list of acceptable strings
        """
        if s is None:
            return
        if s in enum:
            return
        self._precondition_error('{} is not in the accepted values list: {}!'.format(s, enum))

    def _precondition_date(self, d):
        """
        _precondition_date(d)

        Verifies that d is a date, or NoneType. Calls precondition_error otherwise

        Params:
            d : the argument to check
        """
        if d is None:
            return
        try:
            datetime.datetime.strptime(d, '%Y-%m-%d')
            return
        except ValueError:
            self._precondition_error('{} is not a date!'.format(d))

    def _precondition_list(self, l, item_type=None):
        """
        _precondition_list(l, item_type)

        Verifies that l is a list, or NoneType. If item_type is given, it recursively verifies
        that each item is of the specified type. Calls precondition_error otherwise

        Params:
            l : the argument to check
            item_type : optional string : str | int | bool | date | float
        """
        if l is None:
            return
        if type(l) != list:
            self._precondition_error('{} is not a list!'.format(l))
        if item_type == 'str':
            for item in l:
                self._precondition_str(item)
        if item_type == 'int':
            for item in l:
                self._precondition_int(item)
        if item_type == 'bool':
            for item in l:
                self._precondition_bool(item)
        if item_type == 'date':
            for item in l:
                self._precondition_date(item)
        if item_type == 'float':
            for item in l:
                self._precondition_float(item)


####################################################################################################
#                                         Generic Helpers                                          #
####################################################################################################

    def _add_to_dict(self, d, k, v):

        """
        _add_to_dict(d, k, v)

        add k:v to d, iff k and v are not None. if k is expand and V is not none, convert v to a
        lowercase string first.

        Params:
            d : dict : the dict to modify
            k : str : the key to add
            v : any : the value to add
        """

        if k == 'expand' and v:
            v = str(v).lower()
        if k and v:
            d[k] = v

####################################################################################################
#                                           HTTP Methods                                           #
####################################################################################################

    def _get(self, path, params):
        """
        _get(path, params)

        this is a wrapper around the python requests get function


        Params:
            path : str : the path to send the request to
            params : dict : the params to pass to the request function
        """
        url = self._server + path

        if params:
            data = json.dumps(params)
            resp = self._session.get(url, params=data)
        else:
            resp = self._session.get(url)
        return resp.json()

    def _post(self, path, payload):
        """
        _post(path, payload)

        this is a wrapper around the python requests post function

        Params:
            path : str : the path to send the request to
            payload : dict : the params to pass to the request function
        """
        url = self._server + path
        if payload:
            data = json.dumps(payload)
            resp = self._session.post(url, data=data)
        else:
            resp = self._session.post(url)
        return resp.json()

    def _put(self, path, payload):
        """
        _put(path, payload)

        this is a wrapper around the python requests put function

        Params:
            path : str : the path to send the request to
            payload : dict : the params to pass to the request function
        """
        url = self._server + path
        if payload:
            data = json.dumps(payload)
            resp = self._session.put(url, data=data)
        else:
            resp = self._session.put(url)
        return resp.json()

    def _patch(self, path, payload):
        """
        _patch(path, payload)

        this is a wrapper around the python requests patch function

        Params:
            path : str : the path to send the request to
            payload : dict : the params to pass to the request function
        """
        url = self._server + path
        if payload:
            data = json.dumps(payload)
            resp = self._session.patch(url, data=data)
        else:
            resp = self._session.patch(url)
        return resp.json()

    def _delete(self, path, payload):
        """
        _delete(path, payload)

        this is a wrapper around the python requests delete function

        Params:
            path : str : the path to send the request to
            payload : dict : the params to pass to the request function
        """
        url = self._server + path
        if payload:
            data = json.dumps(payload)
            resp = self._session.delete(url, data=data)
        else:
            resp = self._session.delete(url)
        return resp.json()


####################################################################################################
#                                           Accessories                                            #
####################################################################################################

    def create_accessory(self, name, qty, category_id, order_number=None, purchase_cost=None, purchase_date=None, model_number=None, company_id=None, location_id=None, manufacturer_id=None, supplier_id=None):

        self._precondition_str(name)
        self._precondition_int(qty)
        self._precondition_str(order_number)
        self._precondition_float(purchase_cost)
        self._precondition_str(purchase_date)
        self._precondition_str(model_number)
        self._precondition_int(category_id)
        self._precondition_int(company_id)
        self._precondition_int(location_id)
        self._precondition_int(manufacturer_id)
        self._precondition_int(supplier_id)
        payload = {
            'name': name,
            'qty': qty,
            'category_id': category_id
        }
        self._add_to_dict(payload, 'order_number', order_number)
        self._add_to_dict(payload, 'purchase_cost', purchase_cost)
        self._add_to_dict(payload, 'purchase_date', purchase_date)
        self._add_to_dict(payload, 'model_number', model_number)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'location_id', location_id)
        self._add_to_dict(payload, 'manufacturer_id', manufacturer_id)
        self._add_to_dict(payload, 'supplier_id', supplier_id)
        path = '/api/v1/accessories'
        return self._post(path, payload)

    def get_accessories(self, limit=None, offset=None, search=None, order_number=None, sort=None, order=None, expand=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_str(order_number)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        self._precondition_bool(expand)
        params = {}
        self._add_to_dict(params, 'limit', limit)
        self._add_to_dict(params, 'offset', offset)
        self._add_to_dict(params, 'search', search)
        self._add_to_dict(params, 'order_number', order_number)
        self._add_to_dict(params, 'sort', sort)
        self._add_to_dict(params, 'order', order)
        self._add_to_dict(params, 'expand', expand)
        params = str(params)
        path = '/api/v1/accessories'
        return self._get(path, params)

    def get_accessory_by_id(self, accessory_id):
        self._precondition_int(accessory_id)
        path = '/api/v1/accessories/{}'.format(accessory_id)
        return self._get(path, None)

    def get_accessory_by_name(self, name):
        accessories = self.get_accessories(search=name)
        for accessory in accessories['rows']:
            if accessory['name'] == name:
                return accessory
        return None


####################################################################################################
#                                              Assets                                              #
####################################################################################################

    def create_asset(self, status_id, model_id, asset_tag=None, name=None):

        self._precondition_str(asset_tag)
        self._precondition_int(status_id)
        self._precondition_int(model_id)
        self._precondition_str(name)
        payload = {
            'status_id': status_id,  # int
            'model_id': model_id,  # int
        }
        self._add_to_dict(payload, 'asset_tag', asset_tag)
        self._add_to_dict(payload, 'name', name)
        path = '/api/v1/hardware'
        return self._post(path, payload)

    def delete_asset(self, asset_id):
        self._precondition_int(asset_id)
        path = '/api/v1/hardware/{}'.format(asset_id)
        return self._delete(path, None)

    def get_assets(self, limit=None, offset=None, search=None, order_number=None, sort=None, order=None, model_id=None, category_id=None, manufacturer_id=None, company_id=None, location_id=None, status=None, status_id=None):

        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_str(order_number)
        self._precondition_int(model_id)
        self._precondition_int(category_id)
        self._precondition_int(manufacturer_id)
        self._precondition_int(company_id)
        self._precondition_int(location_id)
        self._precondition_str(status)
        self._precondition_str(status_id)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])

        path = '/api/v1/hardware'
        params = {}
        self._add_to_dict(params, 'limit', limit)
        self._add_to_dict(params, 'offset', offset)
        self._add_to_dict(params, 'search', search)
        self._add_to_dict(params, 'order_number', order_number)
        self._add_to_dict(params, 'sort', sort)
        self._add_to_dict(params, 'order', order)
        self._add_to_dict(params, 'model_id', model_id)
        self._add_to_dict(params, 'category_id', category_id)
        self._add_to_dict(params, 'manufacturer_id', manufacturer_id)
        self._add_to_dict(params, 'company_id', company_id)
        self._add_to_dict(params, 'location_id', location_id)
        self._add_to_dict(params, 'status', status)
        self._add_to_dict(params, 'status_id', status_id)

        return self._get(path, params)

    def get_asset_by_id(self, asset_id):
        self._precondition_int(asset_id)
        path = '/api/v1/hardware/{}'.format(asset_id)
        return self._get(path, None)

    def get_asset_by_name(self, name):
        assets = self.get_assets(search=name)
        for asset in assets['rows']:
            if asset['name'] == name:
                return asset
        return None

    def get_asset_by_serial(self, asset_serial):
        self._precondition_str(asset_serial)
        path = '/api/v1/hardware/byserial/{}'.format(asset_serial)
        return self._get(path, None)

    def get_asset_by_tag(self, asset_tag):
        self._precondition_str(asset_tag)
        path = '/api/v1/hardware/bytag/{}'.format(asset_tag)
        return self._get(path, None)

    def get_assets_by_status_id(self, status_label_id):
        self._precondition_int(status_label_id)
        path = '/api/v1/statuslabels/{}/assetlist'.format(status_label_id)
        return self._get(path, None)


    def update_asset(self, asset_id, asset_tag=None, notes=None, status_id=None, model_id=None, last_checkout=None, assigned_to=None, company_id=None, serial=None, order_number=None, warranty_months=None, purchase_cost=None, purchase_date=None, requestable=None, archived=None, rtd_location_id=None, name=None):

        self._precondition_int(asset_id)
        self._precondition_str(asset_tag)
        self._precondition_str(notes)
        self._precondition_int(status_id)
        self._precondition_int(model_id)
        self._precondition_date(last_checkout)
        self._precondition_int(assigned_to)
        self._precondition_int(company_id)
        self._precondition_str(serial)
        self._precondition_str(order_number)
        self._precondition_int(warranty_months)
        self._precondition_float(purchase_cost)
        self._precondition_date(purchase_date)
        self._precondition_bool(requestable)
        self._precondition_bool(archived)
        self._precondition_int(rtd_location_id)
        self._precondition_str(name)
        payload = {}
        self._add_to_dict(payload, 'asset_tag', asset_tag)
        self._add_to_dict(payload, 'notes', notes)
        self._add_to_dict(payload, 'status_id', status_id)
        self._add_to_dict(payload, 'model_id', model_id)
        self._add_to_dict(payload, 'last_checkout', last_checkout)
        self._add_to_dict(payload, 'assigned_to', assigned_to)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'serial', serial)
        self._add_to_dict(payload, 'order_number', order_number)
        self._add_to_dict(payload, 'warranty_months', warranty_months)
        self._add_to_dict(payload, 'purchase_cost', purchase_cost)
        self._add_to_dict(payload, 'purchase_date', purchase_date)
        self._add_to_dict(payload, 'requestable', requestable)
        self._add_to_dict(payload, 'archived', archived)
        self._add_to_dict(payload, 'rtd_location_id', rtd_location_id)
        self._add_to_dict(payload, 'name', name)
        print(payload)

        path = '/api/v1/hardware/{}'.format(asset_id)
        return self._patch(path, payload)

####################################################################################################
#                                            Categories                                            #
####################################################################################################

    def create_category(self, name, category_type, use_default_eula=None, require_acceptance=None, checkin_email=None):
        self._precondition_str(name)
        self._precondition_enum(category_type, ['asset', 'accessory', 'consumable', 'component', 'license'])

        self._precondition_bool(use_default_eula)
        self._precondition_bool(require_acceptance)
        self._precondition_bool(checkin_email)
        payload = {
            'name': name,  # string
            'category_type': category_type,  # string
        }
        self._add_to_dict(payload, 'use_default_uela', use_default_eula)
        self._add_to_dict(payload, 'require_acceptance', require_acceptance)
        self._add_to_dict(payload, 'checkin_email', checkin_email)
        path = '/api/v1/categories'
        return self._post(path, payload)

    def delete_category(self, category_id):
        self._precondition_int(category_id)
        path = '/api/v1/categories/{}'.format(category_id)
        return self._delete(path, None)

    def get_categories(self, limit=None, offset=None, search=None, sort=None, order=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_str(sort)
        self._precondition_enum(order, ['asc', 'desc'])
        payload = {}
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)

        path = '/api/v1/categories'
        return self._get(path, payload)

    def get_category_by_id(self, category_id):
        self._precondition_int(category_id)
        path = '/api/v1/categories/{}'.format(category_id)
        return self._get(path, None)

    def get_category_by_name(self, name):
        categories = self.get_categories(search=name)
        for category in categories['rows']:
            if category['name'] == name:
                return category
        return None

    def update_category(self, category_id, name, category_type, use_default_eula=None, require_acceptance=None, checkin_email=None):
        self._precondition_int(category_id)
        self._precondition_str(name)
        self._precondition_str(category_type)
        self._precondition_bool(use_default_eula)
        self._precondition_bool(require_acceptance)
        self._precondition_bool(checkin_email)
        payload = {
            'name': name,  # string
            'category_type': category_type,  # string
        }
        self._add_to_dict(payload, 'use_default_uela', use_default_eula)
        self._add_to_dict(payload, 'require_acceptance', require_acceptance)
        self._add_to_dict(payload, 'checkin_email', checkin_email)

        path = '/api/v1/categories/{}'.format(category_id)
        return self._patch(path, payload)

####################################################################################################
#                                            Companies                                             #
####################################################################################################

    def create_company(self, name):
        self._precondition_str(name)
        payload = {
            'name': name  # str
        }
        path = '/api/v1/companies'
        return self._post(path, payload)

    def delete_company(self, company_id):
        self._precondition_int(company_id)
        path = '/api/v1/companies/{}'.format(company_id)
        self._delete(path, None)

    def get_companies(self, search=None):
        self._precondition_str(search)
        payload = {}
        self._add_to_dict(payload, 'search', search)
        path = '/api/v1/companies'
        return self._get(path, None)

    def get_company_by_id(self, company_id):
        self._precondition_int(company_id)
        path = '/api/v1/companies/{}'.format(company_id)
        return self._get(path, None)

    def get_company_by_name(self, name):
        companies = self.get_companies(search=name)
        for company in companies['rows']:
            if company['name'] == name:
                return company
        return None

    def update_company(self, company_id, name):
        self._precondition_int(company_id)
        self._precondition_str(name)
        payload = {
            'name': name  # str
        }
        path = '/api/v1/companies/{}'.format(company_id)
        return self._patch(path, payload)

####################################################################################################
#                                            Components                                            #
####################################################################################################

    def create_component(self, name, qty, category_id):
        self._precondition_str(name)
        self._precondition_int(qty)
        self._precondition_int(category_id)
        payload = {
            'name': name,  # str
            'qty': qty,  # int
            'category_id': category_id,  # int
        }
        path = '/api/v1/components'
        return self._post(path, payload)

    def get_components(self, limit=None, offset=None, search=None, order_number=None, sort=None, order=None, expand=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_str(order_number)
        self._precondition_enum(order, ['asc', 'desc'])
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_bool(expand)
        payload = {}
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'order_number', order_number)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)
        self._add_to_dict(payload, 'expand', expand)

        path = '/api/v1/components'
        return self._get(path, payload)

    def get_component_by_id(self, component_id):
        self._precondition_int(component_id)
        path = '/api/v1/components/{}'.format(component_id)
        return self._get(path, None)

    def get_component_by_name(self, name):
        components = self.get_components(search=name)
        for component in components['rows']:
            if component['name'] == name:
                return component
        return None


####################################################################################################
#                                           Consumables                                            #
####################################################################################################


    def create_consumable(self, name, qty, category_id):
        self._precondition_str(name)
        self._precondition_int(qty)
        self._precondition_int(category_id)
        payload = {
            'name': name,  # str
            'qty': qty,  # int
            'category_id': category_id  # int
        }
        path = '/api/v1/consumables'
        return self._post(path, payload)

    def get_consumables(self, limit=None, offset=None, search=None, order_number=None, sort=None, order=None, expand=None, category_id=None, company_id=None, manufacturer_id=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_str(order_number)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        self._precondition_bool(expand)
        self._precondition_int(category_id)
        self._precondition_int(company_id)
        self._precondition_int(manufacturer_id)
        payload = {}
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'order_number', order_number)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)
        self._add_to_dict(payload, 'expand', expand)
        self._add_to_dict(payload, 'category_id', category_id)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'manufacturer_id', manufacturer_id)

        path = '/api/v1/consumables'
        return self._get(path, payload)

    def get_consumable_by_id(self, consumable_id):
        self._precondition_int(consumable_id)
        path = '/api/v1/consumables/{}'.format(consumable_id)
        return self._get(path, None)

    def get_consumable_by_name(self, name):
        consumables = self.get_consumables(search=name)
        for consumable in consumables['rows']:
            if consumable['name'] == name:
                return consumable
        return None


####################################################################################################
#                                              Fields                                             #
####################################################################################################


    def create_field(self, name, element, field_values=None, fmt=None, custom_format=None, help_text=None, show_in_email=None, field_encrypted=None):
        self._precondition_str(name)
        self._precondition_enum(element, ['text', 'listbox', 'textarea'])
        self._precondition_list(field_values, item_type='str')
        self._precondition_enum(fmt, ['ANY', 'CUSTOM REGEX', 'ALPHA', 'ALPHA-DASH', 'NUMERIC', 'ALPHA-NUMERIC', 'EMAIL', 'DATE', 'URL', 'IP', 'IPV4', 'IPV6', 'MAC', 'BOOLEAN'])
        self._precondition_str(custom_format)
        self._precondition_str(help_text)
        self._precondition_bool(show_in_email)
        self._precondition_bool(field_encrypted)
        payload = {
            'name': name,
            'element': element,
        }
        self._add_to_dict(payload, 'field_values', field_values)
        self._add_to_dict(payload, 'format', fmt)
        self._add_to_dict(payload, 'custom_format', custom_format)
        self._add_to_dict(payload, 'help_text', help_text)
        self._add_to_dict(payload, 'show_in_email', show_in_email)
        self._add_to_dict(payload, 'field_encrypted', field_encrypted)

        path = '/api/v1/fields'
        return self._post(path, payload)

    def delete_field(self, field_id):
        self._precondition_int(field_id)
        path = '/api/v1/fields/{}'.format(field_id)
        return self._delete(path, None)

    def get_fields(self):
        path = '/api/v1/fields'
        return self._get(path, None)

    def get_field_by_id(self, field_id):
        self._precondition_int(field_id)
        path = '/api/v1/fields/{}'.format(field_id)
        return self._get(path, None)

    def get_field_by_name(self, name):
        fields = self.get_fields()
        for field in fields['rows']:
            if field['name'] == name:
                return field
        return None

    def update_field(self, field_id, name, element, field_values=None, fmt=None, custom_format=None, help_text=None, show_in_email=None, field_encrypted=None):
        self._precondition_int(field_id)
        self._precondition_str(name)
        self._precondition_enum(element, ['text', 'listbox', 'textarea'])
        self._precondition_list(field_values, item_type='str')
        self._precondition_enum(fmt, ['ANY', 'CUSTOM REGEX', 'ALPHA', 'ALPHA-DASH', 'NUMERIC', 'ALPHA-NUMERIC', 'EMAIL', 'DATE', 'URL', 'IP', 'IPV4', 'IPV6', 'MAC', 'BOOLEAN'])
        self._precondition_str(custom_format)
        self._precondition_str(help_text)
        self._precondition_bool(show_in_email)
        self._precondition_bool(field_encrypted)
        payload = {
            'name': name,
            'element': element,
        }
        self._add_to_dict(payload, 'field_values', field_values)
        self._add_to_dict(payload, 'format', fmt)
        self._add_to_dict(payload, 'custom_format', custom_format)
        self._add_to_dict(payload, 'help_text', help_text)
        self._add_to_dict(payload, 'show_in_email', show_in_email)
        self._add_to_dict(payload, 'field_encrypted', field_encrypted)

        path = '/api/v1/fields/{}'.format(field_id)
        return self._patch(path, payload)


####################################################################################################
#                                            Fieldsets                                             #
####################################################################################################


    def create_fieldset(self, name):
        self._precondition_str(name)
        payload = {
            'name': name,  # str
        }
        path = '/api/v1/fieldsets'
        return self._post(path, payload)

    def delete_fieldset(self, fieldset_id):
        self._precondition_int(fieldset_id)
        path = '/api/v1/fieldsets/{}'.format(fieldset_id)
        return self._delete(path, None)

    def get_fieldsets(self):
        path = '/api/v1/fieldsets'
        return self._get(path, None)

    def get_fieldset_by_id(self, fieldset_id):
        self._precondition_int(fieldset_id)
        path = '/api/v1/fieldsets/{}'.format(fieldset_id)
        return self._get(path, None)

    def get_fieldset_by_name(self, name):
        fieldsets = self.get_fieldsets()
        for fieldset in fieldsets['rows']:
            if fieldset['name'] == name:
                return fieldset
        return None

    def update_fieldset(self, fieldset_id, name):
        self._precondition_int(fieldset_id)
        self._precondition_str(name)
        payload = {
            'name': name,  # str
        }
        path = '/api/v1/fieldsets/{}'.format(fieldset_id)
        return self._put(path, payload)

####################################################################################################
#                                             Licenses                                             #
####################################################################################################

    def create_license(self, name, seats, category_id, product_key=None, company_id=None, expiration_date=None, license_email=None, license_name=None, maintained=None, manufacturer_id=None, notes=None, order_number=None, purchase_cost=None, purchase_date=None, purchase_order=None, reassignable=None, serial=None, supplier_id=None, termination_date=None):
        self._precondition_str(name)
        self._precondition_int(seats)
        self._precondition_int(category_id)
        self._precondition_str(product_key)
        self._precondition_int(company_id)
        self._precondition_date(expiration_date)
        self._precondition_str(license_email)
        self._precondition_str(license_name)
        self._precondition_bool(maintained)
        self._precondition_int(manufacturer_id)
        self._precondition_str(notes)
        self._precondition_int(order_number)
        self._precondition_float(purchase_cost)
        self._precondition_date(purchase_date)
        self._precondition_str(purchase_order)
        self._precondition_bool(reassignable)
        self._precondition_str(serial)
        self._precondition_int(supplier_id)
        self._precondition_date(termination_date)
        payload = {
            'name': name,
            'seats': seats,
            'category_id': category_id
        }
        self._add_to_dict(payload, 'product_key', product_key)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'expiration_date', expiration_date)
        self._add_to_dict(payload, 'license_email', license_email)
        self._add_to_dict(payload, 'license_name', license_name)
        self._add_to_dict(payload, 'maintained', maintained)
        self._add_to_dict(payload, 'manufacturer_id', manufacturer_id)
        self._add_to_dict(payload, 'notes', notes)
        self._add_to_dict(payload, 'order_number', order_number)
        self._add_to_dict(payload, 'purchase_cost', purchase_cost)
        self._add_to_dict(payload, 'purchase_date', purchase_date)
        self._add_to_dict(payload, 'purchase_order', purchase_order)
        self._add_to_dict(payload, 'reassignable', reassignable)
        self._add_to_dict(payload, 'serial', serial)
        self._add_to_dict(payload, 'supplier_id', supplier_id)
        self._add_to_dict(payload, 'termination_date', termination_date)
        path = '/api/v1/licenses'
        return self._post(path, payload)

    def delete_license(self, license_id):
        self._precondition_int(license_id)
        path = '/api/v1/licenses/{}'.format(license_id)
        return self._delete(path, None)

    def get_licenses(self, limit=None, offset=None, search=None, order_number=None, sort=None, order=None, expand=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_str(order_number)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        self._precondition_bool(expand)
        params = {}
        self._add_to_dict(params, 'limit', limit)
        self._add_to_dict(params, 'offset', offset)
        self._add_to_dict(params, 'search', search)
        self._add_to_dict(params, 'order_number', order_number)
        self._add_to_dict(params, 'sort', sort)
        self._add_to_dict(params, 'order', order)
        self._add_to_dict(params, 'expand', expand)
        path = '/api/v1/licenses'
        return self._get(path, params)

    def get_license_by_id(self, license_id):
        self._precondition_int(license_id)
        path = '/api/v1/licenses/{}'.format(license_id)
        return self._get(path, None)

    def get_license_by_name(self, name):
        licenses = self.get_licenses(search=name)
        for license in licenses['rows']:
            if license['name'] == name:
                return license
        return None

    def update_license(self, license_id, name=None, seats=None, company_id=None, expiration_date=None, license_email=None, license_name=None, maintained=None, manufacturer_id=None, notes=None, order_number=None, purchase_cost=None, purchase_date=None, purchase_order=None, reassignable=None, serial=None, supplier_id=None, termination_date=None):
        self._precondition_int(license_id)
        self._precondition_str(name)
        self._precondition_int(seats)
        self._precondition_int(company_id)
        self._precondition_date(expiration_date)
        self._precondition_str(license_email)
        self._precondition_str(license_name)
        self._precondition_bool(maintained)
        self._precondition_int(manufacturer_id)
        self._precondition_str(notes)
        self._precondition_int(order_number)
        self._precondition_float(purchase_cost)
        self._precondition_date(purchase_date)
        self._precondition_str(purchase_order)
        self._precondition_bool(reassignable)
        self._precondition_str(serial)
        self._precondition_int(supplier_id)
        self._precondition_date(termination_date)
        payload = {}
        self._add_to_dict(payload, 'name', name)
        self._add_to_dict(payload, 'seats', seats)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'expiration_date', expiration_date)
        self._add_to_dict(payload, 'license_email', license_email)
        self._add_to_dict(payload, 'license_name', license_name)
        self._add_to_dict(payload, 'maintained', maintained)
        self._add_to_dict(payload, 'manufacturer_id', manufacturer_id)
        self._add_to_dict(payload, 'notes', notes)
        self._add_to_dict(payload, 'order_number', order_number)
        self._add_to_dict(payload, 'purchase_cost', purchase_cost)
        self._add_to_dict(payload, 'purchase_date', purchase_date)
        self._add_to_dict(payload, 'purchase_order', purchase_order)
        self._add_to_dict(payload, 'reassignable', reassignable)
        self._add_to_dict(payload, 'serial', serial)
        self._add_to_dict(payload, 'supplier_id', supplier_id)
        self._add_to_dict(payload, 'termination_date', termination_date)
        path = '/api/v1/licenses/{}'.format(license_id)
        return self._patch(path, payload)

####################################################################################################
#                                            Locations                                             #
####################################################################################################

    def create_location(self, name, address=None, address2=None, city=None, state=None, country=None, zipcode=None):
        self._precondition_str(name)
        self._precondition_str(address)
        self._precondition_str(address2)
        self._precondition_str(city)
        self._precondition_str(state)
        self._precondition_str(country)
        self._precondition_str(zipcode)
        payload = {
            'name': name,
        }
        self._add_to_dict(payload, 'address', address)
        self._add_to_dict(payload, 'address2', address2)
        self._add_to_dict(payload, 'city', city)
        self._add_to_dict(payload, 'state', state)
        self._add_to_dict(payload, 'country', country)
        self._add_to_dict(payload, 'zip', zipcode)
        path = '/api/v1/locations'
        return self._post(path, payload)

    def delete_location(self, location_id):
        self._precondition_int(location_id)
        path = '/api/v1/locations/{}'.format(location_id)
        return self._delete(path, None)

    def get_locations(self, limit=None, offset=None, search=None, sort=None, order=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        payload = {}
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)
        path = '/api/v1/locations'
        return self._get(path, payload)

    def get_location_by_id(self, location_id):
        self._precondition_int(location_id)
        path = '/api/v1/locations/{}'.format(location_id)
        return self._get(path, None)

    def get_location_by_name(self, name):
        locations = self.get_locations(search=name)
        for location in locations['rows']:
            if location['name'] == name:
                return location
        return None

    def update_location(self, location_id, name=None, address=None, address2=None, city=None, state=None, country=None, zipcode=None):
        self._precondition_int(location_id)
        self._precondition_str(name)
        self._precondition_str(address)
        self._precondition_str(address2)
        self._precondition_str(city)
        self._precondition_str(state)
        self._precondition_str(country)
        self._precondition_str(zipcode)
        payload = {}
        self._add_to_dict(payload, 'name', name)
        self._add_to_dict(payload, 'address', address)
        self._add_to_dict(payload, 'address2', address2)
        self._add_to_dict(payload, 'city', city)
        self._add_to_dict(payload, 'state', state)
        self._add_to_dict(payload, 'country', country)
        self._add_to_dict(payload, 'zip', zipcode)
        path = '/api/v1/locations/{}'.format(location_id)
        return self._patch(path, payload)


####################################################################################################
#                                           Maintenances                                           #
####################################################################################################

    def create_maintenace(self, name, address=None, address2=None, state=None, country=None, zipcode=None):

        self._precondition_str(name)
        self._precondition_str(address)
        self._precondition_str(address2)
        self._precondition_str(state)
        self._precondition_str(country)
        self._precondition_str(zipcode)
        payload = {
            'name': name,  # str
        }
        self._add_to_dict(payload, 'address', address)
        self._add_to_dict(payload, 'address2', address2)
        self._add_to_dict(payload, 'state', state)
        self._add_to_dict(payload, 'country', country)
        self._add_to_dict(payload, 'zip', zipcode)
        path = '/api/v1/maintenances'
        return self._post(path, payload)

    def get_maintenaces(self, limit=None, offset=None, search=None, sort=None, order=None, asset_id=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        self._precondition_int(asset_id)
        payload = {}
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)
        self._add_to_dict(payload, 'asset_id', asset_id)
        path = '/api/v1/maintenances'
        return self._get(path, payload)

####################################################################################################
#                                          Manufacturers                                           #
####################################################################################################

    def create_manufacturer(self, name):
        self._precondition_str(name)
        payload = {
            'name': name,
        }
        path = '/api/v1/manufacturers'
        return self._post(path, payload)

    def delete_manufacturer(self, manufacturer_id):
        self._precondition_int(manufacturer_id)
        path = '/api/v1/manufacturers/{}'.format(manufacturer_id)
        return self._delete(path, None)

    def get_manufacturers(self, search=None):
        self._precondition_str(search)
        payload = {}
        self._add_to_dict(payload, 'search', search)
        path = '/api/v1/manufacturers'
        return self._get(path, payload)

    def get_manufacturer_by_id(self, manufacturer_id):
        self._precondition_int(manufacturer_id)
        path = '/api/v1/manufacturers/{}'.format(manufacturer_id)
        return self._get(path, None)

    def get_manufacturer_by_name(self, name):
        manufacturers = self.get_manufacturers(search=name)
        for manufacturer in manufacturers['rows']:
            if manufacturer['name'] == name:
                return manufacturer
        return None

    def update_manufacturer(self, manufacturer_id, name):


        self._precondition_int(manufacturer_id)
        self._precondition_str(name)
        payload = {
            'name': name,
        }
        path = '/api/v1/manufacturers'
        return self._patch(path, payload)

####################################################################################################
#                                              Models                                              #
####################################################################################################

    def create_model(self, name, category_id, manufacturer_id, model_number=None, eol=None, fieldset_id=None):
        self._precondition_str(name)
        self._precondition_str(model_number)
        self._precondition_int(category_id)
        self._precondition_int(manufacturer_id)
        self._precondition_int(eol)
        self._precondition_int(fieldset_id)
        payload = {
            'name': name,
            'category_id': category_id,
            'manufacturer_id': manufacturer_id,
        }
        self._add_to_dict(payload, 'model_number', model_number)
        self._add_to_dict(payload, 'eol', eol)
        self._add_to_dict(payload, 'fieldset_id', fieldset_id)
        path = '/api/v1/models'
        return self._post(path, payload)

    def delete_model(self, model_id):
        self._precondition_int(model_id)
        path = '/api/v1/models/{}'.format(model_id)
        return self._delete(path, None)

    def get_models(self, limit=None, offset=None, search=None, sort=None, order=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        payload = {}
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)
        path = '/api/v1/models'
        return self._get(path, payload)

    def get_model_by_id(self, model_id):
        self._precondition_int(model_id)
        path = '/api/v1/models/{}'.format(model_id)
        return self._get(path, None)

    def get_model_by_name(self, name):
        models = self.get_models(search=name)
        for model in models['rows']:
            if model['name'] == name:
                return model
        return None

    def update_model(self, model_id, name, category_id, manufacturer_id, model_number=None, eol=None, fieldset_id=None):
        self._precondition_int(model_id)
        self._precondition_str(name)
        self._precondition_str(model_number)
        self._precondition_int(category_id)
        self._precondition_int(manufacturer_id)
        self._precondition_int(eol)
        self._precondition_int(fieldset_id)
        payload = {
            'name': name,
            'category_id': category_id,
            'manufacturer_id': manufacturer_id,
        }
        self._add_to_dict(payload, 'model_number', model_number)
        self._add_to_dict(payload, 'eol', eol)
        self._add_to_dict(payload, 'fieldset_id', fieldset_id)
        path = '/api/v1/models/{}'.format(model_id)
        return self._patch(path, payload)

####################################################################################################
#                                          Status Labels                                           #
####################################################################################################

    def create_status_label(self, name, type_name):
        self._precondition_str(name)
        self._precondition_enum(type_name, ['deployable', 'pending', 'archived'])
        payload = {
            'name': name,  # str
        }
        self._add_to_dict(payload, 'type', type_name)
        path = '/api/v1/statuslabels'
        return self._post(path, payload)

    def delete_status_label(self, status_label_id):
        self._precondition_int(status_label_id)
        path = '/api/v1/statuslabels/{}'.format(status_label_id)
        return self._delete(path, None)

    def get_status_labels(self, limit=None, offset=None, search=None, sort=None, order=None):
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_str(search)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        payload = {}
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)
        path = '/api/v1/statuslabels'
        return self._get(path, payload)

    def get_status_label_by_id(self, status_label_id):
        self._precondition_int(status_label_id)
        path = '/api/v1/statuslabels/{}'.format(status_label_id)
        return self._get(path, None)

    def update_status_label(self, status_label_id, name, type_name):
        self._precondition_int(status_label_id)
        self._precondition_str(name)
        self._precondition_enum(type_name, ['deployable', 'pending', 'archived'])

        deployable_bool = False
        pending_bool = False
        archived_bool = False
        if type_name == 'deployable':
            deployable_bool = True
        elif type_name == 'pending':
            pending_bool = True
        elif type_name == 'archived':
            archived_bool = True
        payload = {
            'name': name,
            'deployable': deployable_bool,
            'pending': pending_bool,
            'archived': archived_bool,
        }
        path = '/api/v1/statuslabels/{}'.format(status_label_id)
        return self._post(path, payload)


####################################################################################################
#                                              Users                                               #
####################################################################################################

    def create_user(self, first_name, username, password, last_name=None, email=None, permissions=None, activated=None, phone=None, jobtitle=None, manager_id=None, employee_num=None, notes=None, company_id=None, two_factor_enrolled=None, two_factor_optin=None, department_id=None, location_id=None):

        self._precondition_str(first_name)
        self._precondition_str(last_name)
        self._precondition_str(username)
        self._precondition_str(password)
        self._precondition_str(email)
        self._precondition_str(permissions)
        self._precondition_bool(activated)
        self._precondition_str(phone)
        self._precondition_str(jobtitle)
        self._precondition_int(manager_id)
        self._precondition_str(employee_num)
        self._precondition_str(notes)
        self._precondition_int(company_id)
        self._precondition_bool(two_factor_enrolled)
        self._precondition_bool(two_factor_optin)
        self._precondition_int(department_id)
        self._precondition_int(location_id)
        payload = {
            'first_name': first_name,  # str
            'username': username,  # str
            'password': password,  # str
            'password_confirmation': password,  # str
        }
        self._add_to_dict(payload, 'last_name', last_name)
        self._add_to_dict(payload, 'email', email)
        self._add_to_dict(payload, 'permissions', permissions)
        self._add_to_dict(payload, 'activated', activated)
        self._add_to_dict(payload, 'phone', phone)
        self._add_to_dict(payload, 'jobtitle', jobtitle)
        self._add_to_dict(payload, 'manager_id', manager_id)
        self._add_to_dict(payload, 'employee_num', employee_num)
        self._add_to_dict(payload, 'notes', notes)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'two_factor_enrolled', two_factor_enrolled)
        self._add_to_dict(payload, 'two_factor_optin', two_factor_optin)
        self._add_to_dict(payload, 'department_id', department_id)
        self._add_to_dict(payload, 'location_id', location_id)
        path = '/api/v1/users'
        return self._post(path, payload)

    def delete_user(self, user_id):
        self._precondition_int(user_id)
        path = '/api/v1/users/{}'.format(user_id)
        return self._delete(path, None)

    def get_users(self, search=None, limit=None, offset=None, sort=None, order=None, group_id=None, company_id=None, department_id=None, deleted=None):
        self._precondition_str(search)
        self._precondition_int(limit)
        self._precondition_int(offset)
        self._precondition_enum(sort, ['id', 'name', 'asset_tag', 'serial', 'model', 'model_number', 'last_checkout', 'category', 'manufacturer', 'notes', 'expected_checkin', 'order_number', 'companyName', 'location', 'image', 'status_label', 'assigned_to', 'created_at', 'purchase_date', 'purchase_cost'])
        self._precondition_enum(order, ['asc', 'desc'])
        self._precondition_int(group_id)
        self._precondition_int(company_id)
        self._precondition_int(department_id)
        self._precondition_bool(deleted)
        payload = {}
        self._add_to_dict(payload, 'search', search)
        self._add_to_dict(payload, 'limit', limit)
        self._add_to_dict(payload, 'offset', offset)
        self._add_to_dict(payload, 'sort', sort)
        self._add_to_dict(payload, 'order', order)
        self._add_to_dict(payload, 'group_id', group_id)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'department_id', department_id)
        self._add_to_dict(payload, 'deleted', deleted)
        path = '/api/v1/users'
        return self._get(path, payload)

    def get_user_by_id(self, user_id):
        self._precondition_int(user_id)
        path = '/api/v1/users/{}'.format(user_id)
        return self._get(path, None)

    def get_user_by_name(self, name):
        users = self.get_users(search=name)
        for user in users['rows']:
            if user['name'] == name:
                return user
        return None

    def get_users_checked_out_assets(self, user_id):
        self._precondition_int(user_id)
        path = '/api/v1/users/{}/assets'.format(user_id)
        return self._get(path, None)

    def get_users_checked_out_accessories(self, user_id):
        self._precondition_int(user_id)
        path = '/api/v1/users/{}/accessories'.format(user_id)
        return self._get(path, None)


    def update_user(self, user_id, first_name=None, username=None, password=None, last_name=None, email=None, permissions=None, activated=None, phone=None, jobtitle=None, manager_id=None, employee_num=None, notes=None, company_id=None, two_factor_enrolled=None, two_factor_optin=None, department_id=None, location_id=None):
        self._precondition_int(user_id)
        self._precondition_str(first_name)
        self._precondition_str(last_name)
        self._precondition_str(username)
        self._precondition_str(password)
        self._precondition_str(email)
        self._precondition_str(permissions)
        self._precondition_bool(activated)
        self._precondition_str(phone)
        self._precondition_str(jobtitle)
        self._precondition_int(manager_id)
        self._precondition_str(employee_num)
        self._precondition_str(notes)
        self._precondition_int(company_id)
        self._precondition_bool(two_factor_enrolled)
        self._precondition_bool(two_factor_optin)
        self._precondition_int(department_id)
        self._precondition_int(location_id)
        payload = {}
        self._add_to_dict(payload, 'first_name', first_name)
        self._add_to_dict(payload, 'username', username)
        self._add_to_dict(payload, 'password', password)
        self._add_to_dict(payload, 'password_confirmation', password)
        self._add_to_dict(payload, 'last_name', last_name)
        self._add_to_dict(payload, 'email', email)
        self._add_to_dict(payload, 'permissions', permissions)
        self._add_to_dict(payload, 'activated', activated)
        self._add_to_dict(payload, 'phone', phone)
        self._add_to_dict(payload, 'jobtitle', jobtitle)
        self._add_to_dict(payload, 'manager_id', manager_id)
        self._add_to_dict(payload, 'employee_num', employee_num)
        self._add_to_dict(payload, 'notes', notes)
        self._add_to_dict(payload, 'company_id', company_id)
        self._add_to_dict(payload, 'two_factor_enrolled', two_factor_enrolled)
        self._add_to_dict(payload, 'two_factor_optin', two_factor_optin)
        self._add_to_dict(payload, 'department_id', department_id)
        self._add_to_dict(payload, 'location_id', location_id)
        path = '/api/v1/users/{}'.format(user_id)
        return self._patch(path, payload)


####################################################################################################
#                                             Suppliers                                            #
####################################################################################################


    def create_supplier(self, name, address=None, address2=None, state=None, city=None, country=None, zipcode=None, contact=None, phone=None, fax=None, email=None, url=None, notes=None):
        self._precondition_str(name)
        self._precondition_str(address)
        self._precondition_str(address2)
        self._precondition_str(state)
        self._precondition_str(city)
        self._precondition_str(country)
        self._precondition_str(zipcode)
        self._precondition_str(contact)
        self._precondition_str(phone)
        self._precondition_str(fax)
        self._precondition_str(email)
        self._precondition_str(url)
        self._precondition_str(notes)
        payload = {
            'name': name,
        }
        self._add_to_dict(payload, 'address', address)
        self._add_to_dict(payload, 'address2', address2)
        self._add_to_dict(payload, 'state', state)
        self._add_to_dict(payload, 'city', city)
        self._add_to_dict(payload, 'country', country)
        self._add_to_dict(payload, 'zip', zipcode)
        self._add_to_dict(payload, 'contact', contact)
        self._add_to_dict(payload, 'phone', phone)
        self._add_to_dict(payload, 'fax', fax)
        self._add_to_dict(payload, 'email', email)
        self._add_to_dict(payload, 'url', url)
        self._add_to_dict(payload, 'notes', notes)
        path = '/api/v1/suppliers'
        return self._post(path, payload)

    def delete_supplier(self, supplier_id):
        self._precondition_int(supplier_id)
        path = '/api/v1/suppliers/{}'.format(supplier_id)
        return self._delete(path, None)

    def get_suppliers(self):
        path = '/api/v1/suppliers'
        return self._get(path, None)

    def get_supplier_by_id(self, supplier_id):
        self._precondition_int(supplier_id)
        path = '/api/v1/suppliers/{}'.format(supplier_id)
        return self._get(path, None)

    def get_supplier_by_name(self, name):
        suppliers = self.get_suppliers()
        for supplier in suppliers['rows']:
            if supplier['name'] == name:
                return supplier
        return None

    def update_supplier(self, supplier_id, name, address=None, address2=None, state=None, city=None, country=None, zipcode=None, contact=None, phone=None, fax=None, email=None, url=None, notes=None):
        self._precondition_int(supplier_id)
        self._precondition_str(name)
        self._precondition_str(address)
        self._precondition_str(address2)
        self._precondition_str(state)
        self._precondition_str(city)
        self._precondition_str(country)
        self._precondition_str(zipcode)
        self._precondition_str(contact)
        self._precondition_str(phone)
        self._precondition_str(fax)
        self._precondition_str(email)
        self._precondition_str(url)
        self._precondition_str(notes)
        payload = {}
        self._add_to_dict(payload, 'name', name)
        self._add_to_dict(payload, 'address', address)
        self._add_to_dict(payload, 'address2', address2)
        self._add_to_dict(payload, 'state', state)
        self._add_to_dict(payload, 'city', city)
        self._add_to_dict(payload, 'country', country)
        self._add_to_dict(payload, 'zip', zipcode)
        self._add_to_dict(payload, 'contact', contact)
        self._add_to_dict(payload, 'phone', phone)
        self._add_to_dict(payload, 'fax', fax)
        self._add_to_dict(payload, 'email', email)
        self._add_to_dict(payload, 'url', url)
        self._add_to_dict(payload, 'notes', notes)
        path = '/api/v1/suppliers/{}'.format(supplier_id)
        return self._patch(path, payload)

