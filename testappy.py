from flask import Flask, redirect,render_template
from scrape_mars import scrape
import pymongo
##############   Mongodb set up
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.scrape_db
collection = db.tb_scrape_data



#### Flask setup####
testapp = Flask(__name__)

### flask routes

@testapp.route("/scrape")
def start_scrape():
    #funcrion call to get the scrape data in a dictionary 
    result_dist = scrape()
    #save the in monodb
    collection.insert_one(result_dist)
    return redirect("/",code=302)

@testapp.route("/")    
def index():
    mars = db.tb_scrape_data.find_one()
    
    return render_template("index.html",mars=mars)

if __name__ == '__main__':
    testapp.run(debug=True)    