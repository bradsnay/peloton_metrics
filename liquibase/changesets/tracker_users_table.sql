CREATE TABLE IF NOT EXISTS public.tracked_users (
    user_id text NOT NULL PRIMARY KEY,
    date_initialized timestamptz NOT NULL DEFAULT NOW(),
    last_updated timestamptz NULL,
    username text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    location text NULL,
    image_url text NULL,
    gender text NULL,
    weight real NULL,
    weight_unit text NULL,
    height real NULL,
    height_unit text NULL,
    total_workouts integer NULL default 0,
    peloton_join_date TIMESTAMP NULL,
    birthday date NULL
);

CREATE INDEX IF NOT EXISTS idx_username ON public.tracked_users(username);
CREATE INDEX IF NOT EXISTS idx_firstname_lastname ON public.tracked_users(first_name, last_name);