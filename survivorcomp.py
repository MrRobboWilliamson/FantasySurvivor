### Example inspired by Tutorial at https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
### However the actual example uses sqlalchemy which uses Object Relational Mapper, which are not covered in this course. I have instead used natural sQL queries for this demo. 
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, BlogForm
import pandas as pd
import sqlite3
import datetime

# connect to db and turn on the referential integrity constraints
conn = sqlite3.connect('survivor.db')
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')

# connect flasky things
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# get the competition name
conn = sqlite3.connect('survivor.db')
conn.row_factory = dict_factory
c = conn.cursor()
c.execute("SELECT distinct comp_nm \
        FROM FantasyCompetition")
COMPNAME = c.fetchall()[0]['comp_nm'] 

@app.context_processor
def feed_layout():
    conn = sqlite3.connect('survivor.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT name, ep_no \
        FROM contestant \
        Where ep_no is not Null \
        order by ep_no")
    out_cons = c.fetchall()
    return dict(out_cons=out_cons)

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    # connect to the db and get the users
    conn = sqlite3.connect('survivor.db')
    conn.row_factory = dict_factory
    c = conn.cursor() 
    
    c.execute('SELECT user_nm FROM CompUser')
    results = c.fetchall()
    users = [(results.index(item), item['user_nm']) for item in results]
        
    form = BlogForm()
    form.username.choices = users
    if form.validate_on_submit():
        # get the users choice
        choices = form.username.choices
        user = (choices[form.username.data][1])
        time_ = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        content = form.content.data

        # clear the form data
        form.content.data = form.content.default

        # insert the blog message into the database
        conn = sqlite3.connect('survivor.db')
        c = conn.cursor()

        # NEED TO REPLACE QUOTES WITH DOUBLE QUOTES 
        query = 'insert into Blog (time_, user_nm, comp_nm, post) VALUES ("{}","{}", "{}", "{}")'.format(time_, user, COMPNAME, content)
        c.execute(query)
        conn.commit()

        return redirect(url_for('blog'))
    
    conn = sqlite3.connect('survivor.db')

    #Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM Blog \
        ORDER BY time_ DESC")
    blogs = c.fetchall()

    return render_template('blog.html', posts=blogs, form=form)

@app.route("/")
@app.route("/leaderboard")
def board():
    # Run a query to calculate all of the user scores    
    conn = sqlite3.connect('survivor.db')
    conn.row_factory = dict_factory
    c = conn.cursor()

    # Query for the teams
    query = 'select p.user_nm, t.team_nm, c.name, c.ep_no\
        FROM ParticipatingUser p, Team t, Based_on b, Contestant c\
        WHERE t.user_nm=p.user_nm and b.team_nm=t.team_nm and b.contestant_id=c.contestant_id'
    c.execute(query)   
    df = pd.DataFrame(c.fetchall())

    # Query for the episodes
    c.execute('Select MAX(ep_no) as max from Episode')
    epmax = c.fetchall()[0]['max']
    df = df.fillna(epmax+1)

    # aggregate the scores
    leader_board = df.groupby(['user_nm', 'team_nm'])['ep_no'].agg('sum').reset_index(). \
        sort_values(['ep_no'], ascending=False).rename(columns={'ep_no':'score'})
   
    return render_template('leaderboard.html', leader_board=leader_board)

@app.route("/contestants")
def contestants():
    conn = sqlite3.connect('survivor.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    
    # get the number of times that each contestant has been picked
    c.execute("SELECT contestant_id, count(*) as num_picks \
                FROM based_on \
                GROUP BY contestant_id")
    
    # put into a dataframe for joining
    picks = pd.DataFrame(data=c.fetchall())

    # select the contestant details and put into data frame
    c.execute("SELECT * \
                FROM contestant")
    ctemp = pd.DataFrame(data=c.fetchall())
    # print('\n', ctemp, '\n')

    # join them and fill the blanks with zeros
    contestants = ctemp.merge(right=picks, on=['contestant_id'], how='left')
    contestants['num_picks'] = contestants['num_picks'].fillna(0)
    
    # calculate popularity as a percentage of all picks and sort for presentation
    tot_picks = contestants['num_picks'].sum()
    contestants['popular'] = (contestants['num_picks'] / float(tot_picks)).apply(lambda x: '{:.0%}'.format(x))
    contestants = contestants.sort_values(['num_picks', 'name'], ascending=[False, True])
    
    print('\n', contestants, '\n')

    # convert back dictionary 
    contestants = contestants.to_dict('records')

    return render_template('contestants.html', contestants=contestants)

# Add User
# sets the html file to be displayed - assigns this method to that page
@app.route("/register", methods=['GET', 'POST'])
def register():
    # links the correct form to the page65
    form = RegistrationForm()
    # checks for valid input
    if form.validate_on_submit():
        # commit the new user to the database
        new_user = form.username.data
        email = form.email.data

        # open db
        conn = sqlite3.connect('survivor.db')
        c = conn.cursor()
        c.execute("insert into CompUser values ( '" + new_user + "', '" + email + "')")
        conn.commit()
        
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('board'))
        
    return render_template('register.html', title='Register', form=form)

if __name__ == '__main__':
    app.run(debug=True)