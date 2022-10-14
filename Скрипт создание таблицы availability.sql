-- Table: public.availability

-- DROP TABLE IF EXISTS public.availability;

CREATE TABLE IF NOT EXISTS public.availability
(
    availability_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    availability character varying(30) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT availability_pkey PRIMARY KEY (availability_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.availability
    OWNER to postgres;