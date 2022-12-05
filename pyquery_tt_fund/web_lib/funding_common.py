import re
import sys
import time 
import logging
import json
import pandas as pd
from collections import OrderedDict

sys.path.append('E:\python_progams\web_crawler')
from web_lib.crawler_common import *
from web_sup.funding import *
from fund_lib.fund_common import cal_sharpe_ratio

funding_obj_list = []
replace_words_list = ['chars', 'datas', 'count', 'record', 'pages', 'curpage', 'indexsy', 'showday']
drop_cols = ['SDATE', 'ACTUALSYI', 'NAVTYPE', 'FHFCZ', 'FHFCBZ', 'DTYPE', 'FHSP']
download_path = "E:\python_progams\web_crawler\\fund_data"
fund_analyze_path= "E:\python_progams\web_crawler\\fund_analyze"
sharpe_ratio_cols = ['unit_year_sharpe_ratio', 'accumulative_year_sharpe_ratio']
sharpe_ratio_redline = [-1, -0.5, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 3]

class Dailyfund(Crawler):
    def __init__(self):
        super().__init__()
        self.date_range = [] # date range for searching
        self.funding_list = OrderedDict() # funding_name: funding code...
    
    # return all funding net worth get links, and name
    def find_fund_info(self):
        _tmp = self.web_content.text
        for word in replace_words_list:
            _tmp = _tmp.replace(word, '"'+word+'"')
        _ind = _tmp.index(',"count":')
        _funding_list = json.loads(_tmp[7:_ind]+'}')
        for _fund in _funding_list['datas']:
            self.funding_list[_fund[1]] = _fund[0]
            
    # post date range for funding net worth get links
    # return funding obj with all necessary attrs
    def get_proper_fund_page(self):
        pass
    
    # involve this method into above
    def create_fund_obj(self):
        if not self.date_range:
            for key, value in self.funding_list.items():
                f = Fund()
                try:
                    f.init_fund_obj(url=fund_networth_url,
                                    headers=fund_headers,
                                    fund_name=key,
                                    fund_code=value,
                                    date_range=self.date_range,
                                    # download_path=download_path,
                                    # fund_analyze_path=fund_analyze_path,
                                    )
                    f.process_fund()
                    f.export_fund_excel()
                except:
                    print('something wrong with fund {}, {}'.format(key, value))
                    pass
            
