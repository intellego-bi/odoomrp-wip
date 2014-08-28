# -*- encoding: utf-8 -*-
##############################################################################
#                                                                            #
#  OpenERP, Open Source Management Solution.                                 #
#                                                                            #
#  @author Carlos Sánchez Cifuentes <csanchez@grupovermon.com>               #
#                                                                            #
#  This program is free software: you can redistribute it and/or modify      #
#  it under the terms of the GNU Affero General Public License as            #
#  published by the Free Software Foundation, either version 3 of the        #
#  License, or (at your option) any later version.                           #
#                                                                            #
#  This program is distributed in the hope that it will be useful,           #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              #
#  GNU Affero General Public License for more details.                       #
#                                                                            #
#  You should have received a copy of the GNU Affero General Public License  #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.      #
#                                                                            #
##############################################################################

from openerp import api, exceptions, models, _


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    @api.one
    def onchange_product(self):
        purchase_order = self.env['purchase.order']
        order_obj = purchase_order.browse(self.order_id)
        product_product = self.env['product.product']
        product_obj = product_product.browse(self.product_id)
        purchase_homologation = self.env['purchase.homologation']
        homologation_obj = purchase_homologation.search([
            ('partner_id', '=', order_obj.partner_id.id),
            ('category_id', '=', product_obj.product_tmpl_id.categ_id.id),
            ('start_date', '<', self.date_planned),
            ('end_date', '>', self.date_planned)])
        if homologation_obj is False:
            raise exceptions.Warning(
                _('Error!'),
                _("This product isn't homologate for the supplier selected."))
