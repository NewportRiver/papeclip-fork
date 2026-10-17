DROP TABLE IF EXISTS knowledge_search;

CREATE VIRTUAL TABLE knowledge_search USING fts5(
    record_id UNINDEXED,
    title,
    body,
    domain
);

CREATE TRIGGER IF NOT EXISTS knowledge_search_after_insert
AFTER INSERT ON knowledge_records
WHEN NEW.status = 'Approved'
BEGIN
    INSERT INTO knowledge_search(record_id, title, body, domain)
    VALUES (NEW.id, NEW.title, NEW.body, NEW.domain);
END;

CREATE TRIGGER IF NOT EXISTS knowledge_search_after_update
AFTER UPDATE OF status, title, body, domain ON knowledge_records
BEGIN
    DELETE FROM knowledge_search WHERE record_id = NEW.id;
    INSERT INTO knowledge_search(record_id, title, body, domain)
    SELECT NEW.id, NEW.title, NEW.body, NEW.domain
    WHERE NEW.status = 'Approved';
END;

CREATE TRIGGER IF NOT EXISTS knowledge_search_after_delete
AFTER DELETE ON knowledge_records
BEGIN
    DELETE FROM knowledge_search WHERE record_id = OLD.id;
END;

INSERT INTO knowledge_search(record_id, title, body, domain)
SELECT id, title, body, domain FROM knowledge_records WHERE status = 'Approved';
