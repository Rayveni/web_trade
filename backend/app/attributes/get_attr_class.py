#mosex_sec_history
def gen_attr_class(attr_list):
    ind="    "
    print("class foo:")
    attr_list=list(map(str,attr_list))
    print(ind+"__slots__={}".format(','.join(list(map(lambda s:"'{}'".format(s),attr_list)))))
    print(ind+"def __init__(self,{}):".format(','.join(attr_list)))
    ind+=ind
    for attr in attr_list:
        print(ind+"self.{0}={1}".format(attr,attr))