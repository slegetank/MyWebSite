create table blog
(
`id` int not null auto_increment primary key,
`title` char(100) not null,
`type` char(50) not null,
`writetime` datetime not null,
`desc` varchar(1000),
`filename` char(100) not null,
`lastupdate` int(10) not null,
`image` char(200)
);

insert blog values(NULL, "test1", "emacs", CURRENT_TIMESTAMP, "This is description.", "test", 0);
