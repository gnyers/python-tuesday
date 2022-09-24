PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
            id integer PRIMARY KEY AUTOINCREMENT,
            fname varchar(40),
            sname varchar(60),
            email varchar(255)
    );
INSERT INTO users VALUES(1,'John','Doe','jdoe@example.com');
INSERT INTO users VALUES(2,'Jane','Brown','jane.brown@example.com');
INSERT INTO users VALUES(3,'Frank','Green','frankg@example.com');
INSERT INTO users VALUES(4,'Eileen','Smith','eileeng@example.com');
INSERT INTO users VALUES(5,'George','Moss','moss@example.com');
CREATE TABLE projects (
            id integer PRIMARY KEY AUTOINCREMENT,
            name varchar(140)
    );
INSERT INTO projects VALUES(1,'Project Roadrunner @ACMECo');
INSERT INTO projects VALUES(2,'Webshop Implementation @ACMECo');
INSERT INTO projects VALUES(3,'Security Audit @ACMECo');
CREATE TABLE bookings (
            id integer PRIMARY KEY AUTOINCREMENT,
            user integer,
            project integer,
            date datetime,
            hours numerical,
            remarks varchar,
            FOREIGN KEY (user) REFERENCES users (id),
            FOREIGN KEY (project) REFERENCES users (id)
    );
INSERT INTO bookings VALUES(1,4,2,'2019-09-02',8,'Landingpage design');
INSERT INTO bookings VALUES(2,4,2,'2019-09-03',6,'Landingpage design');
INSERT INTO bookings VALUES(3,4,1,'2019-09-03',2,'Requirement analysis');
INSERT INTO bookings VALUES(4,4,4,'2019-09-04',8,'Verify inventory');
INSERT INTO bookings VALUES(5,4,1,'2019-09-05',2,'Planning review');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',5);
INSERT INTO sqlite_sequence VALUES('projects',3);
INSERT INTO sqlite_sequence VALUES('bookings',5);
COMMIT;
