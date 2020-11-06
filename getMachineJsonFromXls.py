import excel2json
import xlrd
from collections import OrderedDict
import json
# from customer.models import Customer


if __name__ == "__main__":
    excel2json.convert_from_file('Mostafa1.xls')
    wb =xlrd.open_workbook("Mostafa.xls")
    sh = wb.sheet_by_index(0)
    #print(wb._sheet_names)
    data_list = []
    # for rownum in range(2, 10):
    #     row_values = sh.row_values(rownum)
    #     print(row_values(rownum))

    for rownum in range(7, sh.nrows):
        #print(sh)
    
        if(sh.row_values(rownum)[1] != ''):
            data =OrderedDict()
            fields = OrderedDict()
            row_values = sh.row_values(rownum)
            print(row_values)
            data['model'] = 'machine.machine'
            data['fields'] = fields
            if((row_values[1] != '')and ( row_values[1] != 'Machine Serial' and row_values[1].find('Toner') == -1)):
                fields['serial'] = int(row_values[1])
            else:
                fields['serial'] = None
            if(row_values[4] != '' and row_values[4] != 'ProductModel'):
                fields['machine_model'] = row_values[4]
            else:
                fields['machine_model'] = 'no model'
            if(row_values[15]!='' and row_values[15]!="Machine Location"):
            
                fields['Machine_location'] = row_values[15]
            else:
                fields['Machine_location'] = 'no location'
            fields['installation_date'] = None
            fields['added'] = None
            fields['machine_points'] = 1.0
            fields['machine_response_time']= None
            fields['machine_callback_time'] = None
            fields["begin_at"] = "08:00:00"
            fields["finish_at"] = "16:00:00"
            fields["first_week_dayoff"] = 7
            fields["second_week_dayoff"] = 7
            fields['machine_category'] = None
    
            if(row_values[6]!='' and row_values[6]!= 'Customer'):
                fields['customer_id'] = int(row_values[6])
            else:
                fields['customer_id'] = None
            fields['department'] =None
            fields['area'] = None
            fields['contract'] = None
            #data['Customer_name'] = row_values[7]
            if('serial' not in fields):
                break
            # if(fields['serial']==None):
            #     break
            data_list.append(data)
        
    # da = json.loads(json.dumps(data_list,indent=4, ensure_ascii=False))
    # print(da)
    # daa = [item['fields'] for item in da]
    # print(daa[:5])
with open('final_machines1json', 'w', encoding='utf-8') as writeJsonfile:
    json.dump(data_list, writeJsonfile, indent=4, ensure_ascii=False)