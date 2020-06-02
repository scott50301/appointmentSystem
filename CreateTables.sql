CREATE TABLE Users (
    ID INT NOT NULL AUTO_INCREMENT,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    phone BIGINT NOT NULL,
    email varchar(255),
  	 PRIMARY KEY (ID)
);

CREATE TABLE timeSlots (
    ID INT NOT NULL AUTO_INCREMENT,
    slots TIME,
    `date` DATE NOT NULL,
    timeout DATETIME,
	`status` TINYINT DEFAULT 0,
	userId INT,
  	PRIMARY KEY (ID),
  	FOREIGN KEY (userId) REFERENCES Users(ID)
);

INSERT INTO timeslots (slots, `date`)
VALUES ('8:00:00','2020-06-07'),
 ('9:00:00','2020-06-07'),
 ('10:00:00','2020-06-07'),
 ('11:00:00','2020-06-07'),
 ('12:00:00','2020-06-07'),
 ('9:00:00','2020-06-08'),
 ('10:00:00','2020-06-08'),
 ('11:00:00','2020-06-08'),
 ('12:00:00','2020-06-08'),
 ('9:00:00','2020-06-09'),
 ('10:00:00','2020-06-09'),
 ('11:00:00','2020-06-09'),
 ('12:00:00','2020-06-09');