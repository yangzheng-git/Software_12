#coding=UTF-8
from flask import Flask,render_template,request,flash,session,redirect,url_for
from xml.dom.minidom import parse
import  xml.dom.minidom
from flask_sqlalchemy import SQLAlchemy,current_app
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required,login_manager,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from concurrent.futures import  ThreadPoolExecutor
executor=ThreadPoolExecutor(1)
import json
import os
import init

UPLOAD_FOLDER = os.getcwd()+'/static/avatar/'

SQLALCHEMY_BINDS = {
    'users': 'sqlite:///testDB.db',
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test1.db'
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
time_month1 = '10'
time_day1 = '29'
time_month2 = '10'
time_day2 = '29'

app.secret_key = 'lalalalisa'

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

@login_manager.user_loader
###加载用户的回调函数接收以Unicode字符串形式表示的用户标示符
###如果能找到用户，这个函数必须返回用户对象，否则返回None。
def load_user(user_id):
    return User.query.get(int(user_id))


class Event(db.Model):
    __tablename__='events'
    id=db.Column(db.Integer,primary_key=True)
    REPORT_NUM=db.Column(db.Integer)
    EVENT_PROPERTY_NAME=db.Column(db.String)
    EVENT_TYPE_ID=db.Column(db.Integer)
    EVENT_TYPE_NAME=db.Column(db.String)
    EVENT_SRC_NAME=db.Column(db.String)
    DISTRICT_ID=db.Column(db.Integer)
    DISTRICT_NAME= db.Column(db.String)
    COMMUNITY_ID = db.Column(db.String)
    REC_ID = db.Column(db.String)
    STREET_ID = db.Column(db.String)
    OVERTIME_ARCHIVE_NUM= db.Column(db.String)
    OPERATE_NUM = db.Column(db.String)
    DISPOSE_UNIT_ID = db.Column(db.String)
    STREET_NAME=db.Column(db.String)
    CREATE_TIME = db.Column(db.String)
    EVENT_SRC_ID= db.Column(db.String)
    INTIME_TO_ARCHIVE_NUM = db.Column(db.String)
    SUB_TYPE_NAME= db.Column(db.String)
    EVENT_PROPERTY_ID = db.Column(db.String)
    OCCUR_PLACE= db.Column(db.String)
    COMMUNITY_NAME = db.Column(db.String)
    DISPOSE_UNIT_NAME = db.Column(db.String)
    MAIN_TYPE_NAME = db.Column(db.String)
    MAIN_TYPE_ID= db.Column(db.String)

class User(UserMixin,db.Model):
    # 定义表
    __bind_key__ = 'users'
    __tablename__ = 'users'
    # 定义字段
    # db.Column表示是一个字段
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(16))
    name = db.Column(db.String(16))
    department = db.Column(db.String(16))
    username = db.Column(db.String(16),unique=True)
    real_avatar = db.Column(db.String(128), default='../static/avatar/default.png')
    first_login = db.Column(db.String(16), default='YES')
    password = db.Column(db.String(32))
    check = db.Column(db.String(16))

    def __repr__(self):
        return '<User: %s %s %s>' % (self.name,self.password,self.department)

