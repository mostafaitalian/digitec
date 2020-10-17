from django.db import models

# Create your models here.
class MachineModel(models.Model):

    model_choices = (('5855', '5855'), ('5845', '5845'), ('5955', '5955'), ('5945', '5945'),
    ('5865', '5865'), ('5875', '5875'), ('7830', '7830'), ('7845', '7845'), ('7855', '7855'),
    ('7835', '7835'), ('7225', '7225'), ('7120', '7120'),
    ('c60', 'c60'), ('c70', 'c70'),
    ('560', '560'), ('550', '550'),
    ('j60', 'j60'),
    ('b7025', 'b7025'), ('b7030', 'b7030'), ('b7035', 'b7035'),
    ('5325', '5325'), ('5330', '5330'), ('5335', '5335'),
    ('5016', '5016'), ('5020', '5020'),
    ('5019', '5019'), ('5021', '5021'),
    ('5022', '5022'), ('5024', '5024'),
    ('5735', '5735'), ('5745', '5745'), ('5755', '5755'), ('5765', '5765'), ('5790', '5790'),
    ('5635', '5635'), ('5645', '5645'), ('5655', '5655'), ('5665', '5665'), ('5690', '5690'),
    ('3655', '3655'),
    ('3635', '3635'),
    ('3615', '3615'),
    ('8880', '8880'), ('8870', '8870'),
    ('5225', '5225'), ('5230', '5230'), ('5235', '5235'), ('5225A', '5225A'), ('5230A', '5230A'), ('5235A', '5235A'),
    ('4150', '4150'), ('4260', '4260'),
    ('b405', 'b405'), ('c405', 'c405'),
    ('c7025', 'c7025'), ('c7030', 'c7030'), ('c7035', 'c7035'),
    ('b8045', 'b8045'), ('b8055', 'b8055'),
    ('c8035', 'c8035'), ('c8045', 'c8045'), ('c8055', 'c8055'), ('c8065', 'c8065'), ('c8075', 'c8075'),
    ('180', '180'), ('2100', '2100'), ('3100', '3100'))
    name = models.CharField(max_length=5, choices=model_choices)
    neckname = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        if self.neckname:
            return self.name + ' ' + self.neckname
        else:
            return self.name
class SparePart(models.Model):
    part_no = models.CharField(max_length=9, unique=True)
    discription = models.CharField(max_length=255)
    machine_model = models.ManyToManyField(MachineModel, related_name='spareparts', null=True, blank=True)
    store_quantity = models.IntegerField(default=0)

    def  __str__(self):
        if self.machine_model:
            return self.part_no + ' ' + self.machine_model
        else:
            return self.part_no
