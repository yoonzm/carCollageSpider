import leancloud
# yoon
# leancloud.init("Guv8NmYGL7M0xjass3x4Afzi-gzGzoHsz", "zbmTkdFb5AIGLvSeWUc3O72W")
# cc
leancloud.init("PoEFEdhonbMbSMhFOtbqXmvJ-gzGzoHsz", "QyRhWm4N0W0UOfalewKC3Kns")


def save_car_brand(model):
    CarBrand = leancloud.Object.extend('CarBrand')
    car_brand = CarBrand()
    car_brand.set('autoHomeId', model['autoHomeId'])
    car_brand.set('brandFirstWord', model['brandFirstWord'])
    car_brand.set('brandName', model['brandName'])
    car_brand.set('brandLogo', model['brandLogo'])
    car_brand.save()
    return car_brand


def update_car_brand(model):
    CarBrand = leancloud.Object.extend('CarBrand')
    car_brand = CarBrand.create_without_data(model['objectId'])
    car_brand.set('sellTypeCount', model['sellTypeCount'])
    car_brand.set('allTypeCount', model['allTypeCount'])
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


def save_car_model(model):
    CarModel = leancloud.Object.extend('CarModel')
    car_model = CarModel()
    car_model.set('autoHomeId', model['autoHomeId'])
    car_model.set('brandId', model['brandId'])
    car_model.set('typeId', model['typeId'])
    car_model.set('category', model['category'])
    car_model.set('name', model['name'])
    car_model.set('guidePrice', model['guidePrice'])
    car_model.set('realityPrice', model['realityPrice'])
    car_model.save()
    return car_model


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

        CarModel = leancloud.Object.extend('CarModel')
        query_CarModel = leancloud.Query(CarModel)
        query_CarModel.limit(1000)
        all_CarModel = query_CarModel.find()
        leancloud.Object.destroy_all(all_CarModel)
