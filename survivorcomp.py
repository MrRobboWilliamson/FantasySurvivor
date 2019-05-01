### Example inspired by Tutorial at https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
### However the actual example uses sqlalchemy which uses Object Relational Mapper, which are not covered in this course. I have instead used natural sQL queries for this demo. 
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, BlogForm, EditForm, DelForm, LoginForm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
import datetime
import initialise

# connect flasky things
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Function to connect to the database everytime
def get_db():
    conn = sqlite3.connect('survivor.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    
    # enforce integrity constraints 
    c.execute("PRAGMA foreign_keys=ON;")
    return c, conn

# Get the competition name
c, conn = get_db()
c.execute("SELECT distinct comp_nm \
        FROM FantasyCompetition")
COMPNAME = c.fetchall()[0]['comp_nm']

# Progress chart
def chart_progress(df):
    '''
    Get the contestants and loop through in order of the episode out
    to create a progress chart
    '''
    # get contestant and teams data from the db
    c, conn = get_db()
    c.execute('Select * from contestant \
        where ep_no is not null \
        order by ep_no')
    contestants = pd.DataFrame(c.fetchall())
    
    # zero out the ep_no in the teams df
    df['ep_no'] = pd.np.nan
    print('\n\nProgress calcs:')
    progress = pd.DataFrame()
    num_eps = 24
    for idx, row in contestants.iterrows():
        ep_no = row['ep_no']
        name = row['name']

        # assign score to all of the teams
        df[df['name']==name]['ep_no'] = ep_no

        # fill the rest with ep_no + 1
        mdf = df.copy()
        mdf['ep_no'].fillna(ep_no+1, inplace=True)

        # aggregate the scores
        this_ep = mdf.groupby(['user_nm', 'team_nm'])['ep_no'].agg('sum').reset_index(). \
                sort_values(['ep_no'], ascending=False).rename(columns={'ep_no':'score'})
        this_ep['ep_no'] = ep_no
        progress = progress.append(this_ep)

    fig = plt.figure()
    sns.lineplot(x='ep_no', y='score', hue='team_nm', data=progress)
    plt.savefig(r"static\progress.png")
    print('\n\n')

@app.context_processor
def feed_layout():
    c, conn = get_db()
    c.execute("SELECT name, ep_no \
        FROM contestant \
        Where ep_no is not Null \
        order by ep_no")
    out_cons = c.fetchall()
    return dict(out_cons=out_cons)

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    # connect to the db and get the users
    c, conn = get_db()    
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

        # insert the blog message into the database
        c, conn = get_db()
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

@app.route("/blog/edit/<time>/<username>/<comp_name>", methods=['GET', 'POST'])
def blog_detail_view_edit(time, username, comp_name):
    # conv
    c, conn = get_db()
    time = time.replace('-', '/')
    c.execute("SELECT * FROM Blog where time_=? and user_nm=? and comp_nm=?", [time, username, comp_name]) 
    blog = c.fetchone()
    if blog:
        # Render a detailForm and show it.
        form = EditForm()
        form.content.data = blog['post']
        if form.validate_on_submit():
            if 'submit' in request.form:
                # get the new post
                new_post = request.form.get('content')
                print("What is the new post?", new_post)

                # commit it to the database
                c, conn = get_db()
                c.execute("UPDATE Blog \
                    SET post=? \
                    WHERE time_=? and user_nm=? and comp_nm=?", (new_post, time, username, comp_name))
                conn.commit()
                return redirect(url_for('blog'))
            elif 'cancel_btn' in request.form:
                # if cancelling then just redirect back to the message board
                return redirect(url_for('blog'))
    else:
        # TODO: return 404 page
        return "Not found"
    return render_template('edit.html', form=form)

@app.route("/blog/delete/<time>/<username>/<comp_name>", methods=['GET', 'POST'])
def blog_detail_view_delete(time, username, comp_name):
    # get the form with the buttons
    form = DelForm()
    time = time.replace('-', '/')
    if form.validate_on_submit():
        if 'delete_btn' in request.form:
            print('Delete request')
            # delete the post
            c, conn = get_db()
            c.execute("DELETE FROM Blog \
                WHERE time_=? and user_nm=? and comp_nm=?", [time, username, comp_name])
            conn.commit()
            return redirect(url_for('blog'))
        elif 'cancel_btn' in request.form:
            print('Cancel request')

            # if cancelled, then just redirect
            return redirect(url_for('blog'))
        else:
            print("That didn't work!")

    return render_template('delete.html', form=form)

@app.route("/")
@app.route("/leaderboard")
def board():
    # Run a query to calculate all of the user scores    
    c, conn = get_db()

    # Query for the teams
    query = 'select p.user_nm, t.team_nm, c.name, c.ep_no\
        FROM ParticipatingUser p, Team t, Based_on b, Contestant c\
        WHERE t.user_nm=p.user_nm and b.team_nm=t.team_nm and b.contestant_id=c.contestant_id'
    c.execute(query)   
    df = pd.DataFrame(c.fetchall())

    # get chart
    chart_progress(df)

    # Query for the episodes
    c.execute('Select MAX(ep_no) as max from Episode')
    epmax = c.fetchall()[0]['max']
    mdf = df.fillna(epmax+1)

    # aggregate the scores
    leader_board = mdf.groupby(['user_nm', 'team_nm'])['ep_no'].agg('sum').reset_index(). \
        sort_values(['ep_no'], ascending=False).rename(columns={'ep_no':'score'})
    
    return render_template('leaderboard.html', leader_board=leader_board)

@app.route("/contestants")
def contestants():
    c, conn = get_db()
    
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

#Add Login feature
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    conn = sqlite3.connect('survivor.db')
    conn.row_factory = dict_factory
    c = conn.cursor() 
    
    c.execute('SELECT user_nm FROM CompUser')
    result = c.fetchall()
    users = [item['user_nm'] for item in result]

    print('\n\n', users)

    print('\n\n')

    form = LoginForm()
    content = form.username.data

    if content in users:
        flash(f'Logged in as {content}!', 'success')

        print('success')
    else:   
        error = 'Invalid Credentials. Please try again.'
        print(error)

    return render_template('login.html', form=form, error=error)


if __name__ == '__main__':
    app.run(debug=True)