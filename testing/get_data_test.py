import time

import minedata
from minedata.versions import Versions

version = Versions.PC_1_21_4
start = time.time()
data = minedata.get_data(version)
for key, value in data.items():
    print(f"{key}: {len(value)} items")
print(time.time() - start)