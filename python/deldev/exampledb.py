from .deldevdb import DelDevDB

class ExampleDB(DelDevDB):

    def init_table(self):
        self.table_name='example'
        self.fields = [ 'name',  'description',   'category', 'fk_staff' ]
        self.columns = { 'name':'w', 'fk_staff':'i'  }
        self.signature = [ 'name']
