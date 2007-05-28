import sqlite3

sql = """
                create table song (id INTEGER PRIMARY KEY,
                                   name TEXT,                   /* name of song */
                                   artist TEXT,                 /* artist */
                                   barcount INTEGER,            /* number of bars in song */
                                   difficulty INTEGER,          /* difficulty. EASY, NORMAL, INTERMEDIATE, etc */
                                   songdate TEXT,               /* date of the song's orignal recording */
                                   completed_perc INTEGER,      /* fast % calculation of how much is completed */
                                   status INTEGER,              /* status, STARTED, NOT STARTED, COMPLETED, POSTPONED etc */
                                   lyrics TEXT,                 /* lyrics text */
                                   information TEXT,            /* song information */
                                   tuning_alt TEXT,             /* alternate tuning string, when tuning_id = -1 */
                                   tuning_id INTEGER,           /* ID of table entry of tuning */                         
                                   media_id INTEGER);           /* ID of media, book, CD etc where song is found */
                
                create table songcats (id INTEGER PRIMARY KEY, 
                                       song_id INTEGER,         /* id of song where category is linked to */
                                       category_id INTEGER);    /* id of the category associated with the song */
                
                create table link (id INTEGER PRIMARY KEY, 
                                   song_id INTEGER,             /* id of song where link belongs to */
                                   linktype INTEGER,            /* type of link */
                                   linkpath TEXT);              /* path of link */
                
                create table category (id INTEGER PRIMARY KEY, 
                                      name TEXT);               /* name of category */


                create table tuning (id INTEGER PRIMARY KEY,
                                     tuning_name TEXT,          /* name of tuning */
                                     tuning_text TEXT);         /* tuning text */

                /* categories insertion */                                
                insert into category (name) values ('Travis Picking');
                insert into category (name) values ('Ragtime Blues');
                insert into category (name) values ('Blues');
                insert into category (name) values ('Jazz');
                insert into category (name) values ('Generic Fingerstyle');
                insert into category (name) values ('Classic');
                insert into category (name) values ('Rock');
                insert into category (name) values ('Country');    
                insert into category (name) values ('Downstrokes Picking');
                insert into category (name) values ('Classical Guitar');
                insert into category (name) values ('Flamenco');
                insert into category (name) values ('Guitar Solo Player');
                insert into category (name) values ('Guitar Multiple Players');
                insert into category (name) values ('Guitar Moves');
                insert into category (name) values ('Guitar Lick');
                insert into category (name) values ('Lead Guitar');
                insert into category (name) values ('Rhythm Guitar');
                insert into category (name) values ('Shred Guitar');
                insert into category (name) values ('Slack-key Guitar');
                insert into category (name) values ('Slide Guitar'); 
                 
                /* tuning insertion */                                
                insert into tuning (tuning_name, tuning_text) values ('Standard',     'E  A  D  G  B  E ');
                insert into tuning (tuning_name, tuning_text) values ('Drop D',       'D  A  D  G  B  E ');
                insert into tuning (tuning_name, tuning_text) values ('DADGAD', 	    'D  A  D  G  A  D ');
                insert into tuning (tuning_name, tuning_text) values ('Open E',       'E  B  E  G# B  E ');
                insert into tuning (tuning_name, tuning_text) values ('Open A',       'E  A  E  A  C# E ');
                insert into tuning (tuning_name, tuning_text) values ('Open D',       'D  A  D  F# A  D ');   
                insert into tuning (tuning_name, tuning_text) values ('Open G',       'D  G  D  G  B  D ');   
                insert into tuning (tuning_name, tuning_text) values ('Open C',       'C  G  C  G  C  E ');   
                insert into tuning (tuning_name, tuning_text) values ('D Minor',      'D  A  D  F  A  D '); 
                insert into tuning (tuning_name, tuning_text) values ('G Minor',      'D  G  D  G  Bb D ');  
                insert into tuning (tuning_name, tuning_text) values ('D Modal',      'D  A  D  D  A  D ');   
                insert into tuning (tuning_name, tuning_text) values ('High Plain D', 'E  A  d  G  B  E ');   
                insert into tuning (tuning_name, tuning_text) values ('Baritone #1',  'B  E  A  D  F# B ');   
                insert into tuning (tuning_name, tuning_text) values ('Baritone #2',  'A  D  G  C  E  A ');                      
                insert into tuning (tuning_name, tuning_text) values ('Nashville',    'e  a  d  G  B  E ');   
                insert into tuning (tuning_name, tuning_text) values ('Hendrix',      'Eb Ab Db Gb Bb Eb');   
                insert into tuning (tuning_name, tuning_text) values ('Mayfield',     'F# A# C# F# A# F#');   
                insert into tuning (tuning_name, tuning_text) values ('Collins',      'F  C  F  Ab C  F ');   
                insert into tuning (tuning_name, tuning_text) values ('Half Bent',    'F  Bb Eb Ab C  F ');   
                insert into tuning (tuning_name, tuning_text) values ('Fourths',      'E  A  D  G  C  F ');   
                insert into tuning (tuning_name, tuning_text) values ('Lute',         'E  A  D  F# B  E ');   
                insert into tuning (tuning_name, tuning_text) values ('G 6',          'D  G  D  G  B  E ');   
                insert into tuning (tuning_name, tuning_text) values ('Richards',     'G  D  G  B  D    ');   
                insert into tuning (tuning_name, tuning_text) values ('Cooder',       'Db Ab Db F  Ab Db');   
                insert into tuning (tuning_name, tuning_text) values ('Kottke',       'C# F# B  E  G# C#');   
                insert into tuning (tuning_name, tuning_text) values ('C 6',          'C  G  C  G  A  E ');   
                insert into tuning (tuning_name, tuning_text) values ('Kaki King',    'C  G  D  G  A  D ');   
                insert into tuning (tuning_name, tuning_text) values ('Leadbelly',    'B  E  A  D  F# B ');   
                                
                create trigger delete_song after delete on song
                begin
                    delete from songcats where song_id = old.id;
                    delete from link where song_id = old.id;
                end;
              """
c = sqlite3.connect(':memory:')
c.executescript(sql)

