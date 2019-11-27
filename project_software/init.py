from flask import Flask
from xml.dom.minidom import parse
import  xml.dom.minidom

from flask import Flask,request,render_template,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import time

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)







# def first_load():
    # if __name__ == '__main__':
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    REPORT_NUM = db.Column(db.Integer)
    EVENT_PROPERTY_NAME = db.Column(db.String)
    EVENT_TYPE_ID = db.Column(db.Integer)
    EVENT_TYPE_NAME = db.Column(db.String)
    EVENT_SRC_NAME = db.Column(db.String)
    DISTRICT_ID = db.Column(db.Integer)
    DISTRICT_NAME = db.Column(db.String)
    COMMUNITY_ID = db.Column(db.String)
    REC_ID = db.Column(db.String)
    STREET_ID = db.Column(db.String)
    OVERTIME_ARCHIVE_NUM = db.Column(db.String)
    OPERATE_NUM = db.Column(db.String)
    DISPOSE_UNIT_ID = db.Column(db.String)
    STREET_NAME = db.Column(db.String)
    CREATE_TIME = db.Column(db.String)
    EVENT_SRC_ID = db.Column(db.String)
    INTIME_TO_ARCHIVE_NUM = db.Column(db.String)
    SUB_TYPE_NAME = db.Column(db.String)
    EVENT_PROPERTY_ID = db.Column(db.String)
    OCCUR_PLACE = db.Column(db.String)
    COMMUNITY_NAME = db.Column(db.String)
    DISPOSE_UNIT_NAME = db.Column(db.String)
    MAIN_TYPE_NAME = db.Column(db.String)
    MAIN_TYPE_ID = db.Column(db.String)
db.drop_all()
db.create_all()

dom_tree=xml.dom.minidom.parse('2019 Project Data/坪山区-民生诉求数据_完整版.xml')
print(dom_tree)
collection=dom_tree.documentElement
events_1=collection.getElementsByTagName('REPORT_NUM')
events_2=collection.getElementsByTagName('EVENT_PROPERTY_NAME')
events_3=collection.getElementsByTagName('EVENT_TYPE_ID')
events_4=collection.getElementsByTagName('EVENT_TYPE_NAME')
events_5=collection.getElementsByTagName('EVENT_SRC_NAME')
events_6=collection.getElementsByTagName('DISTRICT_ID')
events_7=collection.getElementsByTagName('DISTRICT_NAME')
events_8=collection.getElementsByTagName('COMMUNITY_ID')
events_9=collection.getElementsByTagName('REC_ID')
events_10=collection.getElementsByTagName('STREET_ID')
events_11=collection.getElementsByTagName('OVERTIME_ARCHIVE_NUM')
events_12=collection.getElementsByTagName('OPERATE_NUM')
events_13=collection.getElementsByTagName('DISPOSE_UNIT_ID')
events_14=collection.getElementsByTagName('STREET_NAME')
events_15=collection.getElementsByTagName('CREATE_TIME')
events_16=collection.getElementsByTagName('EVENT_SRC_ID')
events_17=collection.getElementsByTagName('INTIME_TO_ARCHIVE_NUM')
events_18=collection.getElementsByTagName('SUB_TYPE_NAME')
events_19=collection.getElementsByTagName('EVENT_PROPERTY_ID')
events_20=collection.getElementsByTagName('OCCUR_PLACE')
events_21=collection.getElementsByTagName('COMMUNITY_NAME')
events_22=collection.getElementsByTagName('DISPOSE_UNIT_NAME')
events_23=collection.getElementsByTagName('MAIN_TYPE_NAME')
events_24=collection.getElementsByTagName('MAIN_TYPE_ID')


i=1
print(events_1[0].childNodes[0].data)