def find_key2_by_key1(date1:str,date2:str,key1:str,key2=None,if_order=True):#第三代数据获取demo，key1是大类，key2是小类，实现更加灵活多变的数据需求，iforder默认只取十个属性
#def find_key2_by_key1(date: str, key1: str, key2=None, if_order=True):
    statistics = {}
    datas = db.session.query(Event).all()
    print(date1)
    print(date2)

    for data in datas:  # 只对给定日期的时间做统计
        if date1 <= data.CREATE_TIME[:10] and data.CREATE_TIME[:10]<=date2:
        #if date in  data.CREATE_TIME:
            if statistics.get(eval('data' + '.' + key1)) == None :
                if key2!=None:#有两个关键字
                    statistics[eval('data' + '.' + key1)] = {}
                    statistics[eval('data' + '.' + key1)][eval('data' + '.' + key2)] = 1
                else:#只有一个关键字
                    statistics[eval('data' + '.' + key1)] = 1
            else:
                if key2!=None:
                    if statistics[eval('data' + '.' + key1)].get(eval('data' + '.' + key2)) == None:
                        statistics[eval('data' + '.' + key1)][eval('data' + '.' + key2)] = 1
                    else:
                        statistics[eval('data' + '.' + key1)][eval('data' + '.' + key2)] = int(
                            statistics[eval('data' + '.' + key1)][eval('data' + '.' + key2)]) + 1
                else:
                    statistics[eval('data' + '.' + key1)] += 1

    list1 = sorted(statistics.items(), key=lambda x: x[0])#排了个假序，因为是中文
    for i in list1:
         if i[0] == '-':
             list1.remove(i)

    if key2==None:
        list1=sorted(list1,key=lambda x:x[1],reverse=True)

    if len(list1) != 0:
        if if_order == True:
            print(json.dumps(list1[:10],ensure_ascii=False))
            return json.dumps(list1[:10],ensure_ascii=False)
        else:
            print(json.dumps(list1,ensure_ascii=False))
            return json.dumps(list1,ensure_ascii=False)
    else:
        return '没有数据'


def take_time(elme):
   # print(elme)
    return int(elme['time'][11:13]+elme['time'][14:16])

def abnormal():
    events = []
    datas = db.session.query(Event).all()#滚动显示不分优先级
    for data in datas:
        if  '2018-10-30' in data.CREATE_TIME:#异常事件
            event={}
            event['time']=data.CREATE_TIME
            event['street']=data.STREET_NAME
            event['community']=data.COMMUNITY_NAME
            event['source']=data.EVENT_SRC_NAME
            event['sub_type']=data.SUB_TYPE_NAME
            event['property']=data. EVENT_PROPERTY_NAME
            event['unity_name']=data.DISPOSE_UNIT_NAME
            events.append(event)
    # final=json.dumps(events,ensure_ascii=False)
    # print(len(final))
    # print(events[1]['time'][5:7]+events[1]['time'][8:10])
    # print(take_time(events[2]))
    events = sorted(events, key=lambda x: x['time'])
    #print(events)
    return json.dumps(events)

def current_abnormal():
    #DISPOSE_UNIT_NAME
    events = []
    #datas = db.session.query(Event).all()  # 滚动显示不分优先级
    datas = Event.query.filter_by(DISPOSE_UNIT_NAME=current_user.department).all()
    for data in datas:
        if '2018-10-30' in data.CREATE_TIME:  # 异常事件
            event = {}
            event['time'] = data.CREATE_TIME
            event['street'] = data.STREET_NAME
            event['community'] = data.COMMUNITY_NAME
            event['source'] = data.EVENT_SRC_NAME
            event['sub_type'] = data.SUB_TYPE_NAME
            event['property'] = data.EVENT_PROPERTY_NAME
            event['unity_name'] = data.DISPOSE_UNIT_NAME
            events.append(event)

    # final=json.dumps(events,ensure_ascii=False)
    # print(len(final))
    #print(events[1]['time'][5:7]+events[1]['time'][8:10])
    #print(take_time(events[2]))
    events=sorted(events,key=lambda x:x['time'])
    #print(events)

    return events

