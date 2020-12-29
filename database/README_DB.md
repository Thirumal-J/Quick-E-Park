<<<<<<< HEAD
# Read me file for Database

=======
>>>>>>> 817e26c873335096ee4917446a6fc2ff8d02051f
-- drop view tbl_getparkdetails;
-- drop table tbl_parkdetails;
-- drop table tbl_vehicles;
-- drop table tbl_history;
-- drop table tbl_penalty;
-- drop table tbl_User;
--create table tbl_User (UID SERIAL PRIMARY KEY,Name varchar,Surname varchar,Email varchar UNIQUE NOT NULL,Password varchar,mobileno int,licenseno varchar UNIQUE NOT NULL,ActiveStatus bit,RegDate TIMESTAMP default now());
-- create table tbl_parkdetails (UID int,ParkingActive bit,ParkingStartDate TIMESTAMP, ParkingEndDate TIMESTAMP,ParkingLocation varchar,ParkingFare decimal, ParkedCarRegNo varchar, parkingEmail varchar NOT NULL,CONSTRAINT fk_useridpark FOREIGN KEY(UID) REFERENCES tbl_User(UID));
-- create table tbl_vehicles (UID int,CarRegistrationNo varchar, CurrentActive bit, vehicleType varchar,CONSTRAINT fk_useridvhcl FOREIGN KEY(UID) REFERENCES tbl_User(UID));
-- create table tbl_history (UID int, Name varchar,Surname varchar,Email varchar,ParkingStartDate TIMESTAMP, ParkingEndDate TIMESTAMP,ParkingLocation varchar,ParkingFare int,ParkedCarRegNo varchar,CONSTRAINT fk_useridhist FOREIGN KEY(UID) REFERENCES tbl_User(UID));
-- create table tbl_penalty (UID int,ParkingFine decimal,FineDate TIMESTAMP, paidstatus bit,CONSTRAINT fk_useridfine FOREIGN KEY(UID) REFERENCES tbl_User(UID));
insert into tbl_penalty values('1',1.5, '2020-12-25 15:34:55.352255')
select * from tbl_parkdetails
select * from tbl_penalty
drop view uv_getparkdetails
SELECT extract(epoch from ('2020-12-25 10:49:33.372601'-now()) / 60 )
--drop view uv_getparkdetails
select * from tbl_parkdetails where parkingactive in('1') --and uid=1--2020-12-28 16:26:30.673632
select * from uv_getparkdetails
delete from tbl_parkdetails where parkedcarregno='lalalalagla'
select cast('2020-12-25 09:49:33.372601'-now() as decimal) as time
select extract(minutes from '2020-12-25 09:49:33.372601'-now())
--create view uv_getparkdetails as select uid,parkingstartdate,case when (extract(epoch from (parkingenddate-now()) / 60 )<0) then '0' else extract(epoch from (parkingenddate-now()) / 60)  end as timeremaining,parkinglocation,parkingfare,parkedcarregno, parkingEmail from tbl_parkdetails where parkingactive in('1') --and uid=1
select parkingstartdate,timeremaining,parkinglocation,parkingfare,parkedcarregno from uv_getparkdetails where uid in ('1')
select floor(1.5)
--delete from tbl_parkdetails
select * from tbl_history
--select * from tbl_User;
--select * from tbl_parkdetails;
--insert into tbl_parkdetails(uid,parkingstartdate) values(1,now())
--select now()
--SELECT now() + interval '1' minute * 1
--insert into tbl_user (name,surname,email,password) values('Sheharaz2','sheik','sheharaz207@gmail.com','Password')

--drop table tbl_vehicles
select * from tbl_vehicles
--insert into tbl_vehicles values (4,'DE YY1235','1','temporary')

select * from tbl_penalty
