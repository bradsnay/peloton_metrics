CREATE TABLE public.tracked_users (
    user_id text NOT NULL PRIMARY KEY,
    date_initialized timestamptz NOT NULL DEFAULT NOW(),
    last_updated timestamptz NULL,
    username text NOT NULL,
    location text NULL,
    image_url text NULL,
    total_workouts integer NULL default 0,
    peloton_join_date TIMESTAMP NULL
);

CREATE INDEX idx_username ON public.tracked_users(username);
