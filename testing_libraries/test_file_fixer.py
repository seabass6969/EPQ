import re

file_name = "ssss___dance_of_the_sugar_plum_fairy.ogg"
subbed = re.sub(r"(\..*)", '.wav', file_name)
print(subbed)