departms=['安监办（坑梓街道办事处）', '安全生产监督管理办公室（坪山街道办事处）', '安全生产监督管理局', '办公室（碧岭街道办事处）', '碧岭办事处市政服务中心', '碧岭办事处市政服务中心（碧岭街道办事处）', '碧岭社区', '碧岭社区（碧岭街道办事处）', '财政局（国资办）', '城管办（碧岭街道办事处）', '城管办（坑梓街道办事处）', '城建办', '城建办公室（碧岭街道办事处）', '城建办公室（马峦街道办事处）', '城建办公室（坪山街道办事处）', '城建办公室（石井街道办事处）', '城建办（坑梓街道办事处）', '城建办（龙田街道办事处）', '城市更新局', '城市管理办公室（马峦街道办事处）', '城市管理局', '城投公司', '大工业区水务有限公司', '发展和改革局（统计局）', '公共服务办公室（马峦街道办事处）', '公共服务办（碧岭街道办事处）', '公共服务办（石井街道办事处）', '广东移动深圳公司', '规划土地监察大队', '和平社区', '和平社区（坪山街道办事处）', '环境保护和水务局', '环境水政监察大队', '江岭社区', '江岭社区（马峦街道办事处）', '建筑工务局', '交通轨道办', '教育局', '街区发展办公室（马峦街道办事处）', '纪工委（坑梓街道办事处）', '纪工委（龙田街道办事处）', '机关事务服务中心（马峦街道办事处）', '机关事务管理局', '机关事务中心', '纪律检查工作委员会（坪山街道办事处）', '经济和科技促进局', '金龟社区工作站', '金沙社区', '金沙社区（坑梓街道办事处）', '科技创新服务署', '坑梓街道分中心处置', '坑梓街道分中心处置（坑梓街道办事处）', '坑梓社区', '坑梓社区（坑梓街道办事处）', '坑梓自来水公司', '坑梓自来水公司（坑梓街道办事处）', '坑梓自来水公司（坑梓辖区）', '劳动办（坑梓街道办事处）', '劳动办（龙田街道办事处）', '劳动办（坪山街道办事处）', '劳动管理办公室（马峦街道办事处）', '老坑社区', '老坑社区（龙田街道办事处）', '六和社区', '六和社区（坪山街道办事处）', '六联社区', '六联社区（坪山街道办事处）', '龙田街道综合执法队', '龙田街道综合执法队（龙田街道办事处）', '龙田社区', '龙田社区（龙田街道办事处）', '马峦办事处综合执法队', '马峦办事处综合执法队（马峦街道办事处）', '民政局', '南布社区', '南布社区（龙田街道办事处）', '坪环社区', '坪环社区（马峦街道办事处）', '坪山公安分局', '坪山供电局', '坪山交通运输局', '坪山街道电信营业中心', '坪山街道综合执法队', '坪山街道综合执法队（坪山街道办事处）', '坪山联通营业中心', '坪山区城中村综合整治办', '坪山社区', '坪山社区（坪山街道办事处）', '坪山自来水有限公司', '坪山自来水有限公司（坪山街道办事处）', '区测试责任单位一', '群团工作部', '区委宣传部（文体旅游局）', '区委政法委', '区委组织部', '区委（区政府）办公室', '区责任单位', '区指挥中心', '区指挥中心处置', '人力资源局', '沙湖社区', '沙湖社区（碧岭街道办事处）', '沙坣社区', '沙坣社区（马峦街道办事处）', '沙田社区', '沙田社区（坑梓街道办事处）', '社保坪山分局', '市规划国土委坪山管理局', '市规土委坪山管理局', '市交警支队坪山大队', '石井办事处市政服务中心', '石井办事处市政服务中心（石井街道办事处）', '石井办事处综合执法队', '石井办事处综合执法队（石井街道办事处）', '石井社区工作站', '石井社区工作站（石井街道办事处）', '市市场和质量监管委坪山局', '市政服务中心（坑梓街道办事处）', '市政服务中心（龙田街道办事处）', '市政服务中心（马峦街道办事处）', '市政服务中心（坪山街道办事处）', '汤坑社区', '汤坑社区（碧岭街道办事处）', '天隆广播电视网络有限公司', '田头社区工作站', '田头社区工作站（石井街道办事处）', '田心社区工作站（石井街道办事处）', '土地整备局', '土地整备中心（碧岭办）', '土地整备中心（龙田街道办事处）', '土地整备中心（马峦）', '土地整备中心（坪山街道办事处）', '土地整备中心（石井街道办事处）', '卫生和计划生育局', '武装部（龙田街道办事处）', '消安委办（碧岭街道办事处）', '消安委办（坪山街道办事处）', '消安委办（石井街道办事处）', '消防安全管理委员会办公室', '消防安全委员会办公室', '消防安全委员会办公室（坑梓街道办事处）', '秀新社区', '秀新社区（坑梓街道办事处）', '宣传统战办公室（龙田街道办事处）', '政府投资项目前期工作管理办公室', '值班应急与智慧管理指挥分中心（龙田街道办事处）', '值班应急与智慧管理指挥分中心（马峦街道办事处）', '住房和建设局', '竹坑社区', '竹坑社区（龙田街道办事处）', '综治维稳办公室（碧岭街道办事处）', '综治维稳办公室（马峦街道办事处）', '综治维稳办（坑梓街道办事处）', '组织部（坑梓街道办事处）', '组织部（龙田街道办事处）']

