SQL_G_BUILD = """
            CREATE TABLE tGame(
                game_id INTEGER NOT NULL PRIMARY KEY,
                season INTEGER NOT NULL,
                week INTEGER NOT NULL,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL
            );"""

SQL_P_BUILD = """
            CREATE TABLE tPass(
                    play_id INTEGER NOT NULL,
                    game_id INTEGER NOT NULL REFERENCES tGame(game_id),
                    offense TEXT NOT NULL,
                    defense TEXT NOT NULL,
                    game_clock TEXT NOT NULL,
                    clock_min INTEGER NOT NULL,
                    clock_sec INTEGER NOT NULL,
                    quarter INTEGER NOT NULL,
                    down INTEGER NOT NULL,
                    distance INTEGER NOT NULL,
                    game_sequence INTEGER NOT NULL,
                    fieldpos TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    pass_direction TEXT NOT NULL,
                    pass_depth INTEGER,
                    attempt INTEGER,
                    run INTEGER,
                    yards INTEGER,
                    yards_after_catch INTEGER,
                    completion INTEGER,
                    touchdown INTEGER,
                    interception INTEGER,
                    big_time_throw INTEGER,
                    turnover_worthy_play INTEGER,
                    pressure INTEGER,
                    sack INTEGER,
                    hit INTEGER,
                    hurry INTEGER,
                    hit_qb INTEGER,
                    hurry_qb INTEGER,
                    sack_qb INTEGER,
                    press_coverage INTEGER,
                    off_package TEXT,
                    def_package TEXT,
                    pass_box INTEGER,
                    blitz INTEGER,
                    shotgun TEXT,
                    pistol TEXT,
                    play_action INTEGER,
                    screen INTEGER,
                    first_down_conv TEXT,
                    stunt INTEGER,
                    yards_gained INTEGER,
                    play_type TEXT NOT NULL,
                    PRIMARY KEY (play_id)
                );"""

SQL_R_BUILD = """
            CREATE TABLE tRush(
                    play_id INTEGER NOT NULL,
                    game_id INTEGER NOT NULL REFERENCES tGame(game_id),
                    offense TEXT NOT NULL,
                    defense TEXT NOT NULL,
                    game_clock TEXT NOT NULL,
                    clock_min INTEGER NOT NULL,
                    clock_sec INTEGER NOT NULL,
                    quarter INTEGER NOT NULL,
                    down INTEGER NOT NULL,
                    distance INTEGER NOT NULL,
                    game_sequence INTEGER NOT NULL,
                    fieldpos TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    run_position TEXT,
                    run_direction TEXT,
                    yards INTEGER NOT NULL,
                    yards_after_contact INTEGER NOT NULL,
                    touchdown INTEGER,
                    fumbles INTEGER,
                    forced_fumbles INTEGER,
                    tackles_avoided INTEGER,
                    off_package TEXT,
                    def_package TEXT,
                    shotgun TEXT,
                    pistol TEXT,
                    play_action INTEGER,
                    screen INTEGER,
                    first_down_conv TEXT NOT NULL,
                    runner_position TEXT,
                    yards_gained INTEGER,
                    play_type TEXT NOT NULL,
                    PRIMARY KEY (play_id)
                );"""

SQL_RC_BUILD = """
            CREATE TABLE tRunConcept(
                    play_id INTEGER NOT NULL REFERENCES tRush(play_id),
                    run_concept_1 TEXT,
                    run_concept_2 TEXT,
                    run_concept_3 TEXT,
                    PRIMARY KEY (play_id)
                );"""

SQL_CHECK_GAME = """
            SELECT game_id
            FROM tGame
            WHERE season = :season
                AND week = :week
                AND home_team = :home_team
                AND away_team = :away_team
            ;"""

SQL_INSERT_TGAME = """
            INSERT INTO tGame (game_id,
                            season,
                            week,
                            home_team,
                            away_team)
            VALUES (:game_id,
                    :season,
                    :week,
                    :home_team,
                    :away_team)
            ;"""

SQL_CHECK_PASS = """
            SELECT play_id
            FROM tPass
            WHERE game_id = :game_id
                AND offense = :offense
                AND defense = :defense
                AND game_clock = :game_clock
                AND quarter = :quarter
                AND down = :down
                AND distance = :distance
                AND game_sequence = :game_sequence
                AND fieldpos = :fieldpos
                AND play_type = :play_type
            ;"""

