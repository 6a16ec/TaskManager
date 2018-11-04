import mysql.connector as mariadb
import config

class Table:
    def __init__(self, name):
        self.mariadb_connection = mariadb.connect(user = config.username, password = config.password, database = config.database_name)
        self.cursor = self.mariadb_connection.cursor(buffered=True)

        self.table_name = name

    def create(self, columns, types):

        columns_with_type = []
        for i in range(len(columns)):
            columns_with_type.append(columns[i] + " " + types[i])

        columns_with_types_string = ", ".join(columns_with_type);
        print(columns_with_types_string)

        query = """CREATE TABLE"""
        query += """ """ + """IF NOT EXISTS"""
        query += """ """ + """`""" + self.table_name + """`"""
        query += """ """ + """(""" + columns_with_types_string + """)"""

        self.cursor.execute(query)
        self.mariadb_connection.commit()


    def insert(self, parameters, values):

        if (type(parameters) is not list): parameters = [parameters]
        if (type(values) is not list): values = [values]

        for i in range(len(values)):
            if(type(values[i]) is not str): values[i] = str(values[i])
            values[i] = "'" + values[i] + "'";

        parameters_string = ", ".join(parameters)
        values_string = ", ".join(values)

        query = """INSERT INTO"""
        query += """ """ + """`""" + self.table_name + """`"""
        query += """ """ + """(""" + parameters_string + """)"""
        query += """ """ + """VALUES"""
        query += """ """ + """(""" + values_string + """)"""

        print(query)

        self.cursor.execute(query)
        self.mariadb_connection.commit()


    def update(self, key_parameters, key_values, changing_parameters, changing_values):
        if (type(key_parameters) is not list): key_parameters = [key_parameters]
        if (type(key_values) is not list): key_values = [key_values]
        if (type(changing_parameters) is not list): changing_parameters = [changing_parameters]
        if (type(changing_values) is not list): changing_values = [changing_values]

        for i in range(len(key_values)):
            if(type(key_values[i]) is not str): key_values[i] = str(key_values[i])
        for i in range(len(changing_values)):
            if(type(changing_values[i]) is not str): changing_values[i] = str(changing_values[i])

        key_parameter_value_array = []
        for parameter, value in zip(key_parameters, key_values):
            key_parameter_value_array.append(parameter + " = " + "'" + value + "'")
        key_parameter_value_string = " and ".join(key_parameter_value_array)

        changing_parameter_value_array = []
        for parameter, value in zip(changing_parameters, changing_values):
            changing_parameter_value_array.append(parameter + " = " + "'" + value + "'")
        changing_parameter_value_string = ", ".join(changing_parameter_value_array)

        query = """UPDATE"""
        query += """ """ + """`""" + self.table_name + """`"""
        query += """ """ + """SET"""
        query += """ """ + changing_parameter_value_string
        query += """ """ + """WHERE"""
        query += """ """ + key_parameter_value_string

        print(query)

        self.cursor.execute(query)
        self.mariadb_connection.commit()


    def select(self, selected_parameters, key_parameters, key_values):
        if (type(selected_parameters) is not list): selected_parameters = [selected_parameters]
        if (type(key_parameters) is not list): key_parameters = [key_parameters]
        if (type(key_values) is not list): key_values = [key_values]


        for i in range(len(key_values)):
            if (type(key_values[i]) is not str): key_values[i] = str(key_values[i])

        selected_parameters_string = ", ".join(selected_parameters)
        key_parameter_value_array = []
        for parameter, value in zip(key_parameters, key_values):
            key_parameter_value_array.append(parameter + " = " + "'" + value + "'")
        key_parameter_value_string = " and ".join(key_parameter_value_array)

        query = """SELECT"""
        query += """ """ + selected_parameters_string
        query += """ """ + """FROM"""
        query += """ """ + """`""" + self.table_name + """`"""
        query += """ """ + """WHERE"""
        query += """ """ + key_parameter_value_string

        print(query)

        self.cursor.execute(query)
        self.mariadb_connection.commit()
        return self.cursor.fetchall()

    def delete(self, key_parameters, key_values):
        if (type(key_parameters) is not list): key_parameters = [key_parameters]
        if (type(key_values) is not list): key_values = [key_values]

        for i in range(len(key_values)):
            if (type(key_values[i]) is not str): key_values[i] = str(key_values[i])

        key_parameter_value_array = []
        for parameter, value in zip(key_parameters, key_values):
            key_parameter_value_array.append(parameter + " = " + "'" + value + "'")
        key_parameter_value_string = " and ".join(key_parameter_value_array)

        query = """DELETE FROM"""
        query += """ """ + """`""" + self.table_name + """`"""
        query += """ """ + """WHERE"""
        query += """ """ + key_parameter_value_string

        print(query)

        self.cursor.execute(query)
        self.mariadb_connection.commit()

    def close(self):
        self.cursor.close()
        self.mariadb_connection.close()




def example():
    test = Table("test");
    test.create(["id", "id_vk", "name", "message"], ["int(5) PRIMARY KEY AUTO_INCREMENT", "INT(15)", "VARCHAR(100)", "VARCHAR(4096)"])

    test.insert("id_vk", 12345)
    test.insert(["id_vk", "name", "message"], [777777, "Nikita", "Hi, how are you"])
    print(test.select("*", "id", 1))
    print(test.select("*", "id", 2))

    test.update("id", "1", "name", "Nikita")
    test.insert(["id_vk", "name"], [123234, "Nikita"])
    print(test.select("*", "name", "Nikita"))

    test.delete("id", 1)
    print(test.select("*", "name", "Nikita"))

    test.close()




if(__name__ == "__main__"): example()