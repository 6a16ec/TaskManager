table_names, tables, table_fields, table_types = [], {}, {}, {}
add_table, default_data = [], []

# # # # #
add_table.append([
    "tasks",
    [
        "id",
        "user_tid",
        "name",
        "type",
        "duration"
    ],
    [
        "INT(12) PRIMARY KEY AUTO_INCREMENT",
        "INT(12)",
        "CHAR(128)",
        "INT(1)",
        "INT(6)"
    ]
])
add_table.append([
    "constants",
    [
        "name",
        "string"
    ],
    [
        "CHAR(32) PRIMARY KEY",
        "CHAR(128)"
    ]
])

add_table.append([
    "orthoepy",
    [
        "id",
        "word", "syllable",
        "description", "part_of_speech"
    ],
    [
        "INT(4) PRIMARY KEY AUTO_INCREMENT",
        "CHAR(32)", "INT(2)",
        "CHAR(128)", "CHAR(32)"
    ]
])


# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #
    # --- # --- # --- # --- # --- # --- # --- # --- #
# --- # --- # --- # --- # --- # --- # --- # --- # --- # --- #


# default_data.append(["items", ["category_id", "subcategory_id", "count", "name"], [3, 7, 7, "Лисички"]])
default_data.append(["constants", ["name", "string"], ["create_task", "Введите название"]])



for name, fields, types in add_table:
    table_names.append(name)
    tables[name] = name
    table_fields[name] = fields
    table_types[name] = types