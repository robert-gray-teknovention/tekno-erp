from django.contrib.auth.models import User
from djblets.datagrid.grids import Column, DataGrid


class UserDataGrid(DataGrid):
    username = Column("Username", sortable=True)
    first_name = Column("First Name", sortable=True)
    last_name = Column("Last Name", sortable=True)

    def __init__(self, request):
        DataGrid.__init__(self, request, User.objects.filter(is_active=True), "Users")
        self.default_sort = ['username']
        self.default_columns = ['username', 'first_name', 'last_name']
