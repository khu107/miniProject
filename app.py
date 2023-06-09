from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi


ca = certifi.where()
client = MongoClient('', tlsCAFile=ca)
db = client.dbsparta0

@app.route('/')
def home():
    return render_template('index.html')

# 쇼핑몰 상세 페이지 leolego03
@app.route('/view')
def view():
    item_id = request.args.get('itemid')
    view_item = db.shop.find_one({'num': int(item_id)}, {'_id': False})

    return render_template('view.html', view_item = view_item)

#######
@app.route("/itemdetails", methods=["GET"])   # 아이템 하나 상세정보 모두 불러오기
def item_details():
    itemid_receive = int(request.args.get('itemid_give', False))

    # 아이템 정보 찾기
    item_details = db.shop.find_one({'num': itemid_receive}, {'_id': False})

    if item_details:
        return jsonify({'result': item_details, 'msg': '아이템 정보가 불러와졌습니다'})
    else:
        return jsonify({'msg': '아이템을 찾을 수 없습니다.'})

@app.route("/shop", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    name_receive = request.form['name_give']
    category_receive = request.form['category_give']
    price_receive = request.form['price_give']
    count_receive = request.form['count_give']
    area_receive = request.form['area_give']

    shop_list = list(db.shop.find({}))
    count = len(shop_list) + 1
    print(type(count))
    doc = {
        'num': count,
        'url':url_receive,
        'name':name_receive,
        'category':category_receive,
        'price':price_receive,
        'count':count_receive,
        'area':area_receive

    }
    db.shop.insert_one(doc)

    return jsonify({'msg':'succsess'})

@app.route("/shop/cards",methods = ["POST"])
def api_cards():

    num =  request.form["num"]
    # data =list( db.shop.find_one({"num":int(num)}))
    data = list(db.shop.find({'num':int(num)},{'_id':False}))
    
    for i in data:
         db.user.insert_one(i)
    
    
    
    return jsonify({"data":'saqlandi'})
    
            

@app.route("/shop/cards",methods = ["GET"])
def api_get():
        
        
        user = list(db.user.find({},{'_id':False}))
        

        return jsonify({"status" : user})

@app.route("/shop", methods=["GET"])
def movie_get():

    all = list(db.shop.find({},{'_id':False}))
    
    
    return jsonify({'result':all})

@app.route('/card')
def start():
    return render_template('card.html')

@app.route('/pay', methods=["POST"])
def pay():
     
     name = request.form['name']
     val = request.form['val']
     address = request.form['address']
     
     
     doc = {
          'name':name,
          'val':val,
          'address':address
     }
     db.pay.insert_one(doc)

     db.user.delete_many({})

    
     return jsonify({'pay':'sucsess'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
