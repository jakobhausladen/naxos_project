-- List of composers with number of albums
WITH AlbumCounts AS (
    SELECT p.id AS composer_id,
        p.name,
        COUNT(*) AS num_albums
    FROM Person AS p
        JOIN AlbumRole AS r ON p.id = r.person_id
    WHERE r.role = 'composer'
    GROUP BY p.id
    ORDER BY num_albums DESC
),

-- Find unique most commonly associated period if it exists
PeriodCounts AS (
    SELECT
        r.person_id AS composer_id,
        p.period,
        COUNT(*) AS period_count
    FROM AlbumRole AS r
    JOIN AlbumPeriod AS p ON p.catalogue_no = r.album_catalogue_no
    WHERE r.role = 'composer'
    GROUP BY r.person_id, p.period
),
MaxPeriodCounts AS (
    SELECT
        composer_id,
        MAX(period_count) AS max_period_count
    FROM PeriodCounts
    GROUP BY composer_id
),
BothPeriodCounts AS (
    SELECT
        pc.composer_id,
        pc.period,
        pc.period_count,
        mpc.max_period_count
    FROM PeriodCounts AS pc
    JOIN MaxPeriodCounts AS mpc ON pc.composer_id = mpc.composer_id
    WHERE pc.period_count = mpc.max_period_count
),
TopPeriods AS (
    SELECT
        composer_id,
        period AS top_period
    FROM BothPeriodCounts
    WHERE composer_id IN (
        SELECT composer_id
        FROM BothPeriodCounts
        GROUP BY composer_id
        HAVING COUNT(*) = 1
    )
),

-- Find unique most commonly associated genre if it exists
GenreCounts AS (
    SELECT
        r.person_id AS composer_id,
        g.genre,
        COUNT(*) AS genre_count
    FROM AlbumRole AS r
    JOIN AlbumGenre AS g ON g.catalogue_no = r.album_catalogue_no
    WHERE r.role = 'composer'
    GROUP BY r.person_id, g.genre
),
MaxGenreCounts AS (
    SELECT
        composer_id,
        MAX(genre_count) AS max_genre_count
    FROM GenreCounts
    GROUP BY composer_id
),
BothGenreCounts AS (
    SELECT
        gc.composer_id,
        gc.genre,
        gc.genre_count,
        mgc.max_genre_count
    FROM GenreCounts AS gc
    JOIN MaxGenreCounts AS mgc ON gc.composer_id = mgc.composer_id
    WHERE gc.genre_count = mgc.max_genre_count
),
TopGenres AS (
    SELECT
        composer_id,
        genre AS top_genre
    FROM BothGenreCounts
    WHERE composer_id IN (
        SELECT composer_id
        FROM BothGenreCounts
        GROUP BY composer_id
        HAVING COUNT(*) = 1
    )
)

-- Join the above queries
SELECT
    ac.composer_id AS Id,
    ac.name AS Label,
    ac.num_albums,
    tp.top_period,
    tg.top_genre
FROM AlbumCounts AS ac
LEFT JOIN TopPeriods AS tp
ON tp.composer_id = ac.composer_id
LEFT JOIN TopGenres AS tg
ON tg.composer_id = ac.composer_id
WHERE ac.name NOT IN ('Traditional', 'Not Applicable, na')