CREATE TABLE IF NOT EXISTS public.tracked_users (
    user_id BIGINT NOT NULL PRIMARY KEY,
    username text NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_username ON public.tracked_users(username);
