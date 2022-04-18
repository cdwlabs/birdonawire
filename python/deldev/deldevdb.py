"""
Class to provide access to a MySQL table.

see: http://pymysql.readthedocs.io/en/latest/

Usage:

* in script
  from deldevdb import DelDevDB

  dbh = DelDevDB()

  sql = dbh.build_select_query( { 'name': 'value'})

  result = dbh.open_select(sql)

  for row in result:
      print("got row")

* in module

    see: exampledb.py



"""

import pymysql.cursors
import sys

from pathlib import Path
import os
import re
from dotenv import load_dotenv

from common import logger
log = logger.get_mod_logger(__name__)

class DBConfig:
    is_ready = False
    #q_pattern = re.compile('[]')
    def __init__(self,env_file='deldev_db.env'):
        if self.is_ready:
            return

        self.env_file = None
        self.set_env_file(env_file)

        try:
            load_dotenv(self.env_file, verbose=True)

            self.host=os.getenv('host', 'localhost')
            self.user=os.getenv('user')
            self.password=os.getenv('password')
            self.port=os.getenv('port',3306)
            self.db_name=os.getenv('database', 'deldev')
            self.is_ready = True
        except Exception as err:
            log.error("config file {} failed: {}".format( env_file, err))

    def set_env_file(self,env_file):
        #log.debug(f"try {env_file}")
        f = Path(env_file)
        if f.is_file():
            self.env_file = f
            return

        pp = os.getenv('PYTHONPATH', '')
        if pp:
            ppp = Path(pp)
            f = ppp / env_file
            #log.debug(f"try {f}")
            if f.is_file():
                self.env_file = f
                return

        log.error(f"no env file {env_file}")


