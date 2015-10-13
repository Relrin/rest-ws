# -*- coding: utf-8 -*-
"""
    Functions and constants, which can be used for work with User models.
"""
from aiorest_ws.db.utils import convert_db_row_to_dict


SQL_CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS aiorest_auth_user
    (id INTEGER PRIMARY KEY NOT NULL,
     username CHAR(255) NOT NULL,
     password CHAR(255) NOT NULL,
     last_name CHAR(255),
     first_name CHAR(255),
     is_active BOOL DEFAULT TRUE NOT NULL,
     is_superuser BOOL DEFAULT FALSE NOT NULL,
     is_staff BOOL DEFAULT FALSE NOT NULL,
     is_user BOOL DEFAULT TRUE NOT NULL
    );
"""
SQL_CREATE_TOKEN_FOREIGN_KEY = """
    ALTER TABLE aiorest_auth_token
    ADD COLUMN user_id INTEGER REFERENCES aiorest_auth_user(id);
"""
SQL_USER_ADD = """
    INSERT INTO aiorest_auth_user (`username`, `password`, `first_name`,
    `last_name`, `is_superuser`, `is_staff`, `is_user`, `is_active`)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""
SQL_USER_GET = """
    SELECT `username`, `password`, `first_name`, `last_name`, `is_superuser`,
    `is_staff`, `is_user`, `is_active`
    FROM aiorest_auth_user
    WHERE id=?;
"""
SQL_USER_GET_WITH_ID = """
    SELECT `id`, `username`, `password`, `first_name`, `last_name`,
    `is_superuser`, `is_staff`, `is_user`, `is_active`
    FROM aiorest_auth_user
    WHERE username=?;
"""
SQL_USER_GET_BY_USERNAME = """
    SELECT `username`, `password`, `first_name`, `last_name`, `is_superuser`,
    `is_staff`, `is_user`, `is_active`
    FROM aiorest_auth_user
    WHERE username=?;
"""
SQL_USER_UPDATE = """
    UPDATE aiorest_auth_user
    SET {}
    WHERE username=?;
"""
USER_MODEL_FIELDS = (
    'id', 'username', 'password', 'first_name', 'last_name', 'is_superuser',
    'is_staff', 'is_user', 'is_active'
)
USER_MODEL_FIELDS_WITHOUT_PK = (
    'username', 'password', 'first_name', 'last_name', 'is_superuser',
    'is_staff', 'is_user', 'is_active'
)


def construct_update_sql(**parameters):
    query_args = []
    update_field_template = "{}=? "
    updated_fields = ''
    for field, value in parameters.items():
        updated_fields += update_field_template.format(field)
        query_args.append(value)
    sql = SQL_USER_UPDATE.format(updated_fields)
    return sql, query_args


def convert_user_raw_data_to_dict(user_raw_data, with_id=False):
    if with_id:
        fields_tuple = USER_MODEL_FIELDS
    else:
        fields_tuple = USER_MODEL_FIELDS_WITHOUT_PK

    bool_fields = ('is_superuser', 'is_staff', 'is_user', 'is_active')
    user_data = convert_db_row_to_dict(user_raw_data, fields_tuple)
    for field in bool_fields:
        user_data[field] = bool(user_data[field])
    return user_data
