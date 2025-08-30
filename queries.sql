-- 1. Har batch ke students
SELECT * FROM tbl_students WHERE course_batch = 'Batch-1';

-- 2. Top 5 students jinki age 20 se jyada hai
SELECT * FROM tbl_students WHERE age > 20 LIMIT 5;

-- 3. Delhi se students
SELECT * FROM tbl_students WHERE city = 'Delhi';

-- 4. Placed students
SELECT * FROM tbl_placements WHERE placement_status = 'Placed';

-- 5. Students jinhone Python seekha hai
SELECT * FROM tbl_programming WHERE language = 'Python';

-- 6. Students jinhone 50 se jyade problems solve kiye
SELECT * FROM tbl_programming WHERE problems_solved > 50;

-- 7. Students jinki communication skill 80 se jyada hai
SELECT * FROM tbl_softskills WHERE communication > 80;

-- 8. Students jinhone 2 se jyada internships kiye
SELECT * FROM tbl_placements WHERE internships_completed > 2;

-- 9. Students jo 2023 mein graduate honge
SELECT * FROM tbl_students WHERE graduation_year = 2023;

-- 10. Female students
SELECT * FROM tbl_students WHERE gender = 'Female';