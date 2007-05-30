import os
import os.path
import sqlite3

DBVERSION = 1
DBCHECK   = '-- GuitarPortFolio -- Created By Jorgen Bodde --'

DB_NOT_FOUND      = 0 
DB_OPEN_OK        = 1
DB_UPGRADE_NEEDED = 2
DB_ERROR          = 3
DB_UNKNOWN        = 4
DB_CREATE_ERROR   = 5
DB_TOO_NEW        = 6

db_problems         = [DB_NOT_FOUND, DB_ERROR, DB_UNKNOWN, DB_CREATE_ERROR]
db_version_mismatch = [DB_UPGRADE_NEEDED, DB_TOO_NEW]

error_string = {DB_NOT_FOUND: 'Database is not found at this location',
                DB_OPEN_OK: 'Database opened succesfully',
                DB_UPGRADE_NEEDED: 'Upgrade is needed for database',
                DB_ERROR: 'Operational (internal) database error',
                DB_CREATE_ERROR: 'Could not create database on location',
                DB_TOO_NEW: 'Database is newer in version then supported'}

create_sql = """
        BEGIN TRANSACTION;

        create table song (id INTEGER PRIMARY KEY,
                           name TEXT,                   /* name of song */
                           artist TEXT,                 /* artist */
                           barcount INTEGER,            /* number of bars in song */
                           difficulty INTEGER,          /* difficulty. EASY, NORMAL, INTERMEDIATE, etc */
                           songdate TEXT,               /* date of the song's orignal recording */
                           completed_perc INTEGER,      /* calculation 0 - 10 of how much is completed */
                           accuracy_perc INTEGER,       /* calculation 0 - 10 of how accurate the song is played */
                           status INTEGER,              /* status, STARTED, NOT STARTED, COMPLETED, POSTPONED etc */
                           lyrics TEXT,                 /* lyrics text */
                           information TEXT,            /* song information */
                           tuning_alt TEXT,             /* alternate tuning string, when tuning_id = -1 */
                           tuning_id INTEGER,           /* ID of table entry of tuning */  
                           date_unknown INTEGER,        /* 0 when false, 1 when true (date is unknown) */                       
                           year_only INTEGER,           /* 0 when false, 1 when true (only year display) */
                           capo_number INTEGER,         /* 0 = No capo, any other is the fret number */
                           media_id INTEGER,            /* ID of media, book, CD etc where song is found */
                           relpath TEXT,                /* relative path as mask / dir spec where link info is found */
                           time_added TEXT,             /* time when song is added */ 
                           time_started TEXT,           /* time song is started TODO -> STARTED */
                           time_completed TEXT,         /* time when song is set from STARTED -> COMPLETED */
                           time_postponed TEXT);        /* time when song is set from ?? -> POSTPONED */ 

        create table songcats (song_id INTEGER,         /* id of song where category is linked to */
                               category_id INTEGER);    /* id of the category associated with the song */
                                   
        create table category (id INTEGER PRIMARY KEY, 
                               name TEXT);               /* name of category */



        create table logentry (id INTEGER PRIMARY KEY,
                               song_id INTEGER,         /* id of song where log item belongs to */
                               log_date TEXT,           /* date of log entry */
                               log_text TEXT,           /* entered text (if any) */ 
                               log_type INTEGER,        /* type of log (added study time, change accuracy, percentage, etc) */
                               log_value INTEGER);      /* value that is changed */  
                                        
        create table tuning (id INTEGER PRIMARY KEY,
                             tuning_name TEXT,          /* name of tuning */
                             tuning_text TEXT);         /* tuning text */

        create table tabs (id INTEGER PRIMARY KEY,
                           name TEXT,                   /* name of the tab */
                           text TEXT,                   /* actual tab text */ 
                           link TEXT,                   /* FUTURE: link to actual tab */
                           author TEXT);                /* FUTURE: name of author */

        create table songtabs (song_id INTEGER,         /* id of song where tab is linked to */
                               tab_id INTEGER);         /* id of tab */

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
                 
        insert into tuning (tuning_name, tuning_text) values ('Standard',     'E  A  D  G  B  E '); /* keep first! */
        insert into tuning (tuning_name, tuning_text) values ('Drop D',       'D  A  D  G  B  E ');
        insert into tuning (tuning_name, tuning_text) values ('DADGAD', 	  'D  A  D  G  A  D ');
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

        create table version (db_version INTEGER,       /* version of the DB */
                              db_check TEXT);           /* extra check for the DB */
        
        COMMIT;        
        """

class Database(object):
    def __init__(self):
        self._conn = None
        self._dbFile = ''
        self.__opened = False
         
    #---------------------------------------------------------------------------
    def Open(self, path):
        self.Close()
        
        # check for existence of the DB
        if not os.path.isfile(path):
            return DB_NOT_FOUND
            
        # if we are found open and check version
        self._conn = sqlite3.connect(path)
                
        if self._conn <> None:
            try:
                r = self._conn.execute('select db_version, db_check from version').fetchone()
                if r[1] == DBCHECK:
                    if r[0] < DBVERSION:
                        self.Close()
                        return DB_UPGRADE_NEEDED
                    elif r[0] > DBVERSION:
                        self.Close()
                        return DB_TOO_NEW                        
                    else:
                        self.__opened = True
                        self._dbFile = path
                        return DB_OPEN_OK
                else:
                    return DB_UNKNOWN
            
            except sqlite3.OperationalError:    # error in script execution
                self.Close()
                return DB_UNKNOWN
            except sqlite3.DatabaseError:       # no such table etc
                self.Close()
                return DB_UNKNOWN                
        else:
            return DB_ERROR  
         
    #---------------------------------------------------------------------------
    def Create(self, path):
        """ The database needs to be created, only create when 100%
            certain the file does not exist """
        self.Close()
        
        # should not yet exist
        if os.path.isfile(path) or os.path.exists(path):
            return DB_ERROR
            
        # attempt an open first, if opens OK then we are not 
        # going to create it (in fear of destroying data)  
        status = self.Open(path)
        self.Close()

        if status in [DB_OPEN_OK, DB_UPGRADE_NEEDED, DB_TOO_NEW]:
            return DB_CREATE_ERROR    
        
        # check path and create if not present
        if path:
            head, tail = os.path.split(path)
            if not os.path.exists(head):
                try:
                    os.makedirs(head)
                except EnvironmentError:
                    return DB_ERROR
        else:
            return DB_ERROR
        
        # attempt a create of the DB
        self._conn = sqlite3.connect(path)
        conn = self._conn
        if conn:
            try:
                # create DB                
                conn.executescript(create_sql)
                conn.commit()            
                # insert version
                conn.execute('delete from version');
                conn.execute('insert into version (db_version, db_check) values (?,?)', (DBVERSION, DBCHECK))
                conn.commit()                                
            except sqlite3.OperationalError:
                self.Close()
                return DB_CREATE_ERROR
        
        # adapt path when opened succesfully
        return self.Open(path)        
           
    #---------------------------------------------------------------------------
    def IsOpened(self):
        return self.__opened
    
    #---------------------------------------------------------------------------
    def Close(self):
        """ Closes the database """
        self.__opened = False
        self._dbFile = ''
        if self._conn:
            self._conn.close()
            self._conn = None        
         
#===============================================================================
                
__db = None

def Get():
    global __db
    if not __db:
        __db = Database()
    return __db
    
def GetDb():
    assert __db._conn <> None
    return __db._conn
