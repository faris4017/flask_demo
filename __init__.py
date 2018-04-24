from flask import Flask,render_template,request,redirect,url_for,flash
import pymysql,os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'E:/Python/Fari/responsive/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config["APPLICATION_ROOT"] = ""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# app.root_path

@app.route("/")
def main():
    return  render_template('login.html')

@app.route("/login_check", methods=['post'])
def login_check():
    if request.method == 'POST':
        email = request.form['email']
        pswrd = request.form['pswrd']
        
        try:
            cur.execute("SELECT * FROM crazykart_user WHERE email='"+email+"' AND password='"+pswrd+"'")
        except:
            return "Null"
        no_row = cur.rowcount
        if no_row == 1 :
            return redirect(url_for('home'))
        else:
            return redirect(url_for('main'))
    else:
        return "Error Fetch error"
        
@app.route("/about")
def header():  
    return render_template('about.html')


@app.route("/footer")
def footer():
    return render_template('footer.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/delete_product/<int:id>",)
def delete_product(id):
    try:
        delstatmt = "update `crazykart_product` set del_status ='1'  WHERE id = '"+str(id)+"'"
        cur.execute(delstatmt)
        con.commit()
        # cur.execute("delete from crazykart_product where id=?", (id))
        # con.commit()
    except:
        return "please try again"
    return redirect("/product")

@app.route("/product")
def product():
    try:
        cur.execute("SELECT *  FROM crazykart_category where status='1' ")
        category = cur.fetchall()
        cur.execute("SELECT *  FROM crazykart_product where del_status='0' ")  
        product = cur.fetchall()
        con.commit()
        return render_template('product.html', data=product,category = category)

        # where del_status='0'"
        
    except:
        return Exception.message


@app.route("/addProduct", methods=['post'])
def addProduct():
    if request.method == 'POST':
        # return "hiiii"
        product_code = request.form['code']
        product_name = request.form['name']
        product_price = request.form['price']
        f = request.files['file']
        select_id = request.form['select_id']
        # print str(f)
        # return str(f)
        try:
            # return "INSERT INTO crazykart_product(product_code,product_name,product_price,product_image) VALUES("+str(
            #     product_code)+",'"+product_name+"',"+str(product_price)+","+str(f)+")"

            # cur.execute("INSERT INTO crazykart_product(product_code,product_name,product_price,product_image) VALUES("+str(product_code)+",'"+product_name+"',"+str(product_price)+","+str(f)+")")
            # con.commit()
            
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"static/upload/file/images/", filename))
                cur.execute("INSERT INTO crazykart_product(product_code,product_name,product_price,product_image) VALUES(" +
                            str(product_code)+",'"+product_name+"',"+str(product_price)+",'"+filename+"')")
                con.commit()
            return redirect("/product")
        except:
            return Exception.message

      
        return 'file uploaded successfully'
        


@app.route("/edit_product/<int:id>")
def edit_product(id):
    """Dic String"""
    #Fetching data from table
    cur.execute("SELECT *  FROM crazykart_product where id = '"+str(id)+"'")
    con.commit()
    edit_fetch_data = cur.fetchall()
    return render_template('edit_product.html', edit_data=edit_fetch_data,item_id=id)


@app.route("/edit_product_data", methods=['post'])
def edit_product_data():
    if  request.method ==  'POST':
        item_id = request.form['item_id']
        product_code = request.form['product_code']
        product_name = request.form['product_name']
        product_price = request.form['prodcut_price']
        f = request.files['product_file']
        try:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER']+"static/upload/file/images/", filename))
                cur.execute("UPDATE crazykart_product SET product_code="+product_code+",product_name='"+product_name+"',product_price="+product_price+",product_image='"+filename+"' WHERE id="+item_id+"")
                con.commit()
                return redirect("/product")
        except:
            return Exception.message


# Image upload code




@app.route("/category")
def category():
    try:
        cur.execute("SELECT *  FROM crazykart_category WHERE status=1")
        category_data = cur.fetchall()
        con.commit()
        return render_template('category.html', category_data=category_data, category_id = '',cat_name = '')
    except:
        return Exception.message

@app.route("/addCategory", methods=['POST'])
def addCategory():
    if request.method == 'POST':
        category_name = request.form['category']
        try:
            cur.execute("INSERT INTO crazykart_category(category) values('"+category_name+"') ")
            con.commit()
            return redirect("/category")
        except:
            return Exception.message


@app.route("/edit_category/<int:id>/<name>")
def edit_category(id,name):
    
    try:
        cur.execute("SELECT *  FROM crazykart_category WHERE status=1")
        category_data = cur.fetchall()
        con.commit()
        return render_template('category.html', category_data=category_data, category_id =id,cat_name=name)
    except:
        return Exception.message

        
@app.route("/update_form", methods=['POST']) 
def update_form():
    if request.method == 'POST':
      category =  request.form['category']
      category_id = request.form['cat_id']
      try:
        cur.execute("UPDATE crazykart_category SET category='"+category+"' WHERE id='"+category_id+"' ")
        con.commit()
        return redirect("/category")
      except:
        return Exception.message


@app.route("/delete_category/<int:id>")
def delete_category(id):
    try:
        cur.execute("UPDATE crazykart_category SET status=0 WHERE id='"+str(id)+"'") 
        con.commit()
        return redirect("/category")
    except:
        return Exception.message
      


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





if __name__ == "__main__":
    con = pymysql.connect("localhost", "root", "", "crazykart")
    cur = con.cursor()
    app.debug = True
    app.run()
