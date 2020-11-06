import excel2json
import xlrd
from collections import OrderedDict
import json


if __name__ == "__main__":
    excel2json.convert_from_file('Mostafa1.xls')
    wb =xlrd.open_workbook("Mostafa.xls")
    sh = wb.sheet_by_index(0)
    #print(wb._sheet_names,wb.xf_list)
    data_list = []
    fdata_list = []
    
    for rownum in range(7, sh.nrows):
        fdata_list.append(sh.row_values(rownum)[6])
    print(fdata_list)
    a=set(fdata_list)
    fffdata_list= list(a)
    fffdata_list.remove((''))
    print(fffdata_list, len(fffdata_list))
    ffdata_list = []
    for d in fdata_list:
        #print(fdata_list.index(d), max(loc for loc, val in enumerate(fdata_list) if val==d))
        if(fdata_list.index(d)== max(loc for loc, val in enumerate(fdata_list) if val==d)):
            ffdata_list.append(d)
    #print(ffdata_list)



    for rownum in range(7, sh.nrows):
        #print(sh.row_values(rownum))
        if sh.row_values(rownum)[6] in fffdata_list:
            fffdata_list.remove(sh.row_values(rownum)[6])
            if(sh.row_values(rownum)[7]!=''):

                data =OrderedDict()
                fields = OrderedDict()
                row_values = sh.row_values(rownum)
                #print(row_values)
                data['model'] = 'customer.customer'
                data['fields'] = fields
                if(row_values[7] != '' and row_values[7] != 'Customer'):
                    fields['name'] = row_values[7].rstrip('\r\n')
                fields["location"] = "no location"
                fields["address_site"] = "http://www.google.com"
                if(row_values[6]!='' and row_values[6]!='Customer'):
                    fields["customer_id"] = int(row_values[6])
                else:
                    fields["customer_id"] = None
                fields["telephone"] = 1
                fields["begin_at"] = "08:00:00"
                fields["finish_at"] = "16:00:00"
                fields["first_week_dayoff"] = 6
                fields["second_week_dayoff"] = 7
                fields["engineers"]: []

        # if((row_values[1] != '')and ( row_values[1] != 'Machine Serial' and row_values[1].find('Toner') == -1)):
        #     fields['serial'] = int(row_values[1])
        # else:
        #     fields['serial2'] = None
        # if(row_values[4] != '' and row_values[4] != 'ProductModel'):
        #     fields['machine_model'] = row_values[4]
        # else:
        #     fields['machine_model'] = 'no model'
        # if(row_values[15]!='' and row_values[15]!="Machine Location"):

        #     fields['Machine_location'] = row_values[15]
        # else:
        #     fields['Machine_location'] = 'no location'
        # fields['installation_date'] = None
        # fields['added'] = None
        # fields['machine_points'] = 1.0
        # fields['machine_response_time']= None
        # fields['machine_callback_time'] = None
        # fields["begin_at"] = "08:00:00"
        # fields["finish_at"] = "16:00:00"
        # fields["first_week_dayoff"] = 7
        # fields["second_week_dayoff"] = 7
        # fields['machine_category'] = None

        # if(row_values[6]!='' and row_values[6]!= 'Customer'):
        #     fields['customer_id'] = int(row_values[6])
        # else:
        #     fields['customer_id'] = None
        # fields['department'] =None
        # fields['area'] = None
        # fields['contract'] = None
        #data['Customer_name'] = row_values[7]

                data_list.append(data)
        # sdata_list = [dict(t) for t in {tuple(d.items()) for d in data_list}]
    with open('final_customer5.json', 'w', encoding='utf-8') as writeJsonfile:
        json.dump(data_list, writeJsonfile, indent=4, ensure_ascii=False)