# funding_url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183009011155042599239_1630513361408&fundCode=671010&pageIndex=7&pageSize=20&startDate=2020-09-01&endDate=2021-09-01&_=1630513616427'

# this is net worth funding web page
# daily_fund_url = 'http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1'
daily_fund_url = 'http://fund.eastmoney.com/Data/Fund_JJJZ_Data.aspx?t=1&lx=1&letter=&gsid=&text=&sort=bzdm,asc&page=1,12000&dt=1631027590766&atfc=&onlySale=0'
daily_fund_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Referer': 'http://fund.eastmoney.com/fund.html'
}

fund_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Referer': 'http://fundf10.eastmoney.com/'
}

# 2021-09-02 date format
fund_networth_url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery&fundCode={fund_code}&pageIndex={page_index}&pageSize={page_size}&startDate={start_date}&endDate={end_date}&_=1630855459200'