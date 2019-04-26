CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE competition
(comp_nm varchar(255),
first_bonus int,
second_bonus int,
primary key (comp_nm));
CREATE TABLE users
( user_nm varchar(255), /*Username is of type varchar (variable character field) and has a length of 255 (can hold 0 - 255 characters)*/
email varchar(255),
PRIMARY KEY (user_nm) /*Each user can be identified with their username*/
);
CREATE TABLE FantasyCompetition
(comp_nm varchar(255),
first_bonus INT,
second_bonus INT,
season_no INT,
primary key (comp_nm),
foreign key (season_no) references season);
CREATE TABLE CompUser
(user_nm varchar(255), 
email varchar(255),
PRIMARY KEY (user_nm)
);
CREATE TABLE ParticipatingUser
(user_nm varchar(255), 
primary key (user_nm),
CONSTRAINT fk_user
    FOREIGN KEY (user_nm)
    REFERENCES CompUser(user_nm)
    ON DELETE CASCADE    
);
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
CREATE TABLE Series
(series_nm varchar(255),
origin_country varchar(255),
primary key (series_nm));
CREATE TABLE Season
(season_no INT,
season_nm varchar(255),
host_country varchar(255),
presenter_nm varchar(255),
series_nm VARCHAR(255),
primary key (season_no),
foreign key (series_nm) REFERENCES Series);
CREATE TABLE Episode
(ep_no INT,
season_no INT,
ep_nm varchar(255),
PRIMARY KEY (ep_no, season_no),
foreign key (season_no) references Season);
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
CREATE TABLE Based_on
(team_nm varchar(255),
contestant_id int,
primary key (team_nm, contestant_id),
foreign key (team_nm) references Team,
foreign key (contestant_id) references Contestant);
CREATE TABLE Blog
(time_  DATETIME, 
user_nm varchar(255),
comp_nm varchar(255),
post varchar(255),
PRIMARY KEY (time_, user_nm, comp_nm),
constraint fk_user
    FOREIGN KEY (user_nm)
    REFERENCES CompUser
    on delete cascade,
constraint fk_comp
    FOREIGN KEY (comp_nm)
    references FantasyCompetition
    on delete cascade
);
CREATE TABLE From_previous (
contestant_id INT,
season_no INT,
FOREIGN KEY (season_no) REFERENCES Season,
FOREIGN KEY (contestant_id) REFERENCES Contestant
);
