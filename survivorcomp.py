### Example inspired by Tutorial at https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
### However the actual example uses sqlalchemy which uses Object Relational Mapper, which are not covered in this course. I have instead used natural sQL queries for this demo. 
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, BlogForm, EditForm, DelForm, LoginForm, LogoutForm, CreateTeam
import pandas as pd
import seaborn as sns # configure to webapp
import matplotlib.pyplot as plt, mpld3
import matplotlib.font_manager as font_manager
import sqlite3
import datetime
from username import User

# catch initialise exceptions because it won't always work
try:
    import initialise
except Exception as e:
    print('\n\n')
    print('Scraper not working: {}\n\n'.format(e))

# initialise user object
USERNM = User()

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
    progress = pd.DataFrame()
    num_eps = 24
    for idx, row in contestants.iterrows():
        ep_no = row['ep_no']
        name = row['name']

        # assign score to the teams that the evictee from this episode
        df.loc[df['name']==name, ['ep_no']] = ep_no

        # fill the rest with ep_no + 1 as their potential score
        mdf = df.copy()
        mdf['ep_no'].fillna(ep_no+1, inplace=True)

        # aggregate the scores for the estimated totals for following this episode
        this_ep = mdf.groupby(['user_nm', 'team_nm'])['ep_no'].agg('sum').reset_index(). \
                sort_values(['ep_no'], ascending=False).rename(columns={'ep_no':'score'})
        this_ep['ep_no'] = ep_no
        progress = progress.append(this_ep)

    # plot properties
    # Set the font properties (for use in legend)
    chart_size = 14
    label_size = 18
    font_prop = font_manager.FontProperties(size=chart_size)

    # plot the result
    fig, ax = plt.subplots()
    sns.set(style='whitegrid')
    sns.lineplot(x='ep_no', y='score', hue='Team', data=progress.rename(columns={'team_nm': 'Team'}))
    # sns.despine(left=True, bottom=True)
    plt.xlabel('Episode', dict(size=label_size))
    plt.ylabel('Potential scores', dict(size=label_size))
    plt.yticks(size=chart_size)
    plt.xticks(size=chart_size)
    plt.legend(prop=font_prop)
    plt.tight_layout()
    return mpld3.fig_to_html(fig)

def find_superstars():
    '''
    This function will perform a division query to see if there are any
    contestants that have been picked by all users
    '''

    # connect to the database
    c, conn = get_db()
    
    # get all of the teams and contestants
    query = \
        "SELECT contestant_id FROM Contestant \
        WHERE NOT EXISTS ( \
            SELECT team_nm FROM Team \
            EXCEPT \
            SELECT team_nm FROM Based_on \
            WHERE Contestant.contestant_id=Based_on.contestant_id \
            );"

    c.execute(query)
    super_stars = c.fetchall()
    
    # return a list of contestant ids
    return [item['contestant_id'] for item in super_stars]

def apply_status(user):
    '''
    Checks the status by seeing if the user is in participating or not
    '''
    c, conn = get_db()
    c.execute("select user_nm from ParticipatingUser")
    result = c.fetchall()
    pusers = [item['user_nm'] for item in result]

    if user in pusers:
        USERNM.set_status('participating')
    else:
        USERNM.set_status('passive')

def print_log():
    c, conn = get_db()
    c.execute('SELECT * FROM USER_LOG ORDER BY timestamp DESC LIMIT 10')
    result = c.fetchall()

    print ('\n\nShowing top 6 results from user_log:')
    
    print(' _' * 42)

    print('| {: <19}| {: <19}| {: <19}| {: <19}|'.format('USER', 'TIME', 'EMAIL', 'ACTION'))
    print('|{:-<20}+{:-<20}+{:-<20}+{:-<20}|'.format('', '', '', ''))
    for item in result:
        print('| {: <19}| {: <19}| {: <19}| {: <19}|'.format(
            item['user_nm'], item['timestamp'], item['email'], item['action']))

    print('-' * 85 + '\n')

@app.context_processor
def feed_layout():
    c, conn = get_db()
    c.execute("SELECT name, ep_no \
        FROM contestant \
        Where ep_no is not Null \
        order by ep_no")
    out_cons = c.fetchall()
    return dict(out_cons=out_cons, user=USERNM)

@app.route("/blog", methods=['GET', 'POST'])
def blog():
    form = BlogForm()
    if form.validate_on_submit():
        # get the users choice
        time_ = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        content = form.content.data

        # insert the blog message into the database
        c, conn = get_db()
        query = 'insert into Blog (time_, user_nm, comp_nm, post) VALUES ("{}","{}", "{}", "{}")'.format(time_, USERNM.name, COMPNAME, content)
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

    return render_template('blog.html', posts=blogs, form=form, user_nm=USERNM.name)

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

    # chart the progress to this episode
    plot = chart_progress(df.copy())

    # Query for the episodes
    c.execute('Select MAX(ep_no) as max from Episode')
    epmax = c.fetchall()[0]['max']
    mdf = df.fillna(epmax+1)

    # aggregate the scores
    leader_board = mdf.groupby(['user_nm', 'team_nm'])['ep_no'].agg('sum').reset_index(). \
        sort_values(['ep_no'], ascending=False).rename(columns={'ep_no':'score'})

    return render_template('leaderboard.html', leader_board=leader_board, plot=plot)

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
    
    # print('\n', contestants, '\n')
    super_stars = find_superstars()

    # convert back dictionary 
    contestants = contestants.to_dict('records')
    return render_template('contestants.html', contestants=contestants, super_stars=super_stars)