@app.route('/', methods=['GET','POST'])
def index():
    return redirect(url_for('login'))

@app.route('/Login',methods=['GET','POST'])
def login():
    logout_user()
    # login_form = LoginForm()
    # 1,判断请求方式
    if request.method == 'POST':

        # 2,获取请求参数
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username,password]):

            flash(u'参数不完整')

        user=User.query.filter_by(username=username).first()

        if  user is not  None and check_password_hash(user.password, password)==True and user.check=='YES':
            login_user(user)
            return redirect(url_for('display'))
        elif user is None:
            flash('用户不存在')
        else:
            flash('密码错误')

    return render_template('Login.html', departms=departms)


@app.route('/register',methods=['GET','POST'])
def register():
    # register_form = RegisterForm()
    # 1,判断请求方式
    if request.method == 'POST':
        # 2,获取请求参数
        name = request.form.get('name')
        department = request.form.get('department')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        # 3,验证参数是否填写以及密码是否相同,WTF可以一句话就实现所有的校验
        # 我们没有CSRF token
        # if register_form.validate_on_submit():
        if not all ([name, department, username, password, password2]):
            flash('参数不完整')
        elif password == password2 and user is None:
            # role = Role(name=name)
            # db.session.add(role)
            # db.session.commit()
            user = User(name=name, role='用户', department=department, username=username,
                        password=generate_password_hash(password), check='NO')
            db.session.add(user)
            db.session.commit()
            flash('等待审核')
        elif user is not None:
            flash('用户名已存在')
        else:
            flash('密码输入不一致')
    return redirect('/Login')


@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        avatar = request.files['avatar']
        if str(avatar) != "<FileStorage: '' ('application/octet-stream')>" :
            fname = avatar.filename
            ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
            flag = '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        else:
            flag = 999

        if not all ([name, department, username, password, password2]):
            flash('参数不完整')
        elif flag == False:
            flash('文件类型错误')
        elif password == password2:
            if flag == True:
                avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, current_user.username, fname))
                current_user.real_avatar = '/static/avatar/{}_{}'.format(current_user.username, fname)
            current_user.name = name
            current_user.department = department
            current_user.username = username
            current_user.password = generate_password_hash(password)
            db.session.commit()
            flash('修改成功')
        else:
            flash('密码输入不一致')

    return render_template('profile.html', current=current_user, departms=departms, dbnum=len(current_abnormal()))


@app.route('/abnormal', methods=['GET','POST'])
@login_required
def abnormal_events():
        return render_template('abnormal.html', current=current_user, events=current_abnormal(), dbnum=len(current_abnormal()))


@app.route('/refresh',methods=['GET','POST'])   #第一个参数是路由，第二个是请求方法
def real_refresh():
    executor.submit(init.refresh)
    return '0'

# @app.route('/button',methods=['GET','POST'])   #第一个参数是路由，第二个是请求方法
# def button():
#     return render_template('refresh.html')

@app.route('/chart1/refresh',methods=['GET','POST'])   #第一个参数是路由，第二个是请求方法
def ch1_refresh():
    global time_month1
    global time_day1
    global time_month2
    global time_day2
    recv_data = request.get_data()  #得到前端传送的数据
    print(recv_data)
    #print(time_day)
    data1 = find_key2_by_key1('2018-' + time_month1+'-'+time_day1,'2018-' + time_month2+'-'+time_day2, 'EVENT_PROPERTY_NAME')
    return data1                  #返回数据

