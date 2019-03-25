from database_config import table_names, table_fields, table_types, default_data
import database

def create(table_name):
    fields, types = table_fields[table_name], table_types[table_name]


    table = database.table(table_name, close_instantly=False)
    table.create(fields, types)
    table.send_query(f"ALTER TABLE {table_name} CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;")
    table.close()

def create_all():
    for table_name in table_names:
        create(table_name)

def delete(table_name):
    database.table(table_name).delete_table("yes")

def delete_all():
    for table_name in table_names:
        delete(table_name)

def write_default_data():
    for table_name, fields, values in default_data:
        database.table(table_name).insert(fields, values)


if __name__ == "__main__":
    database.table(create_database=True)
    delete_all()
     # delete_all() - really all ???
    create_all()
    write_default_data()