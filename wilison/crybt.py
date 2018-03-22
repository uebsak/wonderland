# 登录neu6抓取内容
import  urllib.request  
import urllib.parse  
import  http.cookiejar

#设置时钟
import time

# 解析抓取内容
from bs4 import BeautifulSoup
import io  
import sys

# 发送邮件提醒
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# 登录六维，两个参数：用户名un和密码pw
def login_neu6(un,pw):
    #post的内容  
    values={   
    'password':pw, 
    'username':un, 
    'quickforward':'yes',
    'handlekey':'ls'  
    }  
    
    #登陆的地址  
    logUrl="http://bt.neu6.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    
    #构建cook  
    cook=http.cookiejar.CookieJar()  
    
    #构建openner  
    openner=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cook))  
    
    #添加headers  
    openner.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]  
    
    r=openner.open(logUrl,urllib.parse.urlencode(values).encode())  
    
    #print(r.read().decode('gbk'))  
    
    r=openner.open("<font color="#ff0000">http://bt.neu6.edu.cn/forum-13-1.html</font>")     # 要监控的页面的网址
    all_html = r.read().decode('gbk')
    return all_html


    # 解析抓取到的内容，查找资源是否存在。两个参数：登录后打开的页面html_content、查找的电影资源名称film
def check_neu6(html_content,film):
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码  
    soup = BeautifulSoup(html_content,"lxml")
    result = soup.find_all("a",class_="s xst")
    exist = False
    for re in result:
        find_index = re.get_text().find(film)
        if find_index >= 0: 
            exist = True
            break
        
    return exist

# 发送邮件提醒，一个参数：查找的电影资源名称film
# 方法来自廖雪峰官网python教程
# 注意：可能会被某些邮箱识别为垃圾邮件
def email_alert(film):
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    
    from_addr = "XXXXXXXXXXXXXX@126.com"      #### 在这填入登录邮箱
    password = "XXXXXXXXXXXXXXX"                    #### 在这填入邮箱登陆密码
    to_addr = "XXXXXXXXXXXXX@qq.com"       #### 在这填入要接受提醒的邮箱
    smtp_server = "smtp.126.com"        #### SMTP邮件服务器地址
    
    msg = MIMEText('<%s>有资源了' % film, 'plain', 'utf-8')
    msg['From'] = _format_addr('jeff <%s>' % from_addr)
    msg['To'] = _format_addr('jeff <%s>' % to_addr)
    msg['Subject'] = Header('from 126 test', 'utf-8').encode()
    
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

# 每n分钟执行一次
def timer(n,film):
    while True:
        content = login_neu6("username","password")    #### 在这填入六维用户名和密码
        is_exist = check_neu6(content,film)
        if is_exist:
            email_alert(film)
            print("邮件已发送，请设置参数后重新开启程序")
            break
        time.sleep(n*60)
        
# 每15分钟查找一下“雷神3”的资源
timer(15,"雷神3")        #### 在这设置查找的时间间隔和电影名称（由于资源区更新较慢，建议不要设置太短的时间，那样既浪费计算资源又有可能被识别为账号异常）