@app.route('/chart1',methods=['GET','POST'])
def chart_1():
    # data= Event.query(Event.STREET_NAME).first()
    '''
    向网页传递数据示例
    针对问题一：
    find_key...('2018-02','EVENT_PROPERTY_NAME')
    问题二：
    find...('2018-02','STREET_NAME','SUB_TYPE_NAME')

    问题三：
    find...('2018-02-11','COMMUNITY_NAME',if_order=False)
    问题四：
    find。。。。（'...','OVERTIME_ARCHIVE_NUM','EVENT_TYPE_NAME'）返回的1是超期结办
    还可以查询上中下旬，月份，年份的数据
    :return:
    '''
    global time_month1
    global time_day1
    global time_month2
    global time_day2
    if request.method == 'POST':
        time_month1 = request.form.get('daterange')[0:2]
        print(time_month1)
        time_day1 = request.form.get('daterange')[3:5]
        print(time_day1)
        time_month2 = request.form.get('daterange')[13:15]
        print(time_month2)
        time_day2 = request.form.get('daterange')[16:18]
        print(time_day2)


    # return render_template("test_data.html")
    return render_template("问题情况.html",
    data1=find_key2_by_key1('2018-' + time_month1+'-'+time_day1,'2018-' + time_month2+'-'+time_day2, 'EVENT_PROPERTY_NAME'),
    data2=str(find_key2_by_key1('2018-' + time_month1 + '-' + time_day1,'2018-' + time_month2 + '-' + time_day2, 'OVERTIME_ARCHIVE_NUM','EVENT_TYPE_NAME')),
                           M1=time_month1,D1=time_day1,M2=time_month2,D2=time_day2,current=current_user,abdata=abnormal(),dbnum=len(current_abnormal()))
###################################################3




@app.route('/chart2/refresh',methods=['GET','POST'])   #第一个参数是路由，第二个是请求方法
def ch2_refresh():
    global time_month1
    global time_day1
    global time_month2
    global time_day2
    recv_data = request.get_data()  #得到前端传送的数据
   # print('hhhhhhhhhh')
   #  print(time_day)
    data1 = find_key2_by_key1('2018-' + time_month1+'-'+time_day1,'2018-' + time_month2+'-'+time_day2,'STREET_NAME','SUB_TYPE_NAME')
    return data1                  #返回数据
@app.route('/chart2',methods=['GET','POST'])
def chat_2():
    # data= Event.query(Event.STREET_NAME).first()

    global time_month1
    global time_day1
    global time_month2
    global time_day2
    if request.method == 'POST':
        time_month1 = request.form.get('daterange')[0:2]
        print(time_month1)
        time_day1 = request.form.get('daterange')[3:5]
        print(time_day1)
        time_month2 = request.form.get('daterange')[13:15]
        print(time_month2)
        time_day2 = request.form.get('daterange')[16:18]
        print(time_day2)

    return render_template('街道事件.html',data=str(find_key2_by_key1('2018-' + time_month1+'-'+time_day1,'2018-' + time_month2+'-'+time_day2,'STREET_NAME','SUB_TYPE_NAME')),
                           M1=time_month1,D1=time_day1,M2=time_month2,D2=time_day2,current=current_user,abdata=abnormal(),dbnum=len(current_abnormal()))
#
#
#
# #############################################################################
@app.route('/chart3/refresh',methods=['GET','POST'])   #第一个参数是路由，第二个是请求方法
def ch3_refresh():
    global time_month1
    global time_day1
    global time_month2
    global time_day2
    recv_data = request.get_data()  #得到前端传送的数据

    data1 =find_key2_by_key1('2018-' + time_month1+'-'+time_day1,'2018-' + time_month2+'-'+time_day2,'COMMUNITY_NAME',if_order=False)
    return data1                  #返回数据
