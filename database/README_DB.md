-- drop view tbl_getparkdetails;
-- drop table tbl_parkdetails;
-- drop table tbl_vehicles;
-- drop table tbl_history;
-- drop table tbl_penalty;
-- drop table tbl_User;
--create table tbl_User (UID SERIAL PRIMARY KEY,Name varchar,Surname varchar,Email varchar UNIQUE NOT NULL,Password varchar,mobileno int,licenseno varchar UNIQUE NOT NULL,ActiveStatus bit,RegDate TIMESTAMP default now());
-- create table tbl_parkdetails (UID int,ParkingActive bit,ParkingStartDate TIMESTAMP, ParkingEndDate TIMESTAMP,ParkingLocation varchar,ParkingFare decimal, ParkedCarRegNo varchar, parkingEmail varchar NOT NULL,paidStatus bit default '0',CONSTRAINT fk_useridpark FOREIGN KEY(UID) REFERENCES tbl_User(UID));
-- create table tbl_vehicles (UID int,CarRegistrationNo varchar, CurrentActive bit, vehicleType varchar,CONSTRAINT fk_useridvhcl FOREIGN KEY(UID) REFERENCES tbl_User(UID));
-- create table tbl_history (UID int, Name varchar,Surname varchar,Email varchar,ParkingStartDate TIMESTAMP, ParkingEndDate TIMESTAMP,ParkingLocation varchar,ParkingFare int,ParkedCarRegNo varchar, parkingemail varchar,CONSTRAINT fk_useridhist FOREIGN KEY(UID) REFERENCES tbl_User(UID));
-- create table tbl_penalty (UID int,ParkingFine decimal,CarRegistrationNo varchar NOT NULL,FineDate TIMESTAMP, paidstatus bit,CONSTRAINT fk_useridfine FOREIGN KEY(UID) REFERENCES tbl_User(UID));
--create view uv_getparkdetails as select uid,parkingstartdate,case when (extract(epoch from (parkingenddate-now()) / 60 )<0) then '0' else  concat(concat(floor(extract(epoch from (parkingenddate-now()) / 3600)), ' Hours '),concat((mod(cast(floor(extract(epoch from (parkingenddate-now()) / 60)) as int),60) ) , ' minutes'))  end as timeremaining,parkinglocation,concat(parkingfare, ' EUR ') as parkingfare,parkedcarregno, parkingEmail from tbl_parkdetails where parkingactive in('1') --and uid=1
--create view uv_totalfare as (select uid,concat(parkingfare, ' EUR')  as parkingfare from tbl_parkdetails where parkingactive='0' and uid=3 and paidstatus='0' union all select uid,concat(parkingfare, ' EUR') as parkingfare from tbl_history where uid=3 and paidstatus='0')
insert into tbl_penalty values('1',1.5, '2020-12-25 15:34:55.352255')
select * from tbl_parkdetails
select * from tbl_penalty
drop view uv_getparkdetails
SELECT extract(epoch from ('2020-12-25 10:49:33.372601'-now()) / 60 )
--drop view uv_getparkdetails

--select * from tbl_parkdetails;
--insert into tbl_parkdetails(uid,parkingstartdate) values(1,now())
--delete from tbl_parkdetails

--select * from tbl_User;
--insert into tbl_user (name,surname,email,password) values('Sheharaz2','sheik','sheharaz207@gmail.com','Password')

--drop table tbl_vehicles
select * from tbl_vehicles
--insert into tbl_vehicles values (4,'DE YY1235','1','temporary')
select name,surname,email,parkingstartdate,parkingenddate,parkinglocation,parkingfare,parkedcarregno,paidstatus,parkingemail from tbl_penalty where uid in ('3')
select * from (
select parkingfare from tbl_parkdetails where parkingactive='0' and uid=3 and paidstatus='0' union all
select parkingfare from tbl_history where uid=3 and paidstatus='0'
) as parking

select * from tbl_history 
insert into tbl_history values (3 , 'test', 'test', 'test', now(), now(), 'test', 10, 'test', '0', 'test')

select * from uv_totalfare


select * from tbl_penalty


call sp_updateTransactions();


CREATE or replace PROCEDURE sp_updateTransactions()
LANGUAGE SQL
AS $$
update tbl_parkdetails set parkingactive='0' where  floor(extract(epoch from (parkingenddate-now()) / 60))<=0 
$$;

select * from uv_getparkdetails




 select floor(extract(epoch from (parkingenddate-now()) / 60)) from tbl_parkdetails

select * from tbl_parkdetails
select * from tbl_history