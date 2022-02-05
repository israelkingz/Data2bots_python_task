import json
import os

def get_type(data):
    if type(data) is str:
        return "STRING"
    elif type(data) is int:
        return "INTEGER"
    elif type(data) is float:
        return "NUMBER"
    elif type(data) is bool:
        return "BOOLEAN"
    elif type(data) is dict:
        return "OBJECT"
    elif type(data) is list:
        if len(data) == 0: return "ENUM" #assume 0 length list is an enum
        if type(data[0]) is str:
            return "ENUM"
        elif type(data[0]) is dict:
            return "ARRAY"

def generate_schema(file_name):
        
    with open(f"data/{file_name}.json", "r") as file:
        data = file.read()

    json_data = json.loads(data)["message"]

    new_data = {}

    def get_object(data):
        return_data = {}

        for key in data.keys():
            key_type = get_type(data[key])

            return_data[key] = {
                "type": key_type,
                "tag": "",
                "description": ""
            }

            if key_type == "OBJECT":
                return_data[key]["properties"] = get_object(data[key])
                return_data[key]["required"] = [k for k in data[key].keys()]
            elif key_type == "ARRAY":
                return_data[key]["items"] = get_object(data[key][0])
                return_data[key]["required"] = [k for k in data[key][0].keys()]

        return return_data

    new_data = get_object(json_data)

    with open(f"schemas/{file_name}_output.json", "w") as output:
        json.dump(new_data, output, indent=4)

if __name__ == "__main__":
    for file in os.listdir(path = "data"):
        file_name = os.path.splitext(file)[0]
        generate_schema(file_name)