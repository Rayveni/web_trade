class index_info:
    __slots__ ='id','type','bloomberg','reuters','isin','index_type','number','calc_time','calc_period','begin_date','update_index','security_limit','duration'
    def __init__(self,id,type,bloomberg,reuters,isin,index_type,number,calc_time,
                 calc_period,begin_date,update_index,security_limit,duration):
        self.id=id
        self.type=type
        self.bloomberg=bloomberg
        self.reuters=reuters
        self.isin=isin
        self.index_type=index_type
        self.number=number
        self.calc_time=calc_time
        self.calc_period=calc_period
        self.begin_date=begin_date
        self.update_index=update_index
        self.security_limit=security_limit
        self.duration=duration