@app.route('/chart3',methods=['GET','POST'])
def chat_3():
    global time_month1
    global time_day1
    global time_month2
    global time_day2
    if request.method == 'POST':
        time_month1 = request.form.get('daterange')[0:2]
        print(time_month1)
        time_day1 = request.form.get('daterange')[3:5]
        print(time_day1)
        time_month2 = request.form.get('daterange')[13:15]
        print(time_month2)
        time_day2 = request.form.get('daterange')[16:18]
        print(time_day2)

    return render_template('热点社区.html',data=str(find_key2_by_key1('2018-' + time_month1+'-'+time_day1,'2018-' + time_month2+'-'+time_day2,'COMMUNITY_NAME',if_order=False)),
                           M1=time_month1, D1=time_day1, M2=time_month2, D2=time_day2,current=current_user,abdata=abnormal(),dbnum=len(current_abnormal()))
# ##################################################################
@app.route('/chart4/refresh',methods=['GET','POST'])   #第一个参数是路由，第二个是请求方法
def ch4_refresh():
    global time_month1
    global time_day1
    global time_month2
    global time_day2
    recv_data = request.get_data()  #得到前端传送的数据

    data2 = find_key2_by_key1('2018-' + time_month1+'-'+time_day1,'2018-' + time_month2+'-'+time_day2,'OVERTIME_ARCHIVE_NUM','EVENT_TYPE_NAME')
    return data2                 #返回数据


@app.route('/manage', methods=['GET','POST'])
@login_required
def manage():
    if current_user.role == '管理员':
        userno = User.query.filter_by(check='NO').all()
        userrole = User.query.filter_by(role='用户', check='YES').all()
        return render_template('manage.html', userno=userno, userrole=userrole, current=current_user, abdata = abnormal(),dbnum=len(current_abnormal()))
    else:
        return redirect('display')


@app.route('/agree/<name>', methods=['GET','POST'])
@login_required
def agree(name):
    if current_user.role == '管理员':
        user = User.query.filter_by(name=name).first()
        user.check = 'YES'
        db.session.commit()
        return redirect(url_for('manage'))
    else:
        return redirect(url_for('display'))

@app.route('/disagree/<name>', methods=['GET','POST'])
@login_required
def disagree(name):
    if current_user.role == '管理员':
        user = User.query.filter_by(name=name).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('manage'))
    else:
        return redirect(url_for('display'))


@app.route('/levelchange/<name>', methods=['GET','POST'])
@login_required
def levelchange(name):
    if current_user.role == '管理员':
        user = User.query.filter_by(name=name).first()
        user.role = '管理员'
        db.session.commit()
        return redirect(url_for('manage'))
    else:
        return redirect('display')


@app.route('/display',methods=['GET','POST'])
@login_required
def display():
    user = User.query.filter_by(check='YES').all()
    check = User.query.filter_by(check='NO').all()
    datanum = Event.query.count()
    usernum = len(user)
    checknum = len(check)
    if current_user.first_login=='YES':
        current_user.first_login='NO'
        db.session.commit()
        if current_user.role=='管理员':
            return render_template('display_manager.html', current=current_user, abdata=abnormal(), usernum=usernum, checknum=checknum, datanum=datanum,dbnum=len(current_abnormal()))
        else:
            return render_template('display_user.html', current=current_user, abdata=abnormal(), usernum=usernum, checknum=checknum, datanum=datanum,dbnum=len(current_abnormal()))
    else:
        return render_template('display.html', current=current_user, abdata=abnormal(), usernum=usernum, checknum=checknum, datanum=datanum,dbnum=len(current_abnormal()))

if __name__ == '__main__':
    #db.drop_all('users')
    db.create_all()
    # user = User(name='余南炜', role='管理员', department='主管部门', username='ynw', first_login='YES',
    #             password='123', check='YES')
    # db.session.add(user)
    # user=User.query.filter_by(name='秋田弘').first()
    # user.password=generate_password_hash('123')
    # db.session.commit()
    app.run()