for i in range(len(events_1)):
    if '2018-10-30' not in events_15[i].childNodes[0].data:
         event_to_add=Event(REPORT_NUM=int(events_1[i].childNodes[0].data),
                            EVENT_PROPERTY_NAME=(events_2[i].childNodes[0].data),
                            EVENT_TYPE_ID=(events_3[i].childNodes[0].data),
                            EVENT_TYPE_NAME=(events_4[i].childNodes[0].data),
                            EVENT_SRC_NAME=(events_5[i].childNodes[0].data),
                            DISTRICT_ID=(events_6[i].childNodes[0].data),
                            DISTRICT_NAME=(events_7[i].childNodes[0].data),
                            COMMUNITY_ID=(events_8[i].childNodes[0].data),
                            REC_ID=(events_9[i].childNodes[0].data),
                            STREET_ID=(events_10[i].childNodes[0].data),
                            OVERTIME_ARCHIVE_NUM=(events_11[i].childNodes[0].data),
                            OPERATE_NUM=(events_12[i].childNodes[0].data),
                            DISPOSE_UNIT_ID=(events_13[i].childNodes[0].data),
                            STREET_NAME=(events_14[i].childNodes[0].data),
                            CREATE_TIME=(events_15[i].childNodes[0].data),
                            EVENT_SRC_ID=(events_16[i].childNodes[0].data),
                            INTIME_TO_ARCHIVE_NUM=(events_17[i].childNodes[0].data),
                            SUB_TYPE_NAME=(events_18[i].childNodes[0].data),
                            EVENT_PROPERTY_ID=(events_19[i].childNodes[0].data),
                            OCCUR_PLACE=(events_20[i].childNodes[0].data),
                            COMMUNITY_NAME=(events_21[i].childNodes[0].data),
                            DISPOSE_UNIT_NAME=(events_22[i].childNodes[0].data),
                            MAIN_TYPE_NAME=(events_23[i].childNodes[0].data),
                            MAIN_TYPE_ID=(events_24[i].childNodes[0].data)
                            )
         db.session.add(event_to_add)

