drop table if exists user_data;
create table user_data (
  	userid Text NOT NULL,
  	pace_number integer NOT NULL DEFAULT (0),
  	distance Real NOT NULL DEFAULT (0),
  	calorie Real NOT NULL DEFAULT (0),
  	sport_type integer NOT NULL DEFAULT (0),
  	datatime TimeStamp NOT NULL DEFAULT (datetime('now','localtime'))
)