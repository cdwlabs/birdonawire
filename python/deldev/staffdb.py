from .deldevdb import DelDevDB
from common import logger
log = logger.get_mod_logger(__name__)

class StaffDB(DelDevDB):

    def init_table(self):
        self.table_name='staff'
        self.fields = [ 'name',  'active', 'user_id', 'employeeNumber',   'title',     'email', 'github_id' ]
        self.columns = { 'name':'w', 'active':'i'  }
        self.signature = [ 'user_id']

    def get_by_email(self, email, active=None):
        log.info(f"email={email}")
        sql = "select fkstaff from staff_email = '%s'" % ( email )
        sql = "select staff.* from staff join staff_email on staff_email.fkStaff = staff.id and staff_email.email = '%s' " % ( email )
        if not active == None:
            sql += " where staff.active = %d " % ( active )
        result = self.open_select(sql)
        rows = [ ]
        for row in result:
            rows.append(row)

        return rows
