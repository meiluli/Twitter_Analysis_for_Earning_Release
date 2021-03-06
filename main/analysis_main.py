from glob import glob
import visualization.plot_method as senti_ploter
import tool.automail as automail
import tool.sentiment_process as senti_process
import statistics.twitter_stats as twitter_stats
import tool.load_intraday as load_intraday
import warnings
warnings.simplefilter("ignore")

dir = '/Users/limeilu/PycharmProjects/Twitter_Analysis_for_Earning_Release'

def analysis_ticker(keyword_list,is_save_senti,is_plot,is_log,is_earning_release,is_stockprice,is_preopen,is_sendemail,email_addrs_list,ticker,flr_thres):
    for key_word in keyword_list:
        ####set path
        keyword_path = dir+"/utils/data/raw_twitters/"+key_word+'/'# where the raw twitters are stored
        ticker = key_word.split('$')[-1] # overwrite the ticker name

        files=glob(keyword_path+key_word+'*.csv')
        #if only need to run the program pre open time, which limit the time from last day 4:00pm to next day 9:30am
        if is_preopen:
            files = files[-2:]
        # see all files'dates
        dates = [i[-14:-4] for i in files]

        print(f'We are observing data from {dates[0]} to {dates[-1]} for {key_word}')
        # get all sentiment from all files, each file represent a day
        all_sentiments  = senti_process.SentiProcess(key_word).get_all_senti(files,flr_thres,is_log,is_save_senti)
        ###################################
        #twitter_stats.show_top(result_path,key_word,topn,is_show_topwds)
        #plot #####################################################
        if is_plot:
            senti_ploter.plot_senti(key_word,ticker,all_sentiments,is_stockprice,is_earning_release)
        
        # statits
        #twitter_stats.observe_annoucement(ticker,all_sentiments)
        #twi_daily = twitter_stats.daily_tweets(all_sentiments)
    if is_preopen:
        twitter_stats.pre_opening_analysis(keyword_list,flr_thres)
        automail.SendEmail(toaddr = email_addrs_list).send_preopen_email()
    if not is_preopen and is_sendemail:
        automail.SendEmail(toaddr = email_addrs_list).send_regular_email()

    pass

def analysis_news(kw_list,ticker,readname):

    # get all sentiment from all files, each file represent a day
    all_sentis  = senti_process.SentiProcess.analysis_news(kw_list,readname)
    #plot #####################################################
    hourly_ohlc = load_intraday.get_hourly_price(ticker)
    senti_ploter.plot_news(hourly_ohlc,all_sentis)
    pass

if __name__ == "__main__":
    # parameters
    key_word = '$RAD' # PLCE $LULU $PLAY $JW.A 
    ticker = 'RAD'
    flr_thres = 0

    flag_paras = {
        'is_save_senti' : 1 ,
        'is_plot' : 1, # plot the graph
        'is_log': 0, # log-scale or not
        'is_earning_release' : 1,
        'is_show_stock' : 1 # no stock processing would be much faster
    }
    pass