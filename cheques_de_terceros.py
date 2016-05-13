# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

#from openerp.osv import osv, orm
#from datetime import time, datetime
#from openerp.tools.translate import _
#from openerp import models, fields

import pytz
import re
import time
import openerp
import openerp.service.report
import uuid
import collections
import babel.dates
from werkzeug.exceptions import BadRequest
from datetime import datetime, timedelta
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from openerp import api
from openerp import tools, SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _
from openerp.http import request
from operator import itemgetter
from openerp.exceptions import UserError

class entidad_bancaria(osv.Model):
	_name = 'entidad.bancaria'
	_description = 'Entidad bancaria'
	_columns = {
		'name': fields.char("Nombre", size=256, required=True),
		'codigo': fields.char("Codigo", size=8),
	}

	_sql_constraints = [
            ('name_uniq', 'unique (name)', "El Nombre ya existe!"),
    ]


class firmante(osv.Model):
	_name = 'firmante'
	_description = 'Firmante del cheque'
	_columns = {
		'name': fields.char("Nombre", size=30, required=True),
		'cuit': fields.char("Cuit", size=20, required=True),
	}

	_sql_constraints = [
            ('cuit_uniq', 'unique (cuit)', "El Cuit ya existe!"),
    ]

class cheques_de_terceros(osv.Model):
    _name = 'cheques.de.terceros'
    _description = 'Objeto cheque'
    _columns =  {
        'name': fields.char("Numero del cheque", size=8, required=True),
        'firmante_id': fields.many2one('firmante', 'Firmante', required=True),
        'banco_id': fields.many2one('entidad.bancaria', 'Banco', required=True),
        'importe': fields.float('Importe'),
        'fecha_vencimiento': fields.date('Fecha de vencimiento'),
        'fecha_deposito': fields.date('Fecha de deposito'),
        'boleta_deposito': fields.text('Boleta de deposito'),
        'fecha_acreditacion_contable': fields.date('Fecha de acreditacion'),
        'state': fields.selection([('draft', 'Cotizacion'), ('en_cartera', 'En cartera'), ('depositado', 'Depositado'), ('rechazado', 'Rechazado')], string='Status', readonly=True, track_visibility='onchange'),
        'cuenta_destino_en_cartera': fields.many2one('account.account', 'Cartera'),
        'cuenta_destino_depositado': fields.many2one('account.account', 'Depositado en'),
        'cuenta_destino_rechazado': fields.many2one('res.partner', 'Rechazado a'),
        'id': fields.many2one('liquidacion', 'Liquidacion id'),

    }
    _defaults = {
    	'state': 'draft',
    	#''
    }