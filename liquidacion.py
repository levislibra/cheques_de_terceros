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

import cheques_de_terceros


class liquidacion(osv.Model):
    _name = 'liquidacion'
    _description = 'liquidacion de cheques'
    _columns =  {
        'id': fields.integer('Nro liquidacion'),
        'fecha_liquidacion': fields.date('Fecha liquidacion'),
        'active': fields.boolean('Activa', help="Cancelar liquidacion luego de validarla"),
        'cliente_id': fields.many2one('res.partner', 'Cliente'),
        'cheques_ids': fields.one2many('cheques.de.terceros', 'id', 'Cheques', ondelete='cascade'),


        'name': fields.char("Numero del cheque", size=8),
        'state': fields.selection([('cotizacion', 'Cotizacion'), ('confirmada', 'Confirmada')], string='Status', readonly=True, track_visibility='onchange'),
    }
    _defaults = {
    	'state': 'cotizacion',
    	#''

    }
    _sql_constraints = [
            ('id_uniq', 'unique (id)', "El Nro de liquidacion ya existe!"),
    ]
