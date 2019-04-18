/*If tables with the name 'users' and 'blogs' already exist, then delete them.*/
drop table if exists FantasyCompetition;
drop table if exists CompUser;
drop table if exists ParticipatingUser;
drop table if exists Team;
drop table if exists Series;
drop table if exists Season;
drop table if exists Blog;
drop table if exists Contestant;
drop table if exists Based_on;
drop table if exists Episode;
drop table if exists From_previous;


/* fantasy competition */
create table FantasyCompetition
(comp_nm varchar(255),
first_bonus INT,
second_bonus INT,
season_no INT,
primary key (comp_nm),
foreign key (season_no) references season);

/* users */
CREATE TABLE CompUser
(user_nm varchar(255), 
email varchar(255),
PRIMARY KEY (user_nm)
);

/* participant */
create table ParticipatingUser
(user_nm varchar(255), 
primary key (user_nm),
FOREIGN key (user_nm) REFERENCES CompUser);

/* team */
create table Team
(team_nm varchar(255),
user_nm varchar(255),
comp_nm varchar(255),
primary key (team_nm),
foreign key (user_nm) REFERENCES ParticipatingUser,
FOReign key (comp_nm) REFERENCES FantasyCompetition);

/* series table */
Create Table Series
(series_nm varchar(255),
origin_country varchar(255),
primary key (series_nm));

/* season table */
Create Table Season
(season_no INT,
season_nm varchar(255),
host_country varchar(255),
presenter_nm varchar(255),
series_nm VARCHAR(255),
primary key (season_no),
foreign key (series_nm) REFERENCES Series);

/* episode */
create table Episode
(ep_no INT,
season_no INT,
ep_nm varchar(255),
PRIMARY KEY (ep_no, season_no),
foreign key (season_no) references Season);

/*Create the 'contestants' table*/
CREATE TABLE Contestant
(contestant_id INTEGER PRIMARY KEY AUTOINCREMENT, 
name varchar(255),
age INT,
sex char(15),
origin_town varchar(255),
season_no INT,
ep_no INT,
position_out INT,
foreign key (season_no) references Season,
foreign key (ep_no) references Episode
);

/* based on */
create table Based_on
(team_nm varchar(255),
contestant_id int,
primary key (team_nm, contestant_id),
foreign key (team_nm) references Team,
foreign key (contestant_id) references Contestant);

/*Create the 'blogs' table*/
CREATE TABLE Blog
(time_  DATETIME, 
user_nm varchar(255),
comp_nm varchar(255),
post varchar(255),
PRIMARY KEY (time_, user_nm, comp_nm),
FOREIGN KEY (user_nm) REFERENCES CompUser,
FOREIGN KEY (comp_nm) references FantasyCompetition
);

/*Create the 'blogs' table*/
CREATE TABLE From_previous (
contestant_id INT,
season_no INT,
FOREIGN KEY (season_no) REFERENCES Season,
FOREIGN KEY (contestant_id) REFERENCES Contestant
);

/*Add users, teams, a competition, a series and season, and teams to database*/
/* users */
Insert into CompUser values ('BigJase', 'bigjase@gmail.com');
Insert into CompUser values ('Janosity', 'jane@gmail.com');
Insert into CompUser values ('Davos', 'davos@gmail.com');
Insert into CompUser values ('Tess', 'tess@gmail.com');
Insert into CompUser values ('Rambo', 'rambo@gmail.com');
Insert into CompUser values ('Sarah', 'sarah@gmail.com');

/* participant */ 
Insert into ParticipatingUser values ('BigJase');
Insert into ParticipatingUser values ('Janosity');
Insert into ParticipatingUser values ('Davos');
Insert into ParticipatingUser values ('Tess');
Insert into ParticipatingUser values ('Rambo');
Insert into ParticipatingUser values ('Sarah');

/* competition */
Insert into FantasyCompetition values ('Milton Crew', 10, 5, 38);

/* series, season */ 
Insert into Series values ('Survivor (U.S. TV Series)', 'United States');
Insert into Season values (38, 'Edge of Extinction', 'Fiji', 'Jeff Probst', 'Survivor (U.S. TV Series)');

/* teams */
Insert into Team values ('Volume', 'BigJase', 'Milton Crew');
Insert into Team values ('Wind', 'Janosity', 'Milton Crew');
Insert into Team values ('Water', 'Davos', 'Milton Crew');
Insert into Team values ('Fire', 'Tess', 'Milton Crew');
Insert into Team values ('Earth', 'Rambo', 'Milton Crew');
Insert into Team values ('Veracity', 'Sarah', 'Milton Crew');

-- Insert into blogs(username, title, content) values ('Jane', 'How to Make Google Docs Look Like Dropbox Paper', 'I love Dropbox Paper. Some people have tons of complaints about it, but I’m not one of those people. It’s one of my favorite tools and I use it for all kinds of work and home documents.');
-- insert into blogs(username, title, content) VALUES ('James', 'The best Data Science courses', 'One of the best courses I have taken is INFS7901');
-- insert into blogs(username, title, content) VALUES ('James', 'How to Build a Data Science Portfolio', 'The best way to build a data science portfolio is to do a project');
-- insert into blogs(username, title, content) VALUES ('Jane', 'Blockchain Could Unlock Vital Funding to Tackle Climate Change', 'Billions of dollars in promised funding is failing to reach the world’s poorest countries — but technologists have a fix in mind .....');
