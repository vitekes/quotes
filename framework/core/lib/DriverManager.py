from selenium import webdriver

class DriverManager:
    instance = None

    class DriverManagerHelper:

        def __call__(self, *args, **kw) :
            if DriverManager.instance is None :
                object = DriverManager()
                DriverManager.instance = object

            return DriverManager.instance

    getInstance = DriverManagerHelper()

    def __init__(self) :
        if DriverManager.instance:
            raise RuntimeError, 'Only one instance of DriverManager is allowed!'

        self.driver = webdriver.Firefox()
        #Continiue initialization...


