WITH ComposerCounts AS (
    SELECT
        a.catalogue_no,
        COUNT(*) AS num_composers
    FROM Album AS a
    JOIN AlbumRole AS r ON r.album_catalogue_no = a.catalogue_no
    WHERE r.role = 'composer'
    GROUP BY a.catalogue_no
    HAVING num_composers > 1
),
PeriodCounts AS (
    SELECT
        a.catalogue_no,
        COUNT(*) AS num_periods
    FROM Album AS a
    JOIN AlbumPeriod AS p ON a.catalogue_no = p.catalogue_no
    GROUP BY a.catalogue_no
)

-- Create edges based on albums
SELECT
    r1.person_id AS Source,
    r2.person_id AS Target,
    COUNT(*) AS Weight
FROM AlbumRole AS r1
JOIN AlbumRole AS r2 ON r1.album_catalogue_no = r2.album_catalogue_no
JOIN ComposerCounts AS cc ON r1.album_catalogue_no = cc.catalogue_no
JOIN PeriodCounts AS pc ON r1.album_catalogue_no = pc.catalogue_no
WHERE r1.person_id != r2.person_id
    AND r1.role = 'composer'
    AND r2.role = 'composer'
    -- Filter albums by the number of featured composers and periods
    -- Play around with filter values to see how they influence the network structure 
    AND cc.num_composers <= 20
    AND pc.num_periods <= 3
GROUP BY r1.person_id, r2.person_id



