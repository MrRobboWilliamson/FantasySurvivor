PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE competition
(comp_nm varchar(255),
first_bonus int,
second_bonus int,
primary key (comp_nm));
INSERT INTO competition VALUES('Milton Crew',10,5);
CREATE TABLE users
( user_nm varchar(255), /*Username is of type varchar (variable character field) and has a length of 255 (can hold 0 - 255 characters)*/
email varchar(255),
PRIMARY KEY (user_nm) /*Each user can be identified with their username*/
);
INSERT INTO users VALUES('BigJase','bigjase@gmail.com');
INSERT INTO users VALUES('Janosity','jane@gmail.com');
INSERT INTO users VALUES('Davos','davos@gmail.com');
INSERT INTO users VALUES('Testicles','tess@gmail.com');
INSERT INTO users VALUES('Rambo','rambo@gmail.com');
INSERT INTO users VALUES('Sarah','sarah@gmail.com');
CREATE TABLE participant
(unm varchar(255), 
primary key (unm),
FOREIGN key (unm) REFERENCES users);
INSERT INTO participant VALUES('BigJase');
INSERT INTO participant VALUES('Janosity');
INSERT INTO participant VALUES('Davos');
INSERT INTO participant VALUES('Tess');
INSERT INTO participant VALUES('Rambo');
INSERT INTO participant VALUES('Sarah');
CREATE TABLE blogs
(time_  DATETIME, 
unm varchar(255),
-- cnm varchar(255),
content varchar(255),
PRIMARY KEY (time_)
-- PRIMARY KEY (time_, unm, cnm)
-- FOREIGN KEY unm REFERENCES users,
-- FOREIGN KEY
);
CREATE TABLE FantasyCompetition
(comp_nm varchar(255),
first_bonus INT,
second_bonus INT,
season_no INT,
primary key (comp_nm),
foreign key (season_no) references season);
INSERT INTO FantasyCompetition VALUES('Milton Crew',10,5,38);
CREATE TABLE CompUser
(user_nm varchar(255), 
email varchar(255),
PRIMARY KEY (user_nm)
);
INSERT INTO CompUser VALUES('BigJase','bigjase@gmail.com');
INSERT INTO CompUser VALUES('Janosity','jane@gmail.com');
INSERT INTO CompUser VALUES('Davos','davos@gmail.com');
INSERT INTO CompUser VALUES('Tess','tess@gmail.com');
INSERT INTO CompUser VALUES('Rambo','rambo@gmail.com');
INSERT INTO CompUser VALUES('Sarah','sarah@gmail.com');
CREATE TABLE ParticipatingUser
(user_nm varchar(255), 
primary key (user_nm),
FOREIGN key (user_nm) REFERENCES CompUser);
INSERT INTO ParticipatingUser VALUES('BigJase');
INSERT INTO ParticipatingUser VALUES('Janosity');
INSERT INTO ParticipatingUser VALUES('Davos');
INSERT INTO ParticipatingUser VALUES('Tess');
INSERT INTO ParticipatingUser VALUES('Rambo');
INSERT INTO ParticipatingUser VALUES('Sarah');
CREATE TABLE Team
(team_nm varchar(255),
user_nm varchar(255),
comp_nm varchar(255),
primary key (team_nm),
foreign key (user_nm) REFERENCES ParticipatingUser,
FOReign key (comp_nm) REFERENCES FantasyCompetition);
INSERT INTO Team VALUES('Volume','BigJase','Milton Crew');
INSERT INTO Team VALUES('Wind','Janosity','Milton Crew');
INSERT INTO Team VALUES('Water','Davos','Milton Crew');
INSERT INTO Team VALUES('Fire','Tess','Milton Crew');
INSERT INTO Team VALUES('Earth','Rambo','Milton Crew');
INSERT INTO Team VALUES('Veracity','Sarah','Milton Crew');
CREATE TABLE Series
(series_nm varchar(255),
origin_country varchar(255),
primary key (series_nm));
INSERT INTO Series VALUES('Survivor (U.S. TV Series)','United States');
CREATE TABLE Season
(season_no INT,
season_nm varchar(255),
host_country varchar(255),
presenter_nm varchar(255),
series_nm VARCHAR(255),
primary key (season_no),
foreign key (series_nm) REFERENCES Series);
INSERT INTO Season VALUES(38,'Edge of Extinction','Fiji','Jeff Probst','Survivor (U.S. TV Series)');
CREATE TABLE Episode
(ep_no INT,
season_no INT,
ep_nm varchar(255),
PRIMARY KEY (ep_no, season_no),
foreign key (season_no) references Season);
INSERT INTO Episode VALUES(1,38,'It Smells Like Success');
INSERT INTO Episode VALUES(2,38,'One of Us is Going to Win the War');
INSERT INTO Episode VALUES(3,38,'Betrayals Are Going to Get Exposed');
INSERT INTO Episode VALUES(4,38,'I Need a Dance Partner');
INSERT INTO Episode VALUES(5,38,'It''s Like the Worst Cocktail Party Ever');
INSERT INTO Episode VALUES(6,38,'There’s Always a Twist');
INSERT INTO Episode VALUES(7,38,'I’m the Puppet Master');
INSERT INTO Episode VALUES(8,38,'Y''all Making Me Crazy');
INSERT INTO Episode VALUES(9,38,'Blood of a Blindside');
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
INSERT INTO Contestant VALUES(17,'Reem Daly',46,NULL,'Ashburn, Virginia',38,1,NULL);
INSERT INTO Contestant VALUES(18,'Keith Sowell',19,NULL,'Durham, North Carolina',38,2,NULL);
INSERT INTO Contestant VALUES(19,'Chris Underwood',25,NULL,'Greenville, South Carolina',38,3,NULL);
INSERT INTO Contestant VALUES(20,'Aubry Bracco',32,NULL,'Los Angeles, California',38,5,NULL);
INSERT INTO Contestant VALUES(21,'Wendy Diaz',25,NULL,'Bell, California',38,6,NULL);
INSERT INTO Contestant VALUES(22,'Joe Anglim',29,NULL,'Ogden, Utah',38,7,NULL);
INSERT INTO Contestant VALUES(23,'Eric Hafemann',35,NULL,'Livermore, California',38,8,NULL);
INSERT INTO Contestant VALUES(24,'Julia Carter',25,NULL,'Bethesda, Maryland',38,9,NULL);
INSERT INTO Contestant VALUES(25,'Aurora McCreary',32,NULL,'Orlando, Florida',38,NULL,NULL);
INSERT INTO Contestant VALUES(26,'Dan Wardog DaSilva',38,NULL,'Los Angeles, California',38,NULL,NULL);
INSERT INTO Contestant VALUES(27,'Gavin Whitson',23,NULL,'Erwin, Tennessee',38,NULL,NULL);
INSERT INTO Contestant VALUES(28,'Julie Rosenberg',46,NULL,'New York City, New York',38,NULL,NULL);
INSERT INTO Contestant VALUES(29,'Lauren O''Connell',21,NULL,'Waco, Texas',38,NULL,NULL);
INSERT INTO Contestant VALUES(30,'Rick Devens',33,NULL,'Macon, Georgia',38,NULL,NULL);
INSERT INTO Contestant VALUES(31,'Ron Clark',45,NULL,'Atlanta, Georgia',38,NULL,NULL);
INSERT INTO Contestant VALUES(32,'Victoria Baamonde',23,NULL,'Bronx, New York',38,NULL,NULL);
CREATE TABLE Based_on
(team_nm varchar(255),
contestant_id int,
primary key (team_nm, contestant_id),
foreign key (team_nm) references Team,
foreign key (contestant_id) references Contestant);
INSERT INTO Based_on VALUES('Volume',19);
INSERT INTO Based_on VALUES('Volume',27);
INSERT INTO Based_on VALUES('Volume',17);
INSERT INTO Based_on VALUES('Volume',31);
INSERT INTO Based_on VALUES('Wind',19);
INSERT INTO Based_on VALUES('Wind',20);
INSERT INTO Based_on VALUES('Wind',28);
INSERT INTO Based_on VALUES('Wind',27);
INSERT INTO Based_on VALUES('Water',22);
INSERT INTO Based_on VALUES('Water',24);
INSERT INTO Based_on VALUES('Water',19);
INSERT INTO Based_on VALUES('Water',29);
INSERT INTO Based_on VALUES('Fire',29);
INSERT INTO Based_on VALUES('Fire',25);
INSERT INTO Based_on VALUES('Fire',30);
INSERT INTO Based_on VALUES('Fire',26);
INSERT INTO Based_on VALUES('Earth',22);
INSERT INTO Based_on VALUES('Earth',31);
INSERT INTO Based_on VALUES('Earth',19);
INSERT INTO Based_on VALUES('Earth',18);
INSERT INTO Based_on VALUES('Veracity',23);
INSERT INTO Based_on VALUES('Veracity',20);
INSERT INTO Based_on VALUES('Veracity',32);
INSERT INTO Based_on VALUES('Veracity',28);
CREATE TABLE Blog
(time_  DATETIME, 
user_nm varchar(255),
comp_nm varchar(255),
post varchar(255),
PRIMARY KEY (time_, user_nm, comp_nm),
FOREIGN KEY (user_nm) REFERENCES CompUser,
FOREIGN KEY (comp_nm) references FantasyCompetition
);
CREATE TABLE From_previous (
contestant_id INT,
season_no INT,
FOREIGN KEY (season_no) REFERENCES Season,
FOREIGN KEY (contestant_id) REFERENCES Contestant
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Contestant',32);
COMMIT;
