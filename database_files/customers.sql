CREATE TABLE public.customers
(
    customer_id integer NOT NULL,
    first_name text COLLATE pg_catalog."default" NOT NULL,
    last_name text COLLATE pg_catalog."default" NOT NULL,
    street text COLLATE pg_catalog."default" NOT NULL,
    housenumber text COLLATE pg_catalog."default" NOT NULL,
    po integer NOT NULL,
    city text COLLATE pg_catalog."default" NOT NULL,
    state text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customers
    OWNER to postgres;
insert into customers (customer_id,first_name,last_name,street,housenumber,po,city,state) values (1,'Thomas','Cox','Seventh Street','405',39755,'Springfield','MA');
