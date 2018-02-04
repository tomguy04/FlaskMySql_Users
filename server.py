from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from datetime import datetime
app = Flask(__name__)
mysql = MySQLConnector(app,'dbsemi-restful_users')

@app.route('/users')
def index():
    friends = mysql.query_db("SELECT * FROM tblsrusers")
    print friends
    return render_template('index.html', all_friends=friends)

@app.route('/users/new')
def new():
    return render_template('adduser.html')

# Insert into database starting with the root route, then the index from root sends us to this route.
@app.route('/users/create', methods=['POST'])
def create():
    print "*******HERE*****"
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
   
    query = "INSERT INTO tblsrusers (first_name, last_name, email, created_at, updated_at) VALUES (:fname, :lname, :email, NOW(), NOW())"
    
    #print query
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'fname': request.form['first_name'],
             'lname': request.form['last_name'],
             'email':  request.form['email']
           }
    # Run query, with dictionary values injected into the query.
    user_data = mysql.query_db(query, data)
    print "**********THE user_data is********************"
    print user_data
    #return redirect('/users/query')
    #return redirect('/users/uid', uid=user_data)
    #return redirect('/users')
    user_path = '/users/'+str(user_data)
    return redirect(user_path)

@app.route('/users/<uid>', methods=['POST'])
def update(uid):
    print "*****************"
    print uid
    
    update_query = "update tblsrusers set first_name = :fname, last_name = :lname, email = :email where id = :myid"
    update_data = {
                    'fname': request.form['first_name'],
                    'lname': request.form['last_name'],
                    'email': request.form['email'],
                    'this_id':uid,
                    'myid':uid
                }
    mysql.query_db(update_query, update_data)

    query = "SELECT * FROM tblsrusers WHERE id = :myid"
    data = {
            'myid':uid
        }

    user_data = mysql.query_db(query, data)
    return render_template('user_profile.html',user = user_data[0])

@app.route('/users/<uid>', methods=['GET'])
def show(uid):
    print "*****************"
    print uid
    
    query = "SELECT * FROM tblsrusers WHERE id = :myid"
    data = {
            'myid':uid
        }

    user_data = mysql.query_db(query, data)
    return render_template('user_profile.html',user = user_data[0])





    
@app.route('/users/<uid>/edit')
def edit(uid):
    print "*****************"
    print uid
    query = "SELECT * FROM tblsrusers WHERE id = :myid"
    data = {
            'myid':uid
        }
    user_data = mysql.query_db(query, data)
    return render_template('edit_profile.html',user = user_data[0])

@app.route('/users/<uid>/destroy')
def destroy(uid):
    print "*****************"
    print uid
    query = "delete FROM tblsrusers WHERE id = :myid"
    data = {
            'myid':uid
        }
    user_data = mysql.query_db(query, data)
    return redirect('/users')



# @app.route("/goback")
# def goback():
#   return redirect("/users")
app.run(debug=True)
