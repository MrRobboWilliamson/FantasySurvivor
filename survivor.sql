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
INSERT INTO CompUser VALUES('Janosity','jane@gmail.com');
INSERT INTO CompUser VALUES('Davos','davos@gmail.com');
INSERT INTO CompUser VALUES('Tess','tess@gmail.com');
INSERT INTO CompUser VALUES('Rambo','rambo@gmail.com');
INSERT INTO CompUser VALUES('Sarah','sarah@gmail.com');
INSERT INTO CompUser VALUES('BigJase','bigjase@gmail.com');
INSERT INTO CompUser VALUES('Roberto','reob@gamil.com');
INSERT INTO CompUser VALUES('Bob','bob@burgers.com');
INSERT INTO CompUser VALUES('Ronda','ronda@gmail.com');
INSERT INTO CompUser VALUES('NewUser','new@user.com');
CREATE TABLE ParticipatingUser
(user_nm varchar(255), 
primary key (user_nm),
CONSTRAINT fk_user
    FOREIGN KEY (user_nm)
    REFERENCES CompUser(user_nm)
    ON DELETE CASCADE    
);
INSERT INTO ParticipatingUser VALUES('Janosity');
INSERT INTO ParticipatingUser VALUES('Davos');
INSERT INTO ParticipatingUser VALUES('Tess');
INSERT INTO ParticipatingUser VALUES('Rambo');
INSERT INTO ParticipatingUser VALUES('Sarah');
INSERT INTO ParticipatingUser VALUES('BigJase');
CREATE TABLE Team
(team_nm varchar(255),
user_nm varchar(255),
comp_nm varchar(255),
primary key (team_nm),
constraint fk_user
    foreign key (user_nm)
    REFERENCES ParticipatingUser(user_nm)
    on delete cascade,
constraint fk_comp
    FOReign key (comp_nm)
    REFERENCES FantasyCompetition(comp_nm)
    on delete cascade
);
INSERT INTO Team VALUES('Wind','Janosity','Milton Crew');
INSERT INTO Team VALUES('Water','Davos','Milton Crew');
INSERT INTO Team VALUES('Fire','Tess','Milton Crew');
INSERT INTO Team VALUES('Earth','Rambo','Milton Crew');
INSERT INTO Team VALUES('Veracity','Sarah','Milton Crew');
INSERT INTO Team VALUES('Bushermans','BigJase','Milton Crew');
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
INSERT INTO Episode VALUES(10,38,'Fasten Your Seatbelts');
INSERT INTO Episode VALUES(11,38,'Awkward');
INSERT INTO Episode VALUES(12,38,'Idol or Bust');
INSERT INTO Episode VALUES(13,38,'I See The Million Dollars');
INSERT INTO Episode VALUES(14,38,'Reunion Special');
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
INSERT INTO Contestant VALUES(1513,'Reem Daly',46,NULL,'Ashburn, Virginia',38,1,NULL);
INSERT INTO Contestant VALUES(1514,'Keith Sowell',19,NULL,'Durham, North Carolina',38,2,NULL);
INSERT INTO Contestant VALUES(1515,'Aubry Bracco',32,NULL,'Los Angeles, California',38,5,NULL);
INSERT INTO Contestant VALUES(1516,'Wendy Diaz',25,NULL,'Bell, California',38,6,NULL);
INSERT INTO Contestant VALUES(1517,'Joe Anglim',29,NULL,'Ogden, Utah',38,7,NULL);
INSERT INTO Contestant VALUES(1518,'Eric Hafemann',35,NULL,'Livermore, California',38,8,NULL);
INSERT INTO Contestant VALUES(1519,'Julia Carter',25,NULL,'Bethesda, Maryland',38,9,NULL);
INSERT INTO Contestant VALUES(1520,'David Wright',44,NULL,'Sherman Oaks, California',38,10,NULL);
INSERT INTO Contestant VALUES(1521,'Kelley Wentworth',31,NULL,'Seattle, Washington',38,11,NULL);
INSERT INTO Contestant VALUES(1522,'Dan Wardog DaSilva',38,NULL,'Los Angeles, California',38,12,NULL);
INSERT INTO Contestant VALUES(1523,'Ron Clark',45,NULL,'Atlanta, Georgia',38,13,NULL);
INSERT INTO Contestant VALUES(1524,'Aurora McCreary',32,NULL,'Orlando, Florida',38,14,NULL);
INSERT INTO Contestant VALUES(1525,'Victoria Baamonde',23,NULL,'Bronx, New York',38,15,NULL);
INSERT INTO Contestant VALUES(1526,'Lauren O''Connell',21,NULL,'Waco, Texas',38,16,NULL);
INSERT INTO Contestant VALUES(1527,'Chris Underwood',25,NULL,'Greenville, South Carolina',38,NULL,NULL);
INSERT INTO Contestant VALUES(1528,'Gavin Whitson',23,NULL,'Erwin, Tennessee',38,NULL,NULL);
INSERT INTO Contestant VALUES(1529,'Julie Rosenberg',46,NULL,'New York City, New York',38,NULL,NULL);
INSERT INTO Contestant VALUES(1530,'Rick Devens',33,NULL,'Macon, Georgia',38,NULL,NULL);
CREATE TABLE Based_on
(team_nm varchar(255),
contestant_id int,
primary key (team_nm, contestant_id),
constraint fk_team
    foreign key (team_nm)
    references Team(team_nm)
    on delete cascade,
foreign key (contestant_id) references Contestant);
INSERT INTO Based_on VALUES('Wind',1523);
INSERT INTO Based_on VALUES('Wind',1518);
INSERT INTO Based_on VALUES('Wind',1529);
INSERT INTO Based_on VALUES('Wind',1530);
INSERT INTO Based_on VALUES('Water',1517);
INSERT INTO Based_on VALUES('Water',1528);
INSERT INTO Based_on VALUES('Water',1515);
INSERT INTO Based_on VALUES('Water',1519);
INSERT INTO Based_on VALUES('Fire',1515);
INSERT INTO Based_on VALUES('Fire',1514);
INSERT INTO Based_on VALUES('Fire',1524);
INSERT INTO Based_on VALUES('Fire',1519);
INSERT INTO Based_on VALUES('Earth',1518);
INSERT INTO Based_on VALUES('Earth',1527);
INSERT INTO Based_on VALUES('Earth',1515);
INSERT INTO Based_on VALUES('Earth',1514);
INSERT INTO Based_on VALUES('Veracity',1513);
INSERT INTO Based_on VALUES('Veracity',1515);
INSERT INTO Based_on VALUES('Veracity',1530);
INSERT INTO Based_on VALUES('Veracity',1516);
INSERT INTO Based_on VALUES('Bushermans',1516);
INSERT INTO Based_on VALUES('Bushermans',1523);
INSERT INTO Based_on VALUES('Bushermans',1520);
INSERT INTO Based_on VALUES('Bushermans',1518);
CREATE TABLE Blog
(time_  DATETIME, 
user_nm varchar(255),
comp_nm varchar(255),
post varchar(255),
PRIMARY KEY (time_, user_nm, comp_nm),
constraint fk_user
    FOREIGN KEY (user_nm)
    REFERENCES CompUser(user_nm)
    on delete cascade,
constraint fk_comp
    FOREIGN KEY (comp_nm)
    references FantasyCompetition(comp_nm)
    on delete cascade
);
INSERT INTO Blog VALUES('2019/05/18 13:10:08','Rambo','Milton Crew','Hi');
CREATE TABLE From_previous
(contestant_id INT,
season_no INT,
FOREIGN KEY (season_no) REFERENCES Season,
FOREIGN KEY (contestant_id) REFERENCES Contestant
);
CREATE TABLE user_log (user_nm varchar(255), timestamp datetime, email varchar(255), action varchar(255),primary key (user_nm, timestamp));
INSERT INTO user_log VALUES('Bubble','2019-05-23 20:04:00','bubble@soap.com','user_created');
INSERT INTO user_log VALUES('NewUser','2019-05-23 20:05:48','new@user.com','user_created');
INSERT INTO user_log VALUES('Browser','2019-05-23 20:07:18','brows@gmail.com','user_created');
INSERT INTO user_log VALUES('Browser','2019-05-23 20:08:52','brows@gmail.com','user_created');
INSERT INTO user_log VALUES('NewGirl','2019-05-23 20:19:40','new@girl.com','user_created');
INSERT INTO user_log VALUES('NewGirl','2019-05-23 20:20:00','new@girl.com','user_deleted');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('Contestant',1530);


CREATE TRIGGER user_log_insert after insert on CompUser
begin
insert into user_log(user_nm, timestamp, email, action)
    values(
    NEW.user_nm,
    strftime('%Y-%m-%d %H:%M:%S', 'now'),
    NEW.email,
    "user_created");
    end;

CREATE TRIGGER user_log_delete after delete on CompUser
begin
insert into user_log(user_nm, timestamp, email , action)
    values (
    old.user_nm,
    strftime('%Y-%m-%d %H:%M:%S', 'now'),
    old.email,
    'user_deleted');
    end;
    
COMMIT;
