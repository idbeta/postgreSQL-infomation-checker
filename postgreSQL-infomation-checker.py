#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,string,time,datetime,csv,xlwt
import psycopg2,json

def cur_file_dir():
    return os.path.split(os.path.realpath(__file__))[0]
def check_pg_1(pgip):
    try:
        pg = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname='skylar')
        cursor = pg.cursor()
        print u"[The pg_stat_activity]\r"
        sql_row = cursor.execute('''SELECT a.attname as name FROM pg_class as c,pg_attribute as a  where c.relname = 'pg_stat_activity' and a.attrelid = c.oid and a.attnum>0''')
        keys = cursor.fetchall()
        wb = xlwt.Workbook(encoding='utf-8')
        style0 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour red, pattern_back_colour red')
        ws = wb.add_sheet(u'pg_stat_activity')  
        for i in range(len(keys)):
            ws.write(0,i,keys[i][0],style0)
        sql_data = cursor.execute('''select * from pg_stat_activity''')
        data = cursor.fetchall()
        for ii in range(len(data)):
            for d in range(len(data[ii])):
                ws.write(1+ii,d,str(data[ii][d]))
                if len(str(data[ii][d])) <251:
                    ws.col(d).width = 256 * (len(str(data[ii][d]))+5) 
                else:
                    ws.col(d).width = 65535
        wb.save(u'The_pg_stat_activity_%s.xls'%int(time.time()))
    except Exception, info:
        print str(info)            
    finally:
        cursor.close()
        pg.close()
def check_pg_2(pgip):
    try:
        pg = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname='skylar')
        cursor = pg.cursor()
        print u"[The pg_stat_database]\r" 
        sql_row = cursor.execute('''SELECT a.attname as name FROM pg_class as c,pg_attribute as a  where c.relname = 'pg_stat_database' and a.attrelid = c.oid and a.attnum>0''')
        keys = cursor.fetchall()
        wb = xlwt.Workbook(encoding='utf-8')
        style0 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour red, pattern_back_colour red')
        ws = wb.add_sheet(u'pg_stat_database')  
        for i in range(len(keys)):
            ws.write(0,i,keys[i][0],style0)
        sql = cursor.execute('''SELECT datname FROM pg_database''')
        datname = cursor.fetchall()
        line=0
        for i in datname:            
            if i[0].startswith('template')==False and i[0] !='postgres' :
                line=line+1
                sql = cursor.execute('''select * from pg_stat_database where datname = '%s';'''%i[0])
                data = cursor.fetchall()
                for d in range(len(data[0])):  
                    ws.write(line,d,str(data[0][d]))
                    if len(str(data[0][d])) <251:
                        ws.col(d).width = 256 * (len(str(data[0][d]))+5) 
                    else:
                        ws.col(d).width = 65535
        wb.save(u'The_pg_stat_database_%s.xls'%int(time.time()))
    except Exception, info:
        print str(info)            
    finally:
        cursor.close()
        pg.close()
def check_pg_3(pgip):
    try:
        pg = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname='skylar')
        cursor = pg.cursor()
        print u"[每张表的统计信息]\r"
        sql = cursor.execute('''SELECT datname FROM pg_database''')
        datname = cursor.fetchall()        
        for i in datname:            
            if i[0].startswith('template')==False and i[0] !='postgres' :
                tables =['pg_stat_user_indexes','pg_stat_user_tables','pg_statio_user_indexes','pg_statio_user_tables','pg_statio_user_sequences']
                pg_t = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname=i[0])
                cursor_t = pg_t.cursor()                
                wb = xlwt.Workbook(encoding='utf-8')
                for t in tables:
                    sql_row = cursor_t.execute('''SELECT a.attname as name FROM pg_class as c,pg_attribute as a  where c.relname = '%s' and a.attrelid = c.oid and a.attnum>0'''%t)
                    keys = cursor_t.fetchall()                    
                    style0 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour red, pattern_back_colour red')
                    ws = wb.add_sheet(t)
                    for k in range(len(keys)):
                        ws.write(0,k,keys[k][0],style0)                    
                    sql = cursor_t.execute('''select * from %s order by relname;'''%t)
                    data = cursor_t.fetchall()
                    for ii in range(len(data)):
                        for d in range(len(data[ii])):
                            ws.write(1+ii,d,str(data[ii][d]))
                            if len(str(data[ii][d])) <241:
                                ws.col(d).width = 256 * (len(str(data[ii][d]))+15) 
                            else:
                                ws.col(d).width = 65535
                wb.save('%s_%s.xls'%(i[0],int(time.time())))    
                cursor_t.close()
                pg_t.close()
    except Exception, info:
        print str(info)            
    finally:
        cursor_t.close()
        pg_t.close()
        cursor.close()
        pg.close()
