-- Table: public.sofas

-- DROP TABLE IF EXISTS public.sofas;

CREATE TABLE IF NOT EXISTS public.sofas
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    artikul character varying(40) COLLATE pg_catalog."default" NOT NULL,
    price numeric(18,2) NOT NULL,
    price_without_discount numeric(18,2),
    availability integer NOT NULL DEFAULT 1,
    sofa_id integer,
    CONSTRAINT sofas_pkey PRIMARY KEY (id),
    CONSTRAINT availability FOREIGN KEY (availability)
        REFERENCES public.availability (availability_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.sofas
    OWNER to postgres;