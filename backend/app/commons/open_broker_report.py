from  lxml import etree
from os import listdir,stat
from os.path import join

class open_broker_report:
    __slots__ ='file_path','root'
    def __init__(self,_file_dir,file_mask:str="_173364_"):  
        self.file_path=self.__get_last_report(_file_dir,file_mask)
        self.root=self.__load_xml(self.file_path).getroot()
    
    def __get_last_report(self,folder_name:str,file_mask:str):
        reports_list=[]
        for _file in listdir(folder_name):
            if _file[-3:]=='xml' and file_mask in _file:
                _file_path=join(folder_name,_file)
                reports_list.append((_file_path,stat(_file_path).st_mtime))
        return sorted(reports_list, key=lambda tup: tup[1])[-1][0]  
    
    def __load_xml(self,file_path:str):
        #parser = etree.XMLParser(encoding='cp1251')
        return etree.parse(file_path)
    
    def __children_to_dict(self,node_name:str,
                           d_keys:list=None,
                           print_uniq_keys:bool=False,
                          float_keys:list=[]):
        if print_uniq_keys:
            d_keys=None
            
        if d_keys is not None:  
            res={}
        else:
            res=[]
            
        for _el in self.root.find(node_name).getchildren():
            _d_el=dict(_el.items())
            _d_el_keys=_d_el.keys()
            for _f_key in float_keys:
                if _f_key in _d_el_keys:
                    _d_el[_f_key]=float(_d_el[_f_key])
            if d_keys is not None:
                _pop_items=[]
                for _k in d_keys[::-1]:
                    _p=_d_el.pop(_k) 
                    _pop_items.append(_p)
                _final_d={_pop_items[0]:_d_el}
                for _k in _pop_items[1:]:
                    _final_d={_k:_final_d}
                    
                upd_res=res
                for _p in _pop_items[::-1]:
                    if _p in  upd_res.keys():
                        upd_res=upd_res[_p]
                        _final_d=_final_d[_p]
                    else:
                        upd_res[_p]=_final_d[_p]
                        #print(res)
                        break
               
                #res.update(_final_d)
            else:
                res.append(_d_el) 
            
        if print_uniq_keys:
            return set().union(*[list(_el.keys()) for _el in res])
        
        return res
    
    def __json_report(self,report=False):
        res={}
        res['title_info']=self._extract_title_info()
        res['section_definition']=self._extract_section_definition(True,True) 
        
        res['spot_main_deals_conclusion']=self._extract_spot_main_deals_conclusion()
        res['spot_main_deals_executed']=self._extract_spot_main_deals_executed()

        res['spot_portfolio_security_params']=self._extract_spot_portfolio_security_params()
        
        if res['title_info']['agreement']['dgvr']=='Договор на ведение индивидуального инвестиционного счета: ':
            res['account_totally']=self._extract_spot_account_totally()
            res['unified_closing_assets']=self._extract_spot_preclosing_assets()
            res['closing_assets']=self._extract_spot_assets()       
            res['non_trade_money_operations']=self._extract_spot_non_trade_money_operations()       
            return res

        res['account_totally']=self._extract_unified_account_totally()
        res['guarantee_totally']=self._extract_unified_guarantee_totally()
        res['non_trade_money_operations']=self._extract_unified_non_trade_money_operations()        
        res['preclosing_assets']=self._extract_unified_preclosing_assets()
        res['closing_assets']=self._extract_unified_closing_assets()        
        res['spot_non_trade_security_operations']=self._extract_unified_spot_non_trade_security_operations()

        return res
    
    def json_report(self,full_report:bool=False):
        report=self.__json_report()
        if not full_report:
            non_trade_currency={}
            for _item in report['non_trade_money_operations']:
                if 'Поставлены на торги средства клиента' in _item['comment']:
                    _currency,_amount=_item['currency_code'],_item['amount']
                    try:
                        non_trade_currency[_currency]=non_trade_currency[_currency]+_amount
                    except:
                        non_trade_currency[_currency]=_amount
           

            cl_assets={}
            _filter_list=['asset_type',
                          'asset_name',
                          'closing_position_fact',
                          'period_change_position_fact',
                          'settlement_price',
                          'price_currency',
                          'settlement_fact_cb',
                          'asset_type_id','position_weight','settlement_fact',
                          'position_weight_cb']
            _sec_dict=report['spot_portfolio_security_params']
            flg1,flg2=False,False
            for key,_items in report['closing_assets'].items():
                f_d=dict(filter(lambda r: r[0] in _filter_list, _items.items()))
                if flg1==False and flg2==False:
                    if 'position_weight' in f_d.keys():
                        flg2=True
                    flg1=True
                if flg2:    
                    f_d['position_weight_cb'] = f_d.pop('position_weight')
                    f_d['settlement_fact_cb'] = f_d.pop('settlement_fact')
                try:
                    _info=_sec_dict[key]
                    f_d['isin']=_info['isin']
                    f_d['asset_name']=key
                    cl_assets[_info['ticker']]=f_d
                except:
                    cl_assets[key]=f_d
                    
            small_report={'period':report['title_info']['period'],
                          'assets_cb_value':report["account_totally"]["assets_cb_value_fact"],
                          'non_trade_currency':non_trade_currency ,
                          'assets':cl_assets
                            }                
    
            return small_report                  
        return report
            
    def _extract_title_info(self,print_raw:bool=False)->dict:
        title_dict=dict(self.root.items())
        if print_raw:
            return title_dict
        
        res={'board_list':list(map(str.strip,title_dict['board_list'].split(','))),
            'period':(title_dict['date_from'][:10],title_dict['date_to'][:10]),
             'cliend_id':{'client_code':title_dict['client_code'],
                          'micex_trade_code':title_dict['micex_trade_code']
                         },
             'agreement':{'agreement_number':title_dict['agreement_number'],
                          'agreement_date':title_dict['agreement_date'],'dgvr':title_dict['dgvr']
                         } ,

             'report_date':title_dict['build_date']
            }
        return res
    
    def _extract_section_definition(self,print_raw:bool=False,hide_empty:bool=False):
        res={}
        for _el in self.root.find('section_definition').getchildren():
            _d_el=dict(_el.items())
            if hide_empty:
                if not(list(_d_el.keys())==['name'] or _d_el=={}):
                    res[_el.tag]=_d_el
            else:
                res[_el.tag]=_d_el
                    
        if print_raw:
            return res
        return "no code written"
    
    def _extract_unified_account_totally(self,print_raw:bool=False):  
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['row_name','currency'],['value']
        _d=self.__children_to_dict('unified_account_totally',d_keys=d_keys,float_keys=float_keys)
        if print_raw:
            return _d
        _mapping={'Входящий остаток (факт)':'income_balance_fact',
                 'Вознаграждение Брокера за организацию доступа к биржевым торгам с предоставлением информации клиентам, необходимой для совершения операций и сделок':'broker_fee_for_info',
                 'Движение средств':'cashflow',
                 'Комиссия Брокера/Доп. комиссия Брокера "Сборы ТС" за заключение сделок':'broker_fee_for_deals',
                 'НКД':'ncd',
                 'Погашение НКД':'repayment_ncd',
                 'Погашение ЦБ':'repayment_cb',
                 'Сальдо расчётов по сделкам с ценными бумагами':'securities_deals_saldo',
                 'Исходящий остаток (факт)':'outcome_balance_fact',
                 'Оценка активов, по курсу ЦБ (факт)':'assets_cb_value_fact',
                 'Оценка активов, по курсу ЦБ (факт+план) (с учётом нерассчитанных сделок по ценным бумагам)':'assets_cb_value_fact_plan',
                 'Оценка активов, по Центральному курсу (факт) (Предварительное закрытие дня)':'assets_cb_value_fact_precloseday',
                 'Оценка активов, по Центральному курсу (факт+план) (с учётом нерассчитанных сделок по ценным бумагам)  (Предварительное закрытие дня)':'assets_cb_value_fact_plan_precloseday',
                 'Оценка активов, по Центральному курсу (факт) (Итоговое закрытие дня)':'assets_cb_value_fact_finalcloseday',
                 'Комиссия Брокера за заключение Специальных сделок РЕПО':'broker_repo_comission',
                 'Комиссия за сделки займа ЦБ на условиях Примерных условий сделок займа ценных бумаг':'broker_loan_securities_comission',
                 'Проценты по предоставленным займам ЦБ':'percents_cb_loans',


                 'Оценка активов, по Центральному курсу (факт+план) (с учётом нерассчитанных сделок по ценным бумагам)  (Итоговое закрытие дня)':'assets_cb_value_fact_plan_finalcloseday'
                 }

        return {_mapping[_key]:{**_item,**{'text_description':_key}} for _key,_item in _d.items()}
    
    def _extract_unified_guarantee_totally(self,print_raw:bool=False): 
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['active_go'],['amount','amount_plan','course','collateral','highly_liquid']

        _d=self.__children_to_dict('unified_guarantee_totally',float_keys=float_keys,d_keys=d_keys)
        if print_raw:
            return _d
        return _d
    
    def _extract_unified_preclosing_assets(self,print_raw:bool=False): 
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['asset_name'],['closing_position_fact',
                                             'closing_position_plan',
                                             'blocked_for_out',
                                             'settlement_price',
                                             'currency_course',
                                             'settlement_fact',
                                             'settlement_plan']

        _d=self.__children_to_dict('unified_preclosing_assets',float_keys=float_keys,d_keys=d_keys)
        if print_raw:
            return _d
        return _d   
    
    def _extract_unified_closing_assets(self,print_raw:bool=False): 
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['asset_name'],['opening_position_fact',
                                             'opening_position_plan',
                                             'period_change_position_fact',
                                             'period_change_position_plan',
                                             'closing_position_fact',
                                             'closing_position_plan',
                                             'blocked_for_out',
                                              'settlement_price',
                                              'currency_course_cb',
                                              'settlement_fact_cb',
                                              'settlement_plan_cb',
                                              'currency_course_ck',
                                              'settlement_fact_ck',
                                              'settlement_plan_ck',
                                              'position_weight_cb',
                                              'position_weight_ck'
                                             ]

        _d=self.__children_to_dict('unified_closing_assets',float_keys=float_keys,d_keys=d_keys)
        if print_raw:
            return _d
        return _d   
    
    def _extract_spot_main_deals_conclusion(self,print_raw:bool=False): 
        if print_raw:
            float_keys=[]
        else:
            float_keys=['buy_qnty',
                         'price',
                         'volume_currency',
                         'volume_rur',
                         'broker_commission'
                       ]

        _d=self.__children_to_dict('spot_main_deals_conclusion',float_keys=float_keys,d_keys=None)
        if print_raw:
            return _d
        return _d     
    def _extract_spot_main_deals_executed(self,print_raw:bool=False):       
        if print_raw:
            float_keys=[]
        else:
            float_keys=['buy_qnty',
                         'price',
                         'volume_currency_price',
                         'price_currency_rate',
                         'volume'
                       ]

        _d=self.__children_to_dict('spot_main_deals_executed',float_keys=float_keys,d_keys=None)
        if print_raw:
            return _d
        return _d           
    
    def _extract_unified_non_trade_money_operations(self,print_raw:bool=False): 
        if print_raw:
            float_keys=[]
        else:
            float_keys=['amount']
        _d=self.__children_to_dict('unified_non_trade_money_operations',float_keys=float_keys,d_keys=None)
        if print_raw:
            return _d
        return _d 
    
    def _extract_unified_spot_non_trade_security_operations(self,print_raw:bool=False): 
        if print_raw:
            float_keys=[]
        else:
            float_keys=['quantity']
        _d=self.__children_to_dict('spot_non_trade_security_operations',float_keys=float_keys,d_keys=None)
        if print_raw:
            return _d
        return _d   
    
    def _extract_spot_portfolio_security_params(self,print_raw:bool=False): 
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['security_name'],['nominal',
                                                 'lot_size',
                                                 'market_price'
                                                ]

        _d=self.__children_to_dict('spot_portfolio_security_params',float_keys=float_keys,d_keys=d_keys)
        if print_raw:
            return _d
        return _d 
    def _extract_spot_account_totally(self,print_raw:bool=False):  
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['row_name','currency'],['value']
        _d=self.__children_to_dict('spot_account_totally',d_keys=d_keys,float_keys=float_keys)
        if print_raw:
            return _d
        _mapping={'Входящий остаток (факт)':'income_balance_fact',
                 'Вознаграждение Брокера за организацию доступа к биржевым торгам с предоставлением информации клиентам, необходимой для совершения операций и сделок':'broker_fee_for_info',
                 'Движение средств':'cashflow',
                 'Комиссия Брокера/Доп. комиссия Брокера "Сборы ТС" за заключение сделок':'broker_fee_for_deals',
                 'НКД':'ncd',
                 'Погашение НКД':'repayment_ncd',
                 'Погашение ЦБ':'repayment_cb',
                 'Сальдо расчетов':'securities_deals_saldo',
                 'Исходящий остаток (факт)':'outcome_balance_fact',
                 #'Оценка активов, по курсу ЦБ (факт)':'assets_cb_value_fact',
                 'Оценка активов, по курсу ЦБ (факт+план) (с учётом нерассчитанных сделок по ценным бумагам)':'assets_cb_value_fact_plan',
                 'Оценка активов, по курсу ЦБ (факт) - Предварительное закрытие дня':'assets_cb_value_fact_precloseday',
                 'Оценка активов, по курсу ЦБ (факт+план) (с учётом не рассчитанных сделок) - Предварительное закрытие дня':'assets_cb_value_fact_plan_precloseday',
                 'Оценка активов, по курсу ЦБ (факт+план) (с учётом не рассчитанных сделок) - Итоговое закрытие дня':'assets_cb_value_fact_plan_finalfcloseday',
                 'Оценка активов, по курсу ЦБ (факт) - Итоговое закрытие дня':'assets_cb_value_fact',
                 'Комиссия Брокера за заключение Специальных сделок РЕПО':'broker_repo_comission',
                 'Комиссия за сделки займа ЦБ на условиях Примерных условий сделок займа ценных бумаг':'broker_loan_securities_comission',
                 'Проценты по предоставленным займам ЦБ':'percents_cb_loans',


                 'Оценка активов, по Центральному курсу (факт+план) (с учётом нерассчитанных сделок по ценным бумагам)  (Итоговое закрытие дня)':'assets_cb_value_fact_plan_finalcloseday'
                 }

        return {_mapping[_key]:{**_item,**{'text_description':_key}} for _key,_item in _d.items()}
    

    
    def _extract_spot_preclosing_assets(self,print_raw:bool=False): 
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['asset_name'],['opening_position_fact',
                                             'opening_position_plan',
                                             'period_change_position_fact',
                                             'period_change_position_plan',
                                             'closing_position_fact',
                                             'closing_position_plan',
                                             'blocked_for_out',
                                              'settlement_price',
                                              'currency_course_cb',
                                              'settlement_fact_cb',
                                              'settlement_plan_cb',
                                              'currency_course_ck',
                                              'settlement_fact_ck',
                                              'settlement_plan_ck',
                                              'position_weight_cb',
                                              'position_weight_ck'
                                             ]

        _d=self.__children_to_dict('spot_preclosing_assets',float_keys=float_keys,d_keys=d_keys)
        if print_raw:
            return _d
        return _d    
    
    def _extract_spot_assets(self,print_raw:bool=False): 
        if print_raw:
            d_keys,float_keys=None,[]
        else:
            d_keys,float_keys=['asset_name'],['opening_position_fact',
                                             'opening_position_plan',
                                             'period_change_position_fact',
                                             'period_change_position_plan',
                                             'closing_position_fact',
                                             'closing_position_plan',
                                             'blocked_for_out',
                                              'settlement_price',
                                              'currency_course_cb',
                                              'settlement_fact_cb',
                                              'settlement_plan_cb',
                                              'currency_course_ck',
                                              'settlement_fact_ck',
                                              'settlement_plan_ck',
                                              'position_weight_cb',
                                              'position_weight_ck'
                                             ]

        _d=self.__children_to_dict('spot_assets',float_keys=float_keys,d_keys=d_keys)
        if print_raw:
            return _d
        return _d       
    def _extract_spot_non_trade_money_operations(self,print_raw:bool=False): 
        if print_raw:
            float_keys=[]
        else:
            float_keys=['quantity','amount']
        _d=self.__children_to_dict('spot_non_trade_money_operations',float_keys=float_keys,d_keys=None)
        if print_raw:
            return _d
        return _d     