
class Decorator1():

    def cleanDataRam(self,func):
        def wrapper(*args):
            r = func(*args).split('Go, ')[1].replace(' Go RAM', '')
            return r
        return wrapper

    def cleanDataStorage(self,func):
        def wrapper(*args):
            r = func(*args).split('Go, ')[0]
            return r
        return wrapper

    def cleanDataPixelPhotos(self,func):
        def wrapper(*args):
            r = func(*args).split(' ')[0]
            return r
        return wrapper

    def cleanDataScreenSize(self,func):
        def wrapper(*args):
            r = func(*args).replace('pouces', '').replace(',', '.')
            return r
        return wrapper

    def cleanDataDimensions(self,func):
        def wrapper(*args):
            r = func(*args).replace("mm","")
            return r
        return wrapper

    def cleanDataWeight(self,func):
        def wrapper(*args):
            r = func(*args).replace('grammes', '')
            return r
        return wrapper

    def cleanDataPrice(self,func):
        def wrapper(*args):
            r = func(*args).split('€')[0]
            return r
        return wrapper

class Decorator2():

    def cleanDataRam(self,func):
        def wrapper(*args):
            r = func(*args).split(' ')[0]
            return r
        return wrapper

    def cleanDataStorage(self,func):
        def wrapper(*args):
            r = func(*args).split(' ')[0]
            return r
        return wrapper

    def cleanDataPixelPhotos(self,func):
        def wrapper(*args):
            r = func(*args).split(' ')[0]
            return r
        return wrapper

    def cleanDataBrand(self,func):
        def wrapper(*args):
            r = func(*args).strip()
            return r
        return wrapper

    def cleanDataScreenSize(self,func):
        def wrapper(*args):
            r = func(*args).replace('"','')
            return r
        return wrapper

    def cleanDataDimensions(self,func):
        def wrapper(*args):
            r = func(*args).replace('mm','').replace('•','x').replace('.',',')
            return r
        return wrapper

    def cleanDataWeight(self,func):
        def wrapper(*args):
            r = func(*args).replace('g', '')
            return r
        return wrapper