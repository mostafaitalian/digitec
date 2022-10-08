from . import models
from import_export import resources

class MachineResource(resources.ModelResource):

    class Meta:
        model = models.Machine

class CallResource(resources.ModelResource):

    class Meta:
        model = models.Call

class ReportResource(resources.ModelResource):

    class Meta:
        model = models.Report
class ContractResource(resources.ModelResource):

    class Meta:
        model = models.Contract
