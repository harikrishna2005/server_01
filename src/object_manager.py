
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
@singleton
class ServerRepository:
    def __init__(self):
        self.server_list = []

    def get_binance(self, account_id:str, production_environment: bool):
        BINANCE = "binance"
        print(f"Binance Object created for account id: {account_id}  in Prod Env : {production_environment}")


    # def get_binance_object():





server_objects = ServerRepository()

if __name__ == '__main__':
    singleton_object1 = ServerRepository()
    singleton_object2 = ServerRepository()
    print(singleton_object1 is singleton_object2)

