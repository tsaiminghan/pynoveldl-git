# pynoveldl-git

I'm studing to use web crawler to get the novels from websites.<br>

enviroment setup step:<br>
1. install python3, and then setup python and pip enviroemnt path.<br>
2. install below python module.<br>
 pip install PyYAML<br>
 pip install lxml<br>
 pip install BeautifulSoup<br>
 pip install requests<br>
 pip install html2text<br>

3. transter to epub and mobi, need below enviroment.<br>
  AozoraEpub3  (need Java)<br>
  <a href="https://w.atwiki.jp/hmdev/pages/21.html">https://w.atwiki.jp/hmdev/pages/21.html</a><br>
  KindleGen  <br>
  <a href="https://www.amazon.com/gp/feature.html?docId=1000765211">https://www.amazon.com/gp/feature.html?docId=1000765211</a><br>
  put them together, and set the path to AozoraEpub3_path in globals.yaml.

4. set path for the AozoraEpub3, edit config/globals.yaml or excute below command to setup. <br>
- n.bat init

my enviroment is:<br>
  Window8<br>
  Python 3.8.2<br>