class DelDevDB:
    dbh = None
    #cfg = DBConfig()
    cfg = DBConfig(env_file='deldev_db.env')

    def __init__(self,f=None):

        self.init_table()
        self.select_query = None

        if not self.cfg.is_ready:
            raise Exception("not ready")

        self.open()
        return

    def init_table(self):
        """sub class should over-ride this"""
        self.table_name = None
        self.fields = [ ]

        #
        # map field name to type
        # where type is one of
        #   x i
        #
        self.columns = {}


    def open(self):
        if self.dbh:
            return
        log.debug( f"connect to {self.cfg.db_name} as {self.cfg.user}" )
        try:
            self.dbh = pymysql.connect(
                host=self.cfg.host,
                user=self.cfg.user,
                password=self.cfg.password ,
                port=self.cfg.port,
                db=self.cfg.db_name,
                #charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
                )
        except Exception as err:
            raise Exception("connect failed: {}".format(err) )
            return

    def close(self):
        self.dbh.close()

    def get(self, id):
        """get a single row by rowID """
        sql = 'select * from %s where id = %s ' % ( self.table_name, id)
        return self.select_one(sql)

    def select_one(self, sql=None, args={}):

        if not sql:
            if not args:
                log.error("ERROR no args or sql")
                return
            sql = self.build_select_query(args)

        results = self.open_select(sql)
        n = 0
        for row in results:
            n += 1

        if n == 1:
            return row
        return None

        try:
            cursor = self.dbh.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            return result

        except Exception as err:
            log.error( "select failed, err=%s \n  query=%s" % (str(err), sql) )
            return

    def build_select_query(self, data):

        if not self.table_name:
            log.error("no table name")
            return

        self.select_query = None
        sql = 'select * from %s ' % ( self.table_name )

        wh = self.select_clause( data)
        if wh:
            sql += ' where %s ' % (  wh)
        if 'order' in data:
            # TODO verify value is of the form
            #   [ F ]
            #   and is of the form
            #   field
            #   field DESC
            #
            o = ",".join( data['order'])
            sql += " order by " + o
            #log.debug("q=%s" % sql)

        self.select_query = sql
        return sql

    def select_clause(self, data, prepare_query=False):
        """ build a where clause for a SQL select statement
        data is a dict of column-name -> value
        where value can have the following syntax:
        !VALUE
        NULL    - match using the IS NULL or IS NOT NULL operator
        <VALUE  - match using the less than operator
        >VALUE  - match using the greater than operator

        if the operator is not determined by the syntax above,
        the default operator is 'like';
        unless the column-name is in the coluns attribute
        and has the value 'i'

        columns (option)
          field => <type>

          where <type> is one of
            x exact (no wildcard )
            i integer
            d date -
            s string / allows

        """

        wh = ''
        for f in self.fields:
            if not f in data:
                continue
            if data[f] == None:
                continue

            if not wh == '':
                wh +=  ' AND '

            # TODO: sanitize data
            #   escape quotes
            # all values must be str
            neg = False
            op = None
            ftype = 's'
            if f in self.columns:
                ftype = self.columns[f]

            val = str(data[f])
            # TODO check if int
            #log.debug(f"val={data[f]} len={len(val)}"  )
            # if typee in 's' and
            #log.debug(f'{f} - type={ftype} value={data[f]}')
            if not ftype == 'i' and data[f][0] == '!':
                neg = True
                data[f] = data[f][1:]

            if data[f] == 'NULL':
                op = 'IS'
                if neg:
                    op = 'IS NOT'
                wh += "%s %s NULL " % ( f, op )
                continue

            # TODO: support >= <=
            if not ftype == 'i':
                if data[f][0] == '<' or data[f][0] == '>':
                    op = data[f][0]
                    data[f] = data[f][1:]

            if ftype == 'i' :
                if not op:
                    op = '='
                    if neg:
                        op = '!='
                # convert to int?
                wh += '%s %s %s' % ( f, op, data[f ])
            elif ftype == 'd':
                pass
                # date type not handled
            elif prepare_query:
                if not op:
                    op = 'like'
                    if neg:
                        op = 'not like'
                wh += '%s %s %s' % ( f, op, data[f ])

            else:
                # ftype == 's', 'x'
                if not op:
                    op = 'like'
                    if neg:
                        op = 'not like'
                wh += '%s %s "%s"' % ( f, op, data[f ])

        if 'id' in data:
            if not wh == '':
                wh +=  ' AND '
            wh += 'id = %s' % (  data['id'])

        return wh

    def open_select(self,sql=None, args={}):
        if args:
            sql = self.build_select_query(args)
            #log.info(f"got sql={sql} args={args}")

        if not sql:
            sql = self.select_query

        if not sql:
            return
        cursor = None
        try:
            #log.debug("open cursor")
            cursor = self.dbh.cursor()
            #log.debug("execute " + sql )
            # Create a new record
            cursor.execute(sql)
        except Exception as err:
            #return "open failed: " + str(err)
            log.error("open failed: " + str(err) )
            return

        while(1):
            row = cursor.fetchone()
            if not row:
                return
            #print(f'row={row} ')
            yield row



    # https://pynative.com/python-mysql-execute-parameterized-query-using-prepared-statement/

    def execute_prepared(self, values=[]):
        """NOT IMPLEMENTED"""
        pass

    def prepare_select(self, cols):
        """NOT IMPLEMENTED"""
        data = {}
        for col in cols:
            data[col] = '%'
        if not data:
            log.error("no valid query")
            return

        query = self.select_clause(data, True)
        query = "select * from %s where %s" % ( self.table_name, query)


    def update_item(self,item):
        sql = self.build_update_query(item)
        #print(f"query={sql} ")
        cursor = self.dbh.cursor( )
        if not cursor:
            raise Exception('no cursor')
        rv = cursor.execute(sql)
        #return
        self.dbh.commit()
        return rv

    def build_update_query(self, item):
        clause = ''
        # calling program is responsible for making sure
        #  all values are of type 'string'

        # self.build_update_quer()
        if not 'id' in item:
            raise Exception("no ID field ")

        for f in self.fields:
            if f in item:
                if item[f] == None:
                    continue

                if clause:
                    clause += ', '

                #print("set {} = {}".format(f, item[f]))
                if f in self.columns and self.columns[f] == 'i':
                    val = item[f]
                else:
                    ###val = self.s_pattern.sub('.', item[f])
                    # TODO: sanitize string
                    # escape quotes
                    val = item[f]
                    s = re.sub(r"'", "\\'", val )
                    val = "'%s'" % val
                clause += " %s = %s " % ( f, val)

        if clause == '':
            raise Exception("no valid fields")

        sql =  "UPDATE `%s` set %s where id = %s " % ( self.table_name, clause, item['id'] )
        #log.debug("sql=%s" % sql )
        return sql

    def add_item(self, item ):
        #print( "add item: p=", item['project'] )
        self.open()

        flist = ''
        vlist  = ''
        # calling program is responsible for making sure
        #  all values are of type 'string'
        for f in self.fields:
            if f in item:
                if item[f] == None:
                    continue

                if flist:
                    flist += ', '
                    vlist += ', '
                flist += "`"  + f + "`"
                vlist += "'" + item[f] + "'"

        #raise Exception("got here")
        if flist == '':
            raise Exception("no valid fields")
            #print( "ERROR: no valid fields" )
            #return

        #sql = "INSERT INTO `{application_usage}`  (" + flist + ") VALUES ( " + vlist + ") "
        sql = f"INSERT INTO `{self.table_name}`  ( {flist} ) VALUES ( {vlist}) "
        #cursor = self.dbh.cursor( dictionary=True)
        cursor = self.dbh.cursor( )
        if not cursor:
            raise Exception('no cursor')
        cursor.execute(sql)
        #return
        self.dbh.commit()
        id = cursor.lastrowid
        self.close
        return id

    def count_column(self, col):
        """ return the number of occurrences of the values
        in a specified column"""

        self.open()
        n = 0

        # set:
        #  fields, col_name, select_field
        if type(col) is list:
            #print( "list", col )
            for c in col:
                if not c in self.fields:
                    raise Exception("invalid column " + c)
                    return
            fields = ', '.join(col)
            col_name =  '_'.join(col)

            x = '," ",'.join( col )
            select_field = 'concat(' + x + ') as ' + col_name


        else:
            ###print( col,"type", type(col) )
            if not col in self.fields:
                raise Exception("invalid column " + col)
                return
            fields = col
            select_field = col
            col_name = col

        #sql = "select count(*) as num, " + select_field + " from application_usage "
        sql = f"select count(*) as num, {select_field}  from {self.table_name} "

        sql += " group by " + fields
        sql += " order by count(*) DESC "
        #print("sql=" + sql )

        clist = []
        try:
            cursor = self.dbh.cursor()
            cursor.execute(sql)
            while True:
                result = cursor.fetchone()
                if not result:
                    break
                n += 1
                #print("{} r={}".format( n, result ))

                clist.append( { 'name': result[col_name], 'count': result['num']})
        except Exception as err:
            #return "count failed: " + str(err)
            log.error( "count failed: " + str(err) )
            return

        return clist

    def count(self, args=None):
        self.open()
        n = 0
        sql = f"select count(*) as num from {self.table_name} "
        try:
            cursor = self.dbh.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            #print( "got results, type", type(result) )
        except Exception as err:
            return "count failed: " + str(err)
            return

        return result['num']

    def date_range(self):
        self.open()
        sql = f"select min(date) as date_min, max(date) as date_max from {self.table_name}"
        try:
            cursor = self.dbh.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            #print( "got results, type", type(result) )
        except Exception as err:
            return "select failed: " + str(err)

        return result

    def open_cursor(self,sql=None):
        if not sql:
            sql = self.select_query

        try:
            self.select_cursor = self.dbh.cursor()
            # Create a new record
            self.select_cursor.execute(sql)
            return True
        except Exception as err:
            #return "open failed: " + str(err)
            log.error("ERROR open failed: " + str(err) )

        return False

    def next_row(self):
        result = self.select_cursor.fetchone()
        return result

    def dump_csv(dump_file='db.csv', max_id=None):
        log.warning( "TODO" )


    def crud(self, sql):
        self.open()
        cursor = self.dbh.cursor( )
        if not cursor:
            raise Exception('no cursor')
        cursor.execute(sql)
        #return
        self.dbh.commit()
        id = cursor.lastrowid
        self.close
        return id
