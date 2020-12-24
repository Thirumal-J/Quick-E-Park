# Read me file for Database

--create table tbl_User (UID int PRIMARY KEY,Name varchar,Surname varchar,Email varchar,Password varchar,mobileno int,ActiveStatus bit,RegDate date)
--create table tbl_parkdetails (UID int,ParkingActive bit,ParkingStartDate date, ParkingEndDate date,ParkingLocation varchar,ParkingFare int, ParkedCarRegNo varchar,CONSTRAINT fk_useridpark FOREIGN KEY(UID) REFERENCES tbl_User(UID))
--create table tbl_vehicles (UID int,CarRegistrationNo varchar, CurrentActive bit,CONSTRAINT fk_useridvhcl FOREIGN KEY(UID) REFERENCES tbl_User(UID))
--create table tbl_history (UID int, Name varchar,Surname varchar,Email varchar,ParkingStartDate date, ParkingEndDate date,ParkingLocation varchar,ParkingFare int,ParkedCarRegNo varchar,CONSTRAINT fk_useridhist FOREIGN KEY(UID) REFERENCES tbl_User(UID))
--create table tbl_penalty (UID int,ParkingFine int,FineDate date,CONSTRAINT fk_useridfine FOREIGN KEY(UID) REFERENCES tbl_User(UID))