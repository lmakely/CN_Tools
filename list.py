import os


list = ["Anacapa", "Bard Estates", "Bruns Park", "Catalina Heights",
        "Coral Sea Cove", "San Miguel", "Santa Cruz", "Santa Rosa",
        "Sea Breeze Village", "Seal Beach"]

for i in list:
    newpath= "C://LMM//5088" + "//" + str(i)
    os.makedirs(newpath)
