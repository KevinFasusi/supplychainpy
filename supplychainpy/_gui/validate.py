import socket as sc


def host(address: str) -> bool:
    address = str(address)
    try:
        sc.inet_aton(address)
        #print("address : {}".format(address))
        return True
    except sc.error:
        return False

def db_path(path: str) -> bool:
    pass

def port(port_num: int) -> bool:
    print("validating port")

    try:
        if int(port_num):
            #print("port present: {}".format(port_num))
            return True
    except ValueError as err:
            return False


def source_file(path: str)->bool:
    pass