db.session.commit()
print('一结束')
def refresh():
    # class Event2(db.Model):
    #     __tablename__ = 'events'
    #     id = db.Column(db.Integer, primary_key=True)
    #     REPORT_NUM = db.Column(db.Integer)
    #     EVENT_PROPERTY_NAME = db.Column(db.String)
    #     EVENT_TYPE_ID = db.Column(db.Integer)
    #     EVENT_TYPE_NAME = db.Column(db.String)
    #     EVENT_SRC_NAME = db.Column(db.String)
    #     DISTRICT_ID = db.Column(db.Integer)
    #     DISTRICT_NAME = db.Column(db.String)
    #     COMMUNITY_ID = db.Column(db.String)
    #     REC_ID = db.Column(db.String)
    #     STREET_ID = db.Column(db.String)
    #     OVERTIME_ARCHIVE_NUM = db.Column(db.String)
    #     OPERATE_NUM = db.Column(db.String)
    #     DISPOSE_UNIT_ID = db.Column(db.String)
    #     STREET_NAME = db.Column(db.String)
    #     CREATE_TIME = db.Column(db.String)
    #     EVENT_SRC_ID = db.Column(db.String)
    #     INTIME_TO_ARCHIVE_NUM = db.Column(db.String)
    #     SUB_TYPE_NAME = db.Column(db.String)
    #     EVENT_PROPERTY_ID = db.Column(db.String)
    #     OCCUR_PLACE = db.Column(db.String)
    #     COMMUNITY_NAME = db.Column(db.String)
    #     DISPOSE_UNIT_NAME = db.Column(db.String)
    #     MAIN_TYPE_NAME = db.Column(db.String)
    #     MAIN_TYPE_ID = db.Column(db.String)



    dom_tree = xml.dom.minidom.parse('2019 Project Data/坪山区-民生诉求数据_完整版.xml')
    print(dom_tree)
    collection = dom_tree.documentElement
    events_1 = collection.getElementsByTagName('REPORT_NUM')
    events_2 = collection.getElementsByTagName('EVENT_PROPERTY_NAME')
    events_3 = collection.getElementsByTagName('EVENT_TYPE_ID')
    events_4 = collection.getElementsByTagName('EVENT_TYPE_NAME')
    events_5 = collection.getElementsByTagName('EVENT_SRC_NAME')
    events_6 = collection.getElementsByTagName('DISTRICT_ID')
    events_7 = collection.getElementsByTagName('DISTRICT_NAME')
    events_8 = collection.getElementsByTagName('COMMUNITY_ID')
    events_9 = collection.getElementsByTagName('REC_ID')
    events_10 = collection.getElementsByTagName('STREET_ID')
    events_11 = collection.getElementsByTagName('OVERTIME_ARCHIVE_NUM')
    events_12 = collection.getElementsByTagName('OPERATE_NUM')
    events_13 = collection.getElementsByTagName('DISPOSE_UNIT_ID')
    events_14 = collection.getElementsByTagName('STREET_NAME')
    events_15 = collection.getElementsByTagName('CREATE_TIME')
    events_16 = collection.getElementsByTagName('EVENT_SRC_ID')
    events_17 = collection.getElementsByTagName('INTIME_TO_ARCHIVE_NUM')
    events_18 = collection.getElementsByTagName('SUB_TYPE_NAME')
    events_19 = collection.getElementsByTagName('EVENT_PROPERTY_ID')
    events_20 = collection.getElementsByTagName('OCCUR_PLACE')
    events_21 = collection.getElementsByTagName('COMMUNITY_NAME')
    events_22 = collection.getElementsByTagName('DISPOSE_UNIT_NAME')
    events_23 = collection.getElementsByTagName('MAIN_TYPE_NAME')
    events_24 = collection.getElementsByTagName('MAIN_TYPE_ID')
    for i in range(len(events_1)):
        k=0

        if '2018-10-30' in events_15[i].childNodes[0].data:

            print(i)
            event_to_add = Event(REPORT_NUM=int(events_1[i].childNodes[0].data),
                                 EVENT_PROPERTY_NAME=(events_2[i].childNodes[0].data),
                                 EVENT_TYPE_ID=(events_3[i].childNodes[0].data),
                                 EVENT_TYPE_NAME=(events_4[i].childNodes[0].data),
                                 EVENT_SRC_NAME=(events_5[i].childNodes[0].data),
                                 DISTRICT_ID=(events_6[i].childNodes[0].data),
                                 DISTRICT_NAME=(events_7[i].childNodes[0].data),
                                 COMMUNITY_ID=(events_8[i].childNodes[0].data),
                                 REC_ID=(events_9[i].childNodes[0].data),
                                 STREET_ID=(events_10[i].childNodes[0].data),
                                 OVERTIME_ARCHIVE_NUM=(events_11[i].childNodes[0].data),
                                 OPERATE_NUM=(events_12[i].childNodes[0].data),
                                 DISPOSE_UNIT_ID=(events_13[i].childNodes[0].data),
                                 STREET_NAME=(events_14[i].childNodes[0].data),
                                 CREATE_TIME=(events_15[i].childNodes[0].data),
                                 EVENT_SRC_ID=(events_16[i].childNodes[0].data),
                                 INTIME_TO_ARCHIVE_NUM=(events_17[i].childNodes[0].data),
                                 SUB_TYPE_NAME=(events_18[i].childNodes[0].data),
                                 EVENT_PROPERTY_ID=(events_19[i].childNodes[0].data),
                                 OCCUR_PLACE=(events_20[i].childNodes[0].data),
                                 COMMUNITY_NAME=(events_21[i].childNodes[0].data),
                                 DISPOSE_UNIT_NAME=(events_22[i].childNodes[0].data),
                                 MAIN_TYPE_NAME=(events_23[i].childNodes[0].data),
                                 MAIN_TYPE_ID=(events_24[i].childNodes[0].data)
                                 )
            db.session.add(event_to_add)
            db.session.commit()


            time.sleep(2)

            k+=1