class Fund(Crawler):
    def __init__(self):
        super().__init__()
        self.fund_name = None 
        self.fund_code = None # 007178
        self.tradable_period = 254
        self.drop_cols = drop_cols
        self.sharpe_ratio_cols = sharpe_ratio_cols
        self.page_index = 1
        self.page_size = 9999
        self.date_range = [] # date range for searching
        self.net_worth = []
        self.download_path = download_path
        self.download_file_path = None
        self.accumulative_net_worth = []
        self.daily_gain_rate = []
        # self.columns = ['date_range', 'net_worth', 'accumulative_net_worth', 'daily_gain_rate']
        self.funding_df = pd.DataFrame()
        self.sharpe_ratio_df = pd.DataFrame() # store every fund sharpe ratio count number
        self.sharpe_ratio_redline = sharpe_ratio_redline
        self.fund_analyze_path = fund_analyze_path
        self.fund_analyze_file_path = None
        
    
    def init_fund_obj(self,**kwargs):
        for key, value in kwargs.items():
            if key in vars(self).keys():
                vars(self)[key] = value
        self.download_file_path = os.path.join(self.download_path, 
                                            self.fund_name+'_'+self.fund_code+'.xlsx')
        self.fund_analyze_file_path = os.path.join(self.fund_analyze_path, 'sharpe_ratio_analyze.csv')
        self.get_networth_plot_url()
        self.create_connect()
        print("===== create fund obj {fund_name} {fund_code} =====".format(fund_name=self.fund_name,
                                                                        fund_code=self.fund_code))

    def get_networth_plot_url(self):
        if not self.date_range:
            self.url = fund_networth_url.format(fund_code=self.fund_code,
                                    page_index=self.page_index,
                                    page_size=self.page_size,
                                    start_date='',
                                    end_date='')
        if self.date_range:
            self.url = fund_networth_url.format(fund_code=self.fund_code,
                                                page_index=self.page_index,
                                                page_size=self.page_size,
                                                start_date=self.date_range[0],
                                                end_date=self.date_range[1])
    
    # get funding networth chart
    def get_networth_chart_data(self):
        _fund_data = json.loads(self.web_content.text[7:-1])
        _fund_data["Data"]['LSJZList'].reverse()
        self.funding_df = self.funding_df.append(_fund_data["Data"]['LSJZList'])
        for _col in self.drop_cols:
            try:
                self.funding_df.drop(_col, axis=1, inplace=True)
            except:
                continue
    
    # matplotlib sharpe ratop
    def create_fund_sharperatio(self):
            self.funding_df = cal_sharpe_ratio(self.funding_df, self.sharpe_ratio_cols, self.tradable_period)
    
    # get whole fund sharperatio count
    def count_fund_sharperatio_percentage(self):
        self.sharpe_ratio_df['fund_name'] = [self.fund_name]
        self.sharpe_ratio_df['fund_code'] = [self.fund_code]
        self.sharpe_ratio_df['total_trading_days'] = len(self.funding_df)
        for col in self.sharpe_ratio_cols: # 'unit_year_sharpe_ratio', 'accumulative_year_sharpe_ratio'
            for line in self.sharpe_ratio_redline: # -1, -0.5, 0, 1, 1.5, 2, 3
                # if line >= 0:
                #     self.sharpe_ratio_df[col+'_'+str(line)] = [round(self.funding_df[self.funding_df[col]>=line][col].count()/len(self.funding_df[col]),3)]
                # else:
                #     self.sharpe_ratio_df[col+'_'+str(line)] = [round(self.funding_df[self.funding_df[col]<=line][col].count()/len(self.funding_df[col]),3)]
                ind = self.sharpe_ratio_redline.index(line)
                if ind == 0:
                    self.sharpe_ratio_df[col+'<'+str(line)] = [round(self.funding_df[self.funding_df[col]<=line][col].count()/self.funding_df[col].count(),3)]
                    self.sharpe_ratio_df[col+'_'+str(line)] = [round(self.funding_df[(self.funding_df[col]>=line)&(self.funding_df[col]<self.sharpe_ratio_redline[ind+1])][col].count()/self.funding_df[col].count(),3)]
                elif ind >0 and ind < len(self.sharpe_ratio_redline)-1:
                    self.sharpe_ratio_df[col+'_'+str(line)] = [round(self.funding_df[(self.funding_df[col]>=line)&(self.funding_df[col]<self.sharpe_ratio_redline[ind+1])][col].count()/self.funding_df[col].count(),3)]
                elif ind == len(self.sharpe_ratio_redline)-1:
                    self.sharpe_ratio_df[col+'_'+str(line)] = [round(self.funding_df[self.funding_df[col]>=line][col].count()/self.funding_df[col].count(),3)]
    
    # combine all process together
    def process_fund(self):
        self.get_networth_chart_data()
        self.create_fund_sharperatio()
        self.count_fund_sharperatio_percentage()

    # export all funding pd to excel, one funding for one tab
    def export_fund_excel(self):
        print("===== start to export {fund_name} =====".format(fund_name=self.fund_name))
        try:
            # export funding data
            self.funding_df.to_excel(self.download_file_path)
            self.sharpe_ratio_df.to_csv(self.fund_analyze_file_path, mode='a', header=False)
            print("===== export completed =====")
        except:
            print("===== export {fund_name} {fund_code}fail =====".format(fund_name=self.fund_name,
                                                                          fund_code=self.fund_code))
            with open("E:\python_progams\web_crawler\export_fail.txt", "a") as f:
                f.write(self.fund_name+" "+self.fund_code+" export fail\n")
        
if __name__ == '__main__':
    # process data local
    pattern = re.compile("(.+)_(\d{6})")
    for file in os.listdir(download_path):
        f = Fund()
        f.fund_analyze_file_path = os.path.join(f.fund_analyze_path, 'sharpe_ratio_analyze.csv')
        f.funding_df = pd.read_excel(os.path.join(download_path, file))
        print(file)
        try:
            f.create_fund_sharperatio() 
            ret = re.search(pattern, file)  
            if ret:
                f.fund_name = ret.group(1)
                f.fund_code = ret.group(2)
                f.count_fund_sharperatio_percentage()
                f.sharpe_ratio_df.to_csv(f.fund_analyze_file_path, mode='a', header=False)
            else:
                print('can\'t find fund name or code')
        except:
            print(file, 'has something wrong')
            pass
        