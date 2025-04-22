CREATE TABLE public.workouts(
    workout_id text NOT NULL,
    user_id text NOT NULL,
    created_at timestamptz NOT NULL,
    start_time timestamptz NOT NULL,
    end_time timestamptz NOT NULL,
    timezone text NOT NULL,
    status text NOT NULL,
    device_type text NOT NULL,
    fitness_disipline text NOT NULL,
    has_pedaling_metrics boolean NOT NULL,
    has_leaderboard_metrics boolean NOT NULL,
    total_work real NOT NULL,
    is_total_work_personal_record boolean NOT NULL,
    is_outdoor boolean NOT NULL,
    metrics_type text NULL,
    name text NOT NULL,
    peloton_id text NOT NULL,
    platform text NOT NULL,
    workout_type text NOT NULL,
    total_watch_time_seconds integer NOT NULL, -- pull from v2_total_video_buffering_seconds
    difficulty_rating real NOT NULL,-- pull from 'ride' key
    difficulty_rating_count integer NOT NULL, -- pull from 'ride' key
    difficulty_level text NOT NULL, -- pull from 'ride' key
    duration integer NOT NULL, -- pull from 'ride' key
    image_url text NOT NULL, -- pull from 'ride' key
    title text NOT NULL, -- pull from 'ride' key
    instructor_id text NOT NULL, -- pull from 'instructor" key
    instructor_first_name text NOT NULL, -- pull from 'instructor" key
    instructor_last_name text NOT NULL, -- pull from 'instructor" key
    PRIMARY KEY(user_id, workout_id)
);

CREATE INDEX idx_start_time ON public.workouts(start_time);
CREATE INDEX idx_status ON public.workouts(status);
CREATE INDEX idx_fitness_disipline ON public.workouts(fitness_disipline);
