-- DATABASE SCHEMA

create database "kominfo_test_db";


-- TABLE USERS

create table "users" (
	id serial primary key,
	username varchar(50),
	email varchar(50),
	password varchar(50),
	created_at timestamp default current_timestamp,
	updated_at timestamp default current_timestamp
)

-- TRIGGER UPDATE TO SET TIMESTAMP ON USERS TABLE

create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = current_timestamp;
    return new;
end;
$$ LANGUAGE plpgsql;

create trigger trigger_set_updated_at before update on "users" for each row execute function set_updated_at();
	
-- INSERT DATA USERS

insert into "users" (username, email, password) values
	('Andi', 'andi@andi.com', '12345'),
	('Budi', 'budi@budi.com', '67890'),
	('Caca', 'caca@caca.com', 'abcde'),
	('Deni', 'deni@deni.com', 'fghij'),
	('Euis', 'euis@euis.com', 'klmno'),
	('Fafa', 'fafa@fafa.com', 'pqrst');


-- TABLE COURSES

create table "courses" (
	id serial primary key,
	course varchar(50),
	mentor varchar(50),
	title varchar(50)
);

-- INSERT DATA COURSES

insert into "courses" (course, mentor, title) values 
	('C++', 'Ari', 'Dr.'),
	('C#', 'Ari', 'Dr.'),
	('C#', 'Ari', 'Dr.'),
	('CSS', 'Cania', 'S.Kom'),
	('HTML', 'Cania', 'S.Kom'),
	('JavaScript', 'Cania', 'S.Kom'),
	('Python', 'Barry', 'S.T'),
	('Micropython', 'Barry', 'S.T'),
	('Java', 'Darren', 'M.T'),
	('Ruby', 'Darren', 'M.T');


-- TABLE USERCOURSE

create table "userCourse" (
	id_user int,
	id_course int,
	foreign key(id_user) references "users"(id),
	foreign key(id_course) references "courses"(id)
);

-- INSERT DATA USERCOURSE

insert into "usercourse" values
	(1, 1),
	(1, 2),
	(1, 3),
	(2, 4),
	(2, 5),
	(2, 6),
	(3, 7),
	(3, 8),
	(3, 9),
	(4, 1),
	(4, 3),
	(4, 5),
	(5, 2),
	(5, 4),
	(5, 6),
	(6, 7),
	(6, 8),
	(6, 9);
	

-- SELECTION QUERIES

select u.id, u.username, c.course, c.mentor, c.title from usercourse uc
	join users u on u.id = uc.id_user 
	join courses c on c.id = uc.id_course;
	
-- GELAR MENTOR SARJANA
select u.id, u.username, c.course, c.mentor, c.title from usercourse uc
	join users u on u.id = uc.id_user 
	join courses c on c.id = uc.id_course
	where c.title ilike 's.%';

-- GELAR MENTOR BUKAN SARJANA
select u.id, u.username, c.course, c.mentor, c.title from usercourse uc
	join users u on u.id = uc.id_user 
	join courses c on c.id = uc.id_course
	where c.title not ilike 's.%';

-- TOTAL PESERTA
select c.course, c.mentor, c.title, count(u.id) as "jumlah_peserta" from usercourse uc
	join courses c on c.id = uc.id_course 
	join users u on u.id = uc.id_user
	group by c.course, c.mentor, c.title
    order by c.mentor;

-- TOTAL FEE
select c.mentor, count(u.id) as "jumlah_peserta", count(u.id) * 2000000 as "total_fee"
from usercourse uc
	join courses c on c.id = uc.id_course 
	join users u on u.id = uc.id_user
	group by c.mentor
    order by "total_fee" desc, c.mentor;


-- KEBUTUHAN ADMIN DAN USER BIASA

create table "roles" (id serial primary key, role varchar(50));

insert into "roles" values (1, 'ADMIN'), (2, 'USER');

alter table "users" add column "id_role" int;

alter table "users" add constraint fk_role foreign key (id_role) references roles(id);
