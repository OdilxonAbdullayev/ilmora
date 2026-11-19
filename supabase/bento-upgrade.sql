-- Run only on existing Academic Edition DB. Preserves existing IDs and progress.
ALTER TABLE public.progress DROP CONSTRAINT IF EXISTS progress_lesson_id_check;
ALTER TABLE public.progress ADD CONSTRAINT progress_lesson_id_check CHECK (lesson_id BETWEEN 1 AND 40);
ALTER TABLE public.lesson_comments DROP CONSTRAINT IF EXISTS lesson_comments_lesson_id_check;
ALTER TABLE public.lesson_comments ADD CONSTRAINT lesson_comments_lesson_id_check CHECK (lesson_id BETWEEN 1 AND 40);
