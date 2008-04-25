BEGIN;

DROP INDEX "tagged_item_tag_id" ;
DROP INDEX "tagged_item_content_type_id" ;

ALTER TABLE "tagged_item" RENAME TO "tagging_taggeditem" ;
ALTER TABLE "tag" RENAME TO "tagging_tag" ;

CREATE INDEX "tagging_taggeditem_tag_id" ON "tagging_taggeditem" ("tag_id");
CREATE INDEX "tagging_taggeditem_content_type_id" ON "tagging_taggeditem" ("content_type_id");
CREATE INDEX "tagging_taggeditem_object_id" ON "tagging_taggeditem" ("object_id");

COMMIT;
