--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Actors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Actors" (
    id integer NOT NULL,
    name character varying NOT NULL,
    age integer,
    gender character varying
);


ALTER TABLE public."Actors" OWNER TO postgres;

--
-- Name: Actors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Actors_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Actors_id_seq" OWNER TO postgres;

--
-- Name: Actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Actors_id_seq" OWNED BY public."Actors".id;


--
-- Name: Movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Movies" (
    id integer NOT NULL,
    title character varying NOT NULL,
    release_date character varying
);


ALTER TABLE public."Movies" OWNER TO postgres;

--
-- Name: Movies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Movies_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Movies_id_seq" OWNER TO postgres;

--
-- Name: Movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Movies_id_seq" OWNED BY public."Movies".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: Actors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Actors" ALTER COLUMN id SET DEFAULT nextval('public."Actors_id_seq"'::regclass);


--
-- Name: Movies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Movies" ALTER COLUMN id SET DEFAULT nextval('public."Movies_id_seq"'::regclass);


--
-- Data for Name: Actors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Actors" (id, name, age, gender) FROM stdin;
1	aymen	24	male
2	tom hanks	65	male
3	leaonardo dicaprio	47	male
4	scarlett johansson	37	female
5	chris evans	40	male
6	angelina jolie	46	female
7	actor1	55	female
8	actor2	70	male
9	actor33	80	male
10	actor55	66	female
11	actor6	22	female
12	actor9	66	male
\.


--
-- Data for Name: Movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Movies" (id, title, release_date) FROM stdin;
1	the shawshank redemption	1994-9-22
2	the godfather	1972-3-24
3	the dark knight	2008-7-18
4	fight club	1999-11-11
5	inception	2010-7-8
6	movie1	1997-10-2
7	movie2	1998-03-10
8	movie3	1999-10-4
9	movie4	2000-10-5
10	movie5	1997-10-6
11	movie6	1997-10-7
12	movie7	1997-10-8
13	movie8	1997-10-9
14	movie9	1997-10-10
15	movie10	1997-10-11
16	movie11	1997-10-12
17	movie12	1997-10-13
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Name: Actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Actors_id_seq"', 12, true);


--
-- Name: Movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Movies_id_seq"', 17, true);


--
-- Name: Actors Actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Actors"
    ADD CONSTRAINT "Actors_pkey" PRIMARY KEY (id);


--
-- Name: Movies Movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Movies"
    ADD CONSTRAINT "Movies_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- PostgreSQL database dump complete
--

