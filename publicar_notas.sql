
CREATE OR REPLACE VIEW public.notas_publicas AS
SELECT disciplina, categoria, atividade, nota_obtida, nota_maxima
FROM public.notas_academicas
WHERE user_id = '522fa395-7afb-407a-a254-8cb922b711d3'::uuid;

REVOKE ALL ON public.notas_publicas FROM PUBLIC;
REVOKE ALL ON public.notas_publicas FROM authenticated;
GRANT USAGE ON SCHEMA public TO anon;
GRANT SELECT ON public.notas_publicas TO anon;
