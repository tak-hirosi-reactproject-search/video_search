from search_app.models import * 

print("==== Start ====")

# Create person
print("===== Create Mainclass Type ====")
try:
    labels_mainclass_type(name="person").save()
    print("Create person : "+ str(labels_mainclass_type.objects.all()))
except Exception as ex:
    print("Pass person : " + str(ex))

# Create labels_attributes_type
print("===== Create Attributes Type ====")
attr_type_list = ['top_type', 'top_color', 'bottom_type', 'bottom_color']

for attr_type in attr_type_list:
    try:
        labels_attributes_type(mainclass_id=1, type=attr_type).save()
        print(f"Create {attr_type} : "+ str(labels_attributes_type.objects.get(type=attr_type).type))
    except Exception as ex:
        print(f'Pass {attr_type} : ' + str(ex))


# Create labels_attributes_type
print("===== Create Attributes ====")
attributes_set = [
    ["long_sleeve", "short_sleeve", "sleeveless", "onepiece"] ,
    ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "grey", "black"],
    ["long_pants", "short_pants", "skirt"],
    ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "grey", "black"],
]

for attr_type_id, attr_list in enumerate(attributes_set):
    print(f"===== Create Attribute Tpye [{attr_type_id+1}] ====")
    for idx, attr in enumerate(attr_list):
        try:
            labels_attributes(type_id=attr_type_id+1, index=idx, name=attr).save()
            print(f"Create type_id({attr_type_id+1}) name({attr}) : " + str(labels_attributes.objects.get(type_id=attr_type_id+1, name=attr).name))
        except Exception as ex:
            print(f"Pass idx({idx}) name({attr}) : " + str(ex))
            
print("==== END ====")
        
        