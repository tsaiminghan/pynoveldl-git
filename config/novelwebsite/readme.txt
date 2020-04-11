============== Downloader
除了encoding之外，其它參數請參考python requests初始化時的參數

proxies:
格式為
{
  'http'  : 'http://ID:PW@IP:PORT', 
  'https' : 'https://ID:PW@IP:PORT', 
}
timeout:
網頁連接逾時設定，單位為秒

encoding:
網頁編碼

headers:
requests送出的UA為python-requests/2.18.4，有些網站會阻擋requests發出的請求，
模擬mozilla的UA範例
user-agent: 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
============== NovelDownloader
ctl_append_title_when_dl_chapter:
下載章節時，將標題加入內文開頭。如原本內文已包含標題，
則會造成標頭重覆一次

ctl_dl_delay:
下載章節成功時，會延遲下載任務結束時間，單位為秒
目的是為了錯開下載的時間，但是如果開啟多線下載(pool_num)，
下載任務仍然會重疊

pool_num:
使用multiprocee多線下載，但是有些網站會回傳錯誤碼503
所以預設為1