SQL_INSERT_TPASS = """
            INSERT INTO tPass (play_id,
                            game_id,
                            offense,
                            defense,
                            game_clock,
                            clock_min,
                            clock_sec,
                            quarter,
                            down,
                            distance,
                            game_sequence,
                            fieldpos,
                            hash,
                            pass_direction,
                            pass_depth,
                            attempt,
                            run,
                            yards,
                            yards_after_catch,
                            completion,
                            touchdown,
                            interception,
                            big_time_throw,
                            turnover_worthy_play,
                            pressure,
                            sack,
                            hit,
                            hurry,
                            hit_qb,
                            hurry_qb,
                            sack_qb,
                            press_coverage,
                            off_package,
                            def_package,
                            pass_box,
                            blitz,
                            shotgun,
                            pistol,
                            play_action,
                            screen,
                            first_down_conv,
                            stunt,
                            yards_gained,
                            play_type)
            VALUES (:play_id,
                    :game_id,
                    :offense,
                    :defense,
                    :game_clock,
                    :clock_min,
                    :clock_sec,
                    :quarter,
                    :down,
                    :distance,
                    :game_sequence,
                    :fieldpos,
                    :hash,
                    :pass_direction,
                    :pass_depth,
                    :attempt,
                    :run,
                    :yards,
                    :yards_after_catch,
                    :completion,
                    :touchdown,
                    :interception,
                    :big_time_throw,
                    :turnover_worthy_play,
                    :pressure,
                    :sack,
                    :hit,
                    :hurry,
                    :hit_qb,
                    :hurry_qb,
                    :sack_qb,
                    :press_coverage,
                    :off_package,
                    :def_package,
                    :pass_box,
                    :blitz,
                    :shotgun,
                    :pistol,
                    :play_action,
                    :screen,
                    :first_down_conv,
                    :stunt,
                    :yards_gained,
                    :play_type)
            ;"""

SQL_CHECK_RUSH = """
            SELECT play_id
            FROM tRush
            WHERE game_id = :game_id
                AND offense = :offense
                AND defense = :defense
                AND game_clock = :game_clock
                AND quarter = :quarter
                AND down = :down
                AND distance = :distance
                AND game_sequence = :game_sequence
                AND fieldpos = :fieldpos
                AND play_type = :play_type
            ;"""

SQL_INSERT_TRUSH = """
            INSERT INTO tRush (play_id,
                            game_id,
                            offense,
                            defense,
                            game_clock,
                            clock_min,
                            clock_sec,
                            quarter,
                            down,
                            distance,
                            game_sequence,
                            fieldpos,
                            hash,
                            run_position,
                            run_direction,
                            yards,
                            yards_after_contact,
                            touchdown,
                            fumbles,
                            forced_fumbles,
                            tackles_avoided,
                            off_package,
                            def_package,
                            shotgun,
                            pistol,
                            play_action,
                            screen,
                            first_down_conv,
                            runner_position,
                            yards_gained,
                            play_type)
            VALUES (:play_id,
                    :game_id,
                    :offense,
                    :defense,
                    :game_clock,
                    :clock_min,
                    :clock_sec,
                    :quarter,
                    :down,
                    :distance,
                    :game_sequence,
                    :fieldpos,
                    :hash,
                    :run_position,
                    :run_direction,
                    :yards,
                    :yards_after_contact,
                    :touchdown,
                    :fumbles,
                    :forced_fumbles,
                    :tackles_avoided,
                    :off_package,
                    :def_package,
                    :shotgun,
                    :pistol,
                    :play_action,
                    :screen,
                    :first_down_conv,
                    :runner_position,
                    :yards_gained,
                    :play_type)
            ;"""

SQL_CHECK_RUNCONCEPT = """
            SELECT play_id
            FROM tRunConcept
            WHERE play_id = :play_id
            ;"""

SQL_INSERT_TRUNCONCEPT = """
            INSERT INTO tRunConcept (play_id,
                            run_concept_1,
                            run_concept_2,
                            run_concept_3)
            VALUES (:play_id,
                    :run_concept_1,
                    :run_concept_2,
                    :run_concept_3)
            ;"""