@app.route("/create-team", methods=['GET', 'POST'])
def create_team():
    c, conn = get_db()    

    # get the contestants
    c.execute('Select contestant_id, name from contestant')
    contestants = c.fetchall()
    form = CreateTeam()
    pre_sql = []
    # f = request
    if form.validate_on_submit():
        team_name = form.teamname.data
        for con in contestants:
            con_id = con['contestant_id']
            checkbox = "checkboxes-{}".format(con_id) 
            if checkbox in request.form:
                # print(request.form[checkbox])            
                pre_sql.append(
                    "('{}',{})".format(team_name, str(con_id))
                )

        if len(pre_sql) == 4 and team_name:
            # need to add the user to the participating user table
            c, conn = get_db()
            c.execute('INSERT INTO ParticipatingUser (user_nm) VALUES (?)', [USERNM.name])
            conn.commit()
            
            # add the team name to the Team table
            c, conn = get_db()
            c.execute('INSERT INTO Team (team_nm, user_nm, comp_nm) \
                VALUES (?,?,?)', [team_name, USERNM.name, COMPNAME])
            conn.commit()

            # then insert 
            c, conn = get_db()
            c.execute('INSERT INTO Based_on (team_nm, contestant_id) VALUES ' + ','.join(pre_sql))
            conn.commit()

            # update the user status
            apply_status(USERNM.name)

            # redirect to the leaderboard
            return redirect(url_for('board'))
        else:
            flash("Please pick four team members")


    return render_template('create_team.html', form=form, contestants=contestants)

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

        flash('Account created for {}!'.format(form.username.data), 'success')
        print_log()
        return redirect(url_for('login'))
        
    return render_template('register.html', title='Register', form=form)

#Add Login feature
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    c, conn = get_db()
    c.execute('SELECT user_nm FROM CompUser')
    results = c.fetchall()
    users = [item['user_nm'] for item in results]

    # print('\n',users,'\n')

    form = LoginForm()
    if form.validate_on_submit():
        # get the users choice
        if form.username.data not in users:
            flash('User not found!')
        else:
            # Set the user name and status
            USERNM.set_user_nm(form.username.data)
            apply_status(USERNM.name)

            # update the layout form
            feed_layout()
            
            # go to myaccount
            if USERNM.status=='passive':
                return redirect(url_for('create_team'))
            else:
                return redirect(url_for('board'))

    return render_template('login.html', form=form, error=error)

#Add myaacount feature
@app.route("/myaccount", methods=['GET', 'POST'])
def myaccount():
    # Don't show this page if we're not logged in 
    if USERNM.name == None:
        redirect(url_for('board'))

    c, conn = get_db()    
    # get the team members
    c.execute('SELECT name, age, origin_town, ep_no  \
        FROM Team t, Contestant c, Based_on b \
        Where b.team_nm = t.team_nm AND \
        b.contestant_id = c.contestant_id AND user_nm = "{0}"'.format(USERNM.name))
    results = c.fetchall()

    # get the team name
    team_nm=None
    if USERNM.status=='participating':
        c.execute('Select team_nm from team where user_nm=?', [USERNM.name])
        team_nm = c.fetchall()[0]['team_nm']
        # print(team_nm)

    form = DelForm()
    if form.validate_on_submit():
        print("pressed")
        return redirect(url_for('myaccount_delete'))

    return render_template('myaccount.html', results=results, form=form, team_nm=team_nm, user_nm=USERNM.name)

# @app.route("/logout")
@app.route("/myaccount/delete/<username>", methods=['GET', 'POST'])
def myaccount_delete(username):
    # get the form with the buttons
    form = DelForm()
    if form.validate_on_submit():
        if 'delete_btn' in request.form:
            print('Delete request')
            # delete the post
            c, conn = get_db()
            c.execute('DELETE FROM CompUser \
                WHERE user_nm="{}"'.format(username))
            conn.commit()
            
            # reset the username and tell the layout
            USERNM.logout()

            # print log
            print_log()

            return redirect(url_for('login'))
        elif 'cancel_btn' in request.form:
            print('Cancel request')

            # if cancelled, then just redirect
            return redirect(url_for('myaccount'))
        else:
            print("That didn't work!")

    return render_template('delete.html', form=form)
#Add create team feature
# if the user is in the CompUser table and not in the Participating user table
# then this feature is available otherwise it is replace with my team
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # get the form with the buttons
    form = LogoutForm()
    if form.validate_on_submit():
        if 'logout_btn' in request.form:
            # print('Delete request')
            # delete the post
            USERNM.logout()
        elif 'cancel_btn' in request.form:
            pass
            # if cancelled, then just redirect            
        else:
            print("That didn't work!")

        return redirect(url_for('board'))

    return render_template('logout.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)