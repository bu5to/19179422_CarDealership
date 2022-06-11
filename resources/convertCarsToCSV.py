import csv

car_header = ['brand', 'model']

with open('carModels.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(car_header)
    f = open("brandsAndModels.txt", "r", encoding="utf-8")
    brands = []
    for line in f:
        splitLine = line.split(":")
        brandTemp = splitLine[0]
        brand = brandTemp.split("(")
        brand = brand[0]
        brand = brand[:-1]
        print(brand)
        modelsTemp = str(splitLine[1])
        models = modelsTemp.split(",")
        newModels = []
        for model in models:
            model = model[1:]
            model = model.replace("\n", "")
            newModels.append(model)
            car_row = [brand, model]
            writer.writerow(car_row)
        print(newModels)
