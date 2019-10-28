#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def parseargs(cmdline=sys.argv[1:], known_args_only=False):
    import argparse
    import datetime
    p = argparse.ArgumentParser()
    p.add_argument('-d', '--database', type=str, required=True, help='The SQLite database')
    p.set_defaults(func=verify_tables)
    sp = p.add_subparsers(help='Commands')

    #-- argument to create schema
    sp_create = sp.add_parser('create', help='Create the required schema')
    sp_create.set_defaults(func=create_schema)

    #-- argument to verify schema
    sp_verify = sp.add_parser('verify', help='Verify if the required tables exist is correct')
    sp_verify.set_defaults(func=verify_tables)

    #-- argument to dump table contents
    sp_dumptbl = sp.add_parser('dump-table', help='Dump table contents')
    sp_dumptbl.add_argument('table', choices='users projects bookings'.split(),
                            help='Dump contents of this table')
    sp_dumptbl.add_argument('-f', '--format', choices='txt csv json'.split(),
                            default='txt', help='the data format of the output')
    sp_dumptbl.add_argument('-H', '--headers', action='store_true',
                            help='Show headers')
    sp_dumptbl.set_defaults(func=dump_table)

    #-- arguments to add a user record
    sp_user = sp.add_parser('add-user', help='Add user record')
    sp_user.add_argument('-f', '--first-name', help='First name of the new user')
    sp_user.add_argument('-s', '--surname', help='Surname of the new user')
    sp_user.add_argument('-e', '--email', help='Email address of the new user')
    sp_user.set_defaults(func=add_new_user)

    #-- arguments to add a project record
    sp_project = sp.add_parser('add-project', help='Add project record')
    sp_project.add_argument('-n', '--name', help='Project name')
    sp_project.set_defaults(func=add_new_project)

    #-- arguments to add a booking record
    sp_booking = sp.add_parser('add-booking', help='Add booking record')
    # user;project;date;hours;remarks
    sp_booking.add_argument('-u', '--user', type=int,
                            help='User ID')
    sp_booking.add_argument('-p', '--project', type=int,
                            help='Project ID')
    # a conversion function for str -> datetime.date
    conv = lambda d: datetime.date( *map(int, d.split('-')) )
    sp_booking.add_argument('-d', '--date', type=conv,
                            default=datetime.date.today(),
                            help='The date of the booking (ISO format 2019-01-20)')
    sp_booking.add_argument('-H', '--hours', type=float, default=8,
                            help='The date of the booking')
    sp_booking.add_argument('-r', '--remarks', default='',
                            help='A custom remark for this booking')
    sp_booking.set_defaults(func=add_new_booking)

    args = p.parse_args(cmdline)          # parse all args!

    return args

def dbconnect(args):
    import sqlite3
    try:
        conn = sqlite3.connect(database=args.database)
    except sqlite3.OperationalError:
        print('Unable to open SQLite database: {}'.format(args.database))
        sys.exit(10)
    except TypeError:
        print('')
        sys.exit(12)
    return conn

def sql_exec(conn, sql, sql_args=()):
    cur = conn.cursor()
    cur.execute(sql, sql_args)
    conn.commit()
    return tuple(cur), cur.lastrowid

def create_schema(conn, args):
    sql = '''
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS projects;
    DROP TABLE IF EXISTS bookings;

    CREATE TABLE users (
            id integer PRIMARY KEY AUTOINCREMENT,
            fname varchar(40),
            sname varchar(60),
            email varchar(255)
    );

    CREATE TABLE projects (
            id integer PRIMARY KEY AUTOINCREMENT,
            name varchar(140)
    );

    CREATE TABLE bookings (
            id integer PRIMARY KEY AUTOINCREMENT,
            user integer,
            project integer,
            date datetime,
            hours numerical,
            remarks varchar,
            FOREIGN KEY (user) REFERENCES users (id),
            FOREIGN KEY (project) REFERENCES users (id)
    );
    '''
    if not input('Are you sure to delete all existing data? [y/N] '
            ).lower() in 'y yes'.split():
        print('Exiting...')
        sys.exit(0)
    cur = conn.cursor()
    res = cur.executescript(sql)

def dump_table(conn, args):
    queries = dict(
        users=( 'select * from users;', 'id fname sname email'.split() ),
        projects=( 'select * from projects;', 'id project_name'.split() ),
        bookings=( '''
        SELECT b.id, b.user, u.fname, u.sname, b.project, p.name, 
               b.date, b.hours, b.remarks
        FROM bookings as b,
             users as u,
             projects as p
        WHERE
            b.user = u.id AND
            b.project = p.id
        ''',
        '''booking_id user_id user_fname user_sname project_id project_name
        booking_date booking_hours booking_remarks'''.split()),
    )
    sql, headers = queries.get(args.table)
    res = sql_exec(conn, sql)
    records = res[0]
    if args.headers:
        # headers = [ row[1] for row in schema[args.table] ]
        records = ((tuple(headers), ) + records)
    if args.format == 'txt':
        import csv
        w = csv.writer(sys.stdout, delimiter=' ')
        w.writerows(records)
    elif args.format == 'csv':
        import csv
        w = csv.writer(sys.stdout, delimiter=';')
        w.writerows(records)

def verify_tables(conn, args):
    tables = 'users projects bookings'.split()
    schema = {}
    for table in tables:
        res = tuple( sql_exec(conn, 'PRAGMA table_info({})'.format(table)) )
        if res[0]:
            schema[table] = tuple(res[0])
        else:
            raise Exception('Table "{}" is missing, schema is invalid'
                            .format(table))
    if args.func == 'verify_tables':
        print('Tables verified: OK')
    return schema

def add_new_user(conn, args):
    sql = '''
    INSERT INTO users (fname, sname, email)
    VALUES (?, ?, ?);
    '''
    res = sql_exec(conn, sql, (args.first_name, args.surname, args.email))
    print('New user added, id={}'.format(res[1]))

def add_new_project(conn, args):
    sql = '''
    INSERT INTO projects (name)
    VALUES (?);
    '''
    res = sql_exec(conn, sql, (args.name,))
    print('New project added, id={}'.format(res[1]))

def add_new_booking(conn, args):
    sql = '''
    INSERT INTO bookings (user, project, date, hours, remarks)
    VALUES (?, ?, ?, ?, ?);
    '''
    res = sql_exec(conn, sql, (args.user, args.project, args.date, args.hours, args.remarks))
    print('New booking added, id={}'.format(res[1]))


if __name__ == '__main__':
    arguments = parseargs()            # the CLI arguments provided by user
    connection = dbconnect(arguments)  # connect to specified SQLite DB
    if arguments.func != create_schema:
        schema = verify_tables(connection, arguments)    # verify the tables
    arguments.func(connection, arguments)   # invoke the requested function

