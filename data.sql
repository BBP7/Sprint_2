--
-- PostgreSQL database dump
-

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: sports; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sports (
    message character varying(255),
    username character varying(30)
);


ALTER TABLE public.sports OWNER TO postgres;

--
-- Name: tvshows; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tvshows (
    message character varying(255),
    username character varying(30)
);


ALTER TABLE public.tvshows OWNER TO postgres;

--
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE movies (
    message character varying(255),
    username character varying(30)
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(30),
    password character varying(30),
    moviessection character varying(10),
    sportssection character varying(10),
    tvshowssection character varying(10)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: sports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sports (message, username) FROM stdin;
I love sports. peter
me too. ryan
I like only sports. tank
\.


--
-- Data for Name: tvshows; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tvshows (message, username) FROM stdin;
Im Here.  peter
So am I.  ryan
Yep. tank
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY movies (message, username) FROM stdin;
Hello.  peter
Whats Happing? ryan
Nothing much. tank
\.

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password, moviessection, sportssection, tvshowssection) FROM stdin;
01	peter	peter	True	True	True
02  ryan    ryan    True    True    False
03  tank    car     True    False   False
04  outcast no      False   False   False
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 41, true);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

