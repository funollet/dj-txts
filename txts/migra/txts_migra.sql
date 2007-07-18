BEGIN ;
-- Pre-upgrade script, transition from 'tags' application to 'django-tagging'.
-- Changes tables without reinstalling 'txts' application.
-- Works with 'tags-loader.py' and 'tags-extractor.py'. See the former one for usage instructions.
--
-- preserve original table
ALTER TABLE txts_txt RENAME TO txts_txt_old ;
-- create table with new structure
CREATE TABLE "txts_txt" (
    "id" integer NOT NULL PRIMARY KEY,
    "status" varchar(3) NOT NULL,
    "section_id" integer NOT NULL,
    "category_id" integer NULL,
    "name" varchar(200) NOT NULL,
    "abstract" text NOT NULL,
    "abstract_markup" text NOT NULL,
    "body" text NOT NULL,
    "body_markup" text NOT NULL,
    "tags" varchar(255) NOT NULL,
    "pub_date" datetime NOT NULL,
    "modif_date" datetime NOT NULL,
    "crea_date" datetime NOT NULL,
    "easyname" varchar(50) NOT NULL UNIQUE,
    "author_name" varchar(75) NOT NULL,
    "comments_closed" bool NOT NULL,
    "_order" integer NULL
);
-- move content to the new table losing all tags
INSERT INTO txts_txt SELECT id,status,section_id,category_id,name,abstract,abstract_markup,body,body_markup,'',pub_date,modif_date,crea_date,easyname,author_name,comments_closed,_order FROM txts_txt_old;
-- remove unused tables
ALTER TABLE txts_txt_tags RENAME TO txts_txt_tags_old;
ALTER TABLE tags_tag RENAME TO tags_tag_old;
--
-- (optional) show some results
--.tables txts
--.tables tags
--SELECT id,section_id,name FROM txts_txt WHERE id=4 ;
--
COMMIT ;
