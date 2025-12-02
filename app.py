from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3
app = Flask(__name__)
app.secret_key='saniya2401'
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        conn=sqlite3.connect('database/data.db')
        c=conn.cursor()
        c.execute('INSERT INTO users (name,email,password) VALUES(?,?,?)',(name,email,password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        conn=sqlite3.connect('database/data.db')
        c=conn.cursor()
        c.execute('SELECT * FROM users WHERE email=? AND password=?',(email,password))
        row=c.fetchone()
        conn.close()
        if row:
            session['user_id']=row[0]
            session['name']=row[1]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')
@app.route('/add_job',methods=['GET','POST'])
def add_job():
    if  request.method=='POST':
        company_name=request.form['company_name']
        role=request.form['role']
        status=request.form['status']
        date_applied=request.form['date_applied']
        user_id=session.get('user_id')
        conn=sqlite3.connect('database/data.db')
        c=conn.cursor()
        c.execute('INSERT INTO applications (company_name,role,status,date_applied,user_id) VALUES(?,?,?,?,?)',
                  (company_name,role,status,date_applied,user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_job.html')
@app.route('/edit_job/<int:job_id>',methods=['GET','POST'])
def edit_job(job_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn=sqlite3.connect('database/data.db')
    c=conn.cursor()
    if request.method=='POST':
        new_company_name=request.form['company_name']
        new_role=request.form['role']
        new_status=request.form['status']
        new_date_applied=request.form['date_applied']
        c.execute('UPDATE applications SET company_name=?, role=?, status=?, date_applied=? WHERE id=? AND user_id=?',(new_company_name,new_role,new_status,new_date_applied,job_id,session['user_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))    
    else:
        c.execute('SELECT * FROM applications WHERE id=? AND user_id=?',(job_id,session['user_id']))
        job=c.fetchone()
        conn.close()
        return render_template('edit_job.html',job=job)
@app.route('/delete_job/<int:job_id>')
def delete_job(job_id):
    if 'user_id' in session:
        conn=sqlite3.connect('database/data.db')
        c=conn.cursor()
        c.execute('DELETE FROM applications WHERE id=? AND user_id=?',(job_id,session['user_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id=session.get('user_id')
    conn=sqlite3.connect('database/data.db')
    c=conn.cursor()
    c.execute('SELECT * FROM applications WHERE user_id=?',(user_id,))
    jobs=c.fetchall()
    conn.close()
    return render_template('dashboard.html',jobs=jobs,name=session.get('name'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True,port=5005)