def check_pg_4(pgip):
    try:
        pg = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname='skylar')
        cursor = pg.cursor()        
        print u"[Table Size Information]\r"
        sql = cursor.execute('''SELECT datname FROM pg_database''')
        datname = cursor.fetchall()
        wb = xlwt.Workbook(encoding='utf-8')
        for i in datname:
            if i[0].startswith('template')==False and i[0] !='postgres' :
                pg_t = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname=i[0])
                cursor_t = pg_t.cursor()
                row=['oid','table_schema','TABLE_NAME','row_estimate','total_bytes','index_bytes','toast_bytes','table_bytes','total','INDEX','toast','TABLE']                
                style0 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour red, pattern_back_colour red')
                ws = wb.add_sheet(i[0])
                for k in range(len(row)):            
                    ws.write(0,k,row[k],style0)           
                sql_data = cursor_t.execute('''SELECT *, pg_size_pretty(total_bytes) AS total
            , pg_size_pretty(index_bytes) AS INDEX
            , pg_size_pretty(toast_bytes) AS toast
            , pg_size_pretty(table_bytes) AS TABLE
          FROM (
          SELECT *, total_bytes-index_bytes-COALESCE(toast_bytes,0) AS table_bytes FROM (
              SELECT c.oid
                      ,nspname AS table_schema
                  , relname AS TABLE_NAME
                      , c.reltuples AS row_estimate
                      , pg_total_relation_size(c.oid) AS total_bytes
                      , pg_indexes_size(c.oid) AS index_bytes
                      , pg_total_relation_size(reltoastrelid) AS toast_bytes
                  FROM pg_class c
                  LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
                  WHERE relkind = 'r'
          ) a
        ) b
        where b.table_schema='public' order by table_bytes desc;
        ''')
                data = cursor_t.fetchall()
                for ii in range(len(data)):
                    for d in range(len(data[ii])):
                        ws.write(1+ii,d,str(data[ii][d]))
                        if len(str(data[ii][d])) <241:
                            ws.col(d).width = 256 * (len(str(data[ii][d]))+15) 
                        else:
                            ws.col(d).width = 65535
                cursor_t.close() 
                pg_t.close()
        wb.save('Table_Size_Information_%s.xls'%(int(time.time())))
    except Exception, info:
        print str(info)            
    finally:
        cursor.close()
        pg.close()
def check_pg_5(pgip):
    try:
        pg = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname='skylar')
        cursor = pg.cursor()        
        print u"[The largest databases]\r"
        row=['Name','Owner','SIZE']
        wb = xlwt.Workbook(encoding='utf-8')
        style0 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour red, pattern_back_colour red')
        ws = wb.add_sheet(u'sheet1')
        for k in range(len(row)):            
            ws.write(0,k,row[k],style0) 
        sql_data = cursor.execute('''SELECT d.datname AS Name,  pg_catalog.pg_get_userbyid(d.datdba) AS Owner,
    CASE WHEN pg_catalog.has_database_privilege(d.datname, 'CONNECT')
        THEN pg_catalog.pg_size_pretty(pg_catalog.pg_database_size(d.datname))
        ELSE 'No Access'
    END AS SIZE
FROM pg_catalog.pg_database d
    where d.datname <>'template0' and d.datname <>'template1'
    ORDER BY
    CASE WHEN pg_catalog.has_database_privilege(d.datname, 'CONNECT')
        THEN pg_catalog.pg_database_size(d.datname)
        ELSE NULL
    END DESC -- nulls first
    LIMIT 20
''')
        data = cursor.fetchall()
        for ii in range(len(data)):
            for d in range(len(data[ii])):
                ws.write(1+ii,d,str(data[ii][d]))
                if len(str(data[ii][d])) <241:
                    ws.col(d).width = 256 * (len(str(data[ii][d]))+15) 
                else:
                    ws.col(d).width = 65535
        wb.save('The_largest_databases_%s.xls'%int(time.time())) 
    except Exception, info:
        print str(info)            
    finally:
        cursor.close()
        pg.close()
