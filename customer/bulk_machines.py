from collections import OrderedDict
import xlrd
import json
import excel2json

from customer.models import Department
from engineer.models import Area
def create_bulk(customers):
    wb =xlrd.open_workbook("TA09.xls")
    sh = wb.sheet_by_index(0)

    data_list = []
    # for rownum in range(2, 10):
    #     row_values = sh.row_values(rownum)
    #     print(row_values(rownum))

    for rownum in range(8, sh.nrows-1):
        #print(sh)
    
        if(sh.row_values(rownum)[1] != ''):
            data =OrderedDict()
            fields = OrderedDict()
            row_values = sh.row_values(rownum)
            print(row_values, row_values[1])
            data['model'] = 'machine.machine'
            data['fields'] = fields
            if((row_values[1] != '')and ( row_values[1] != 'Machine Serial' and row_values[1].find('Toner') == -1)):
                fields['serial'] = int(row_values[1])
                fields['machine_serial'] = row_values[1]
            else:
                fields['serial'] = None
            if(row_values[4] != '' and row_values[4] != 'ProductModel'):
                fields['machine_model'] = row_values[4]
            else:
                fields['machine_model'] = 'no model'
            if(row_values[15]!='' and row_values[15]!="Machine Location"):
            
                fields['machine_location'] = row_values[15]
            else:
                fields['machine_location'] = 'no location'
            fields['installation_date'] = None
            fields['added'] = None
            # if row_values[6] != '':
            #     # fields['machine_points'] = row_values[6]
            #     pass
            # else:
            fields['machine_points'] = 1.0
            fields['machine_response_time']= None
            fields['machine_callback_time'] = None
            fields["begin_at"] = "08:00:00"
            fields["finish_at"] = "16:00:00"
            fields["first_week_dayoff"] = 7
            fields["second_week_dayoff"] = 7
            fields['machine_category'] = None
    
            if(row_values[6]!='' and row_values[6]!= 'Customer'):
                fields['customer'] = customers.get(customer_id=int(row_values[6])).id
            else:
                fields['customer'] = None
            fields['department'] =Department.objects.get(customer__id=customers.get(customer_id=int(row_values[6])).id).id
            fields['area'] = Area.objects.get(name='TA09').id
            fields['contract'] = None
            #data['Customer_name'] = row_values[7]
            if('serial' not in fields):
                break
            # if(fields['serial']==None):
            #     break
            data_list.append(data)
    return data_list
