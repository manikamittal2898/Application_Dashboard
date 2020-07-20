from pymongo import MongoClient

class mongoConnect2:
    # db_url = "mongodb://esupport:esu#&p@ausdlesmgdb01.us.dell.com:27100/admin?connect=replicaSet"
    db_url ="mongodb://localhost:27017/?readPreference=primary&ssl=false"
    # db_name = "esupport"
    db_name = "error-logs"
    # collection_name = "log"
    collection_name = "col"

    def __init__(self):
        try:
            self.Client = MongoClient(self.db_url, maxPoolSize=100)
            print('Connection established!')
        except Exception as e:
            print('Connection failed due to an error! Error: ',e)

    def push_to_db(self, list_of_items):
        collection = self.Client[self.db_name][self.collection_name]
        try:
            collection.insert_many(list_of_items)
            print('Successfully pushed the documents!')
        except:
            print('Connection Error')
    
    # def find_document(self,elements):
    def find_document(self,from_date,to_date):
    #    Function to retrieve single or multiple documents from a provided
        # Collection using a dictionary containing a document's elements.
        collection = self.Client[self.db_name][self.collection_name]
        try:
            # {"$gte": from_date, "$lte": to_date}
            # x = collection.find({},{'_id': 0, "timestamp8601": 1, "message": 1, "cf_app_name": 1,"level" :1,"Error_Message" :1,"Exception_Details" :1,"Exception_Name" :1 }) 
            list=[]
            x=collection.find({"timestamp8601":{"$gte": from_date, "$lte": to_date}})
            # x=collection.find({"Exception_Name":"Number.Exception"})
            for element in x: 
               del element['_id']
               del element['message']
               del element['level']
               element['timestamp8601'] = element['timestamp8601'].strftime("%Y-%m-%dT%H:%M:%S")
               list.append(element)
            #    print(element)
            #    print("\n")
            # results = collection.find(elements)
            print('Successfully fetched the documents!')
            return list
            # print("in try")
            
        except:
            print('Connection Error ')
            # print("in except")
        # results = collection.find(elements)
        # return [r for r in results]