def check_pg_6(pgip):
    try:
        pg = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname='skylar')
        cursor = pg.cursor()        
        print u"[The size of your biggest relations]\r"
        sql = cursor.execute('''SELECT datname FROM pg_database''')
        datname = cursor.fetchall()
        wb = xlwt.Workbook(encoding='utf-8')
        for i in datname:
            if i[0].startswith('template')==False and i[0] !='postgres' :
                pg_t = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname=i[0])
                cursor_t = pg_t.cursor()
                row=['relation','size']                
                style0 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour red, pattern_back_colour red')
                ws = wb.add_sheet(i[0])
                for k in range(len(row)):            
                    ws.write(0,k,row[k],style0) 
                sql_data = cursor_t.execute('''SELECT nspname || '.' || relname AS "relation",
            pg_size_pretty(pg_relation_size(C.oid)) AS "size"
          FROM pg_class C
          LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
          WHERE nspname NOT IN ('pg_catalog', 'information_schema')
          ORDER BY pg_relation_size(C.oid) DESC
          LIMIT 20;
        ''')
                data = cursor_t.fetchall()
                for ii in range(len(data)):
                    for d in range(len(data[ii])):
                        ws.write(1+ii,d,str(data[ii][d]))
                        if len(str(data[ii][d])) <241:
                            ws.col(d).width = 256 * (len(str(data[ii][d]))+15) 
                        else:
                            ws.col(d).width = 65535
                cursor_t.close()
                pg_t.close()            
        wb.save('The_size_of_your_biggest_relations_%s.xls'%(int(time.time())))                
    except Exception, info:
        print str(info)            
    finally:
        cursor.close()
        pg.close()
def check_pg_7(pgip):
    try:
        pg = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname='skylar')
        cursor = pg.cursor()        
        print u"[The total size of your biggest tables]\r"
        sql = cursor.execute('''SELECT datname FROM pg_database''')
        datname = cursor.fetchall()
        wb = xlwt.Workbook(encoding='utf-8')
        for i in datname:
            if i[0].startswith('template')==False and i[0] !='postgres' :
                pg_t = psycopg2.connect(host=pgip.split(':')[0],port=str(pgip.split(':')[1]), user='postgres',password='postgres',dbname=i[0])
                cursor_t = pg_t.cursor()
                row=['relation','total_size']                
                style0 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour red, pattern_back_colour red')
                ws = wb.add_sheet(i[0])
                for k in range(len(row)):            
                    ws.write(0,k,row[k],style0) 
                sql_data = cursor_t.execute('''SELECT nspname || '.' || relname AS "relation",
            pg_size_pretty(pg_total_relation_size(C.oid)) AS "total_size"
          FROM pg_class C
          LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
          WHERE nspname NOT IN ('pg_catalog', 'information_schema')
            AND C.relkind <> 'i'
            AND nspname !~ '^pg_toast'
          ORDER BY pg_total_relation_size(C.oid) DESC
          LIMIT 20;
        ''')
                data = cursor_t.fetchall()
                for ii in range(len(data)):
                    for d in range(len(data[ii])):
                        ws.write(1+ii,d,str(data[ii][d]))
                        if len(str(data[ii][d])) <241:
                            ws.col(d).width = 256 * (len(str(data[ii][d]))+15) 
                        else:
                            ws.col(d).width = 65535
                cursor_t.close()
                pg_t.close()
        wb.save('The_total_size_of_your_biggest_tables_%s.xls'%int(time.time()))
    except Exception, info:
        print str(info)            
    finally:
        cursor.close()
        pg.close()        
def check_pg(pgip,option):
    os.chdir(cur_file_dir())
    if int(option)==1:
        check_pg_1(pgip)
    elif int(option)==2:
        check_pg_2(pgip) 
    elif int(option)==3:
        check_pg_3(pgip) 
    elif int(option)==4:
        check_pg_4(pgip)
    elif int(option)==5:
        check_pg_5(pgip) 
    elif int(option)==6:
        check_pg_6(pgip) 
    elif int(option)==7:
        check_pg_7(pgip)    
    elif int(option)==0:
        check_pg_1(pgip)
        check_pg_2(pgip) 
        check_pg_3(pgip) 
        check_pg_4(pgip)
        check_pg_5(pgip)
        check_pg_6(pgip)
        check_pg_7(pgip)
    else:
        print 'the second option only can be 0-7 !'

if __name__ == "__main__":
    check_pg(sys.argv[1],sys.argv[2])