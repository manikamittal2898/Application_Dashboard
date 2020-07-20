from flask import Flask, request
from datetime import datetime
import os
import json
from flask.helpers import send_file, send_from_directory

# from flask import Flask
from mongoConnect2 import mongoConnect2
# import os
import dateutil.parser as parser
# from datetime import datetime
# import json

# connecting to mongoDB
mc = mongoConnect2()
path="C:\\Users\\User\\Desktop\\DELL\\dashboard\\Json_local_storage\\"
app_list = ["IPSDashboard-UX", "support-ode-ux", "Documents-UX", "Advisories-UX", "guidedPath-ux-prod", "OrderStatusUX", "KbArticle-UX", "article-ux", "flatcontents-ux","ProductSupport-UX","security-portal-ux","masthead-ux","support-home-ux","drivers-ux","sonar-validator-ux"]
app = Flask(__name__)

def readFromFile(st, et, ls_cf_apps_include, ls_cf_apps_exclude) :
    with open(path+os.listdir(path)[0]) as f:
        data = json.load(f)   
    ls = data
    n_ls = []

    if len(ls_cf_apps_include) == 0 :
        ls_cf_apps_include = app_list
    for item in ls :
        if item['cf_app_name'] in ls_cf_apps_include and item['cf_app_name'] not in ls_cf_apps_exclude :
            start_time = item['timestamp8601']
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
            if start_time >= st and start_time <= et :
                mp = {}
                mp['cf_app_name'] = str(item['cf_app_name'])
                mp['timestamp8601'] = str(item['timestamp8601'])
                mp['Exception_Name'] = str(item['Exception_Name'])
                mp['Exception_Details'] = str(item['Exception_Details'])
                mp['Error_Message'] = str(item['Error_Message'])

                n_ls.append(mp)
    return json.dumps(n_ls)
    with open('response.json', 'w') as json_file:
        json.dump(n_ls, json_file)


    
@app.route('/download')
def downloadfile1() :
    print("hello")
    return send_from_directory('D:\\1705415\\','Air pollution PR.pdf',as_attachment = True)


@app.route('/getExceptions')
def getExceptions() :
    return 'success'


@app.route('/filterData')
def searchDatabase() :
    ls_cf_apps_include = request.args.getlist("app_i")
    ls_cf_apps_exclude = request.args.getlist("app_x")

    ls_except_include = request.args.getlist("except_i")
    ls_except_exclude = request.args.getlist("except_x")
    st = request.args.getlist("st")
    
    et = request.args.getlist("et")
    if len(st) < 1 or len(et) < 1 :
        return "failed to fetch data"
    st = str(st[0])[:19]
    et = str(et[0])[:19]
    print(len(ls_cf_apps_include))
    st1 = datetime.strptime(st, "%Y-%m-%dT%H:%M:%S")
    et1 = datetime.strptime(et, "%Y-%m-%dT%H:%M:%S")
    print(st1)
    print(et1)

    if len(os.listdir(path=path)) > 0 :
            start_time = str(os.listdir(path=path)[0])[:17] # this will be replaced with new path
            end_time = str(os.listdir(path=path)[0])[18:]
            end_time = end_time.replace(".json","")

            #print(start_time + " " + end_time)

            dt = datetime.strptime(start_time, "%Y-%m-%dT%H%M%S")
            dt1 = datetime.strptime(end_time, "%Y-%m-%dT%H%M%S")

            print(dt)
            print(dt1)
            if st1 >= dt and et1 <= dt1:
                return readFromFile(st1, et1, ls_cf_apps_include, ls_cf_apps_exclude)
                # return "read"
            else :
                # readFromMongo()
                # return "readF1"
                from_date = st1
                to_date = et1
                r=mc.find_document(from_date, to_date)
                #Storing json data in a file
                file_name=str(from_date.isoformat())+"$"+str(to_date.isoformat())+".json"
                file_name=file_name.replace(" ","T")
                file_name=file_name.replace(":","")
                # file_name='2020-07-14 12:50:00$2020-07-14 12:55:00.json'
                print(file_name)
                out_file = open(path+file_name, "w")     
                json.dump(r, out_file, indent = 6)     
                out_file.close()
                list1=[]

                c=0
                for doc in r:
                    list1.append(doc["Exception_Name"])
                    c+=1
                # print(c)
                # print(list1)
                list_ex=list(set(list1))
                print(list_ex)

                return readFromFile(st1, et1, ls_cf_apps_include, ls_cf_apps_exclude)
    else :
        # readFromMongo()
                from_date = st1
                to_date = et1
                r=mc.find_document(from_date, to_date)
                #Storing json data in a file
                file_name=str(from_date.isoformat())+"$"+str(to_date.isoformat())+".json"
                file_name=file_name.replace(" ","T")
                file_name=file_name.replace(":","")
                # file_name='2020-07-14 12:50:00$2020-07-14 12:55:00.json'
                print(file_name)
                out_file = open(path+str(file_name), "w")     
                json.dump(r, out_file, indent = 6)     
                out_file.close()
                list1=[]

                c=0
                for doc in r:
                    list1.append(doc["Exception_Name"])
                    c+=1
                # print(c)
                # print(list1)
                list_ex=list(set(list1))
                print(list_ex)



                return readFromFile(st1, et1, ls_cf_apps_include, ls_cf_apps_exclude)
        #  return "readF2"

    # return "success"




if __name__ == '__main__' :
    app.run(debug=True,port=8089)

    """2020-07-14T125021$2020-07-14T125634.json"""