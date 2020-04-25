# pynoveldl-git

I'm studing to use web crawler to get the novels from websites.<br>
my enviroment is:<br>
  Window8<br>
  Python 3.8.2<br>

enviroment setup step:<br>
1. install python3, and then setup python and pip to windows enviroemnt path.<br>
  https://www.python.org/download/releases/3.0/</br>
  During installing process, Please tick the checkbox【Add python 3.8.x to PATH】<br>
  and python would be add to windows enviroment path.<br>
  https://docs.python.org/3/using/windows.html<br>
  
2. install below python module.<br>
 pip install PyYAML<br>
 pip install lxml<br>
 pip install BeautifulSoup<br>
 pip install requests<br>
 pip install html2text<br>
 pip install opencc-python-reimplemented<br>

3. transter to epub and mobi, need below enviroment.<br>
  AozoraEpub3 (need Java)<br>
  https://w.atwiki.jp/hmdev/pages/21.html<br>
  OpenJDK (java), I try the newest jdk-14.0.1 on below site, and it works fine for AozoraEpub3.<br>
  need add it to windows enviroment path, too.<br>
  https://jdk.java.net/archive/<br>
  KindleGen  <br>
  https://www.amazon.com/gp/feature.html?docId=1000765211<br>
  put kindleGen and AozraEpub3 together

4. set AozoraEpub3 and KindleGen path, edit config/globals.yaml or excute below command to setup. <br>
  n.bat init<br>
  
<h3>command usage</h3>

1. get command infomation.<br>
  n.bat help<br>

2. get the free chapters from qidian, run below command on cmds<br>
  n.bat download https://book.qidian.com/info/1010868264<br>
  or<br>
  n.bat d https://book.qidian.com/info/1010868264<br>
  
<h3>References:</h3>
  https://github.com/whiteleaf7/narou<br>
  https://github.com/eight04/ComicCrawler<br>
