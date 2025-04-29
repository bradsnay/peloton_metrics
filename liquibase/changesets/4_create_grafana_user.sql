-- User is read only so it's okay that the password here is visible.
-- Normally this would be done with a secret manager but that's overkill for this use case.
CREATE USER grafana WITH PASSWORD 'grafanapw';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO grafana;
