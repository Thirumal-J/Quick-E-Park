--drop table tbl_parkdetails;

--drop table tbl_vehicles;

--drop table tbl_history;

--drop table tbl_penalty;

--drop table tbl_User;

-- create table tbl_User (UID SERIAL PRIMARY KEY,Name varchar,Surname varchar,Email varchar,Password varchar,mobileno int,ActiveStatus bit,RegDate date);

-- create table tbl_parkdetails (UID int,ParkingActive bit,ParkingStartDate date, ParkingEndDate date,ParkingLocation varchar,ParkingFare int, ParkedCarRegNo varchar,CONSTRAINT fk_useridpark FOREIGN KEY(UID) REFERENCES tbl_User(UID));

-- create table tbl_vehicles (UID int,CarRegistrationNo varchar, CurrentActive bit,CONSTRAINT fk_useridvhcl FOREIGN KEY(UID) REFERENCES tbl_User(UID));

-- create table tbl_history (UID int, Name varchar,Surname varchar,Email varchar,ParkingStartDate date, ParkingEndDate date,ParkingLocation varchar,ParkingFare int,ParkedCarRegNo varchar,CONSTRAINT fk_useridhist FOREIGN KEY(UID) REFERENCES tbl_User(UID));

-- create table tbl_penalty (UID int,ParkingFine int,FineDate date,CONSTRAINT fk_useridfine FOREIGN KEY(UID) REFERENCES tbl_User(UID));

select * from tbl_User;

select * from tbl_parkdetails;


--insert into tbl_user (name,surname,email,password) values('Sheharaz','sheik','sheharaz07@gmail.com','Password')