import sys
print(sys.path)

import module1

#data_tojson = module1.generate_json_plots()
#with open("test.json", "w") as outfile:
#    outfile.write(data_tojson)

module1.update_data_from_server(data_type="provincial")
#module1.update_data_from_server(data_type="regional")
#module1.update_data_from_server(data_type="national")
module1.generate_json_plots()
