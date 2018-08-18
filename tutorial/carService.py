import leancloud

leancloud.init("Guv8NmYGL7M0xjass3x4Afzi-gzGzoHsz", "zbmTkdFb5AIGLvSeWUc3O72W")


def save_car_brand(model):
    CarBrand = leancloud.Object.extend('CarBrand')
    car_brand = CarBrand()
    car_brand.set('autoHomeId', model['autoHomeId'])
    car_brand.set('brandFirstWord', model['brandFirstWord'])
    car_brand.set('brandName', model['brandName'])
    car_brand.set('brandLogo', model['brandLogo'])
    car_brand.save()
    return car_brand


def save_car_type(model):
    CarType = leancloud.Object.extend('CarType')
    car_type = CarType()
    car_type.set('autoHomeId', model['autoHomeId'])
    car_type.set('brandId', model['brandId'])
    car_type.set('brandName', model['brandName'])
    car_type.set('typeName', model['typeName'])
    car_type.set('name', model['name'])
    car_type.set('maxPrice', model['maxPrice'])
    car_type.set('minPrice', model['minPrice'])
    car_type.set('image', model['image'])
    car_type.set('stopPro', model['stopPro'])
    car_type.save()
    return car_type


def delete_all():
    CarBrand = leancloud.Object.extend('CarBrand')
    query_CarBrand = leancloud.Query(CarBrand)
    query_CarBrand.limit(1000)
    all_CarBrand = query_CarBrand.find()
    leancloud.Object.destroy_all(all_CarBrand)

    for index in range(10):
        CarType = leancloud.Object.extend('CarType')
        query_CarType = leancloud.Query(CarType)
        query_CarType.limit(1000)
        all_CarType = query_CarType.find()
        leancloud.Object.destroy_all(all_CarType)

