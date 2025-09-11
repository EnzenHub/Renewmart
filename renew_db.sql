--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-09-08 20:08:58

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 5233 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 894 (class 1247 OID 88372)
-- Name: approvalstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.approvalstatus AS ENUM (
    'PENDING',
    'APPROVED',
    'REJECTED',
    'CANCELLED'
);


ALTER TYPE public.approvalstatus OWNER TO postgres;

--
-- TOC entry 897 (class 1247 OID 88382)
-- Name: milestonestatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.milestonestatus AS ENUM (
    'PENDING',
    'IN_PROGRESS',
    'COMPLETED',
    'APPROVED',
    'REJECTED'
);


ALTER TYPE public.milestonestatus OWNER TO postgres;

--
-- TOC entry 915 (class 1247 OID 88468)
-- Name: notificationchannel; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notificationchannel AS ENUM (
    'EMAIL',
    'SMS',
    'WEB_PUSH',
    'IN_APP'
);


ALTER TYPE public.notificationchannel OWNER TO postgres;

--
-- TOC entry 918 (class 1247 OID 88478)
-- Name: notificationstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notificationstatus AS ENUM (
    'PENDING',
    'SENT',
    'DELIVERED',
    'FAILED',
    'READ'
);


ALTER TYPE public.notificationstatus OWNER TO postgres;

--
-- TOC entry 912 (class 1247 OID 88448)
-- Name: notificationtype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notificationtype AS ENUM (
    'TASK_ASSIGNED',
    'TASK_COMPLETED',
    'APPROVAL_REQUIRED',
    'APPROVAL_DECISION',
    'MILESTONE_REACHED',
    'DEADLINE_REMINDER',
    'SLA_BREACH',
    'DOCUMENT_UPLOADED',
    'STATUS_CHANGE'
);


ALTER TYPE public.notificationtype OWNER TO postgres;

--
-- TOC entry 900 (class 1247 OID 88394)
-- Name: opportunitystatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.opportunitystatus AS ENUM (
    'DRAFT',
    'SUBMITTED',
    'UNDER_REVIEW',
    'APPROVED',
    'REJECTED',
    'EXPIRED'
);


ALTER TYPE public.opportunitystatus OWNER TO postgres;

--
-- TOC entry 888 (class 1247 OID 88336)
-- Name: parcelstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.parcelstatus AS ENUM (
    'REGISTERED',
    'FEASIBILITY_ASSIGNED',
    'FEASIBILITY_IN_PROGRESS',
    'FEASIBILITY_COMPLETED',
    'FEASIBILITY_APPROVED',
    'FEASIBILITY_REJECTED',
    'READY_FOR_PROPOSAL',
    'IN_PROPOSAL',
    'IN_DEVELOPMENT',
    'READY_TO_BUILD'
);


ALTER TYPE public.parcelstatus OWNER TO postgres;

--
-- TOC entry 906 (class 1247 OID 88422)
-- Name: projectstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.projectstatus AS ENUM (
    'INITIATED',
    'IN_PROGRESS',
    'STAGE_GATE',
    'READY_TO_BUILD',
    'CANCELLED',
    'COMPLETED'
);


ALTER TYPE public.projectstatus OWNER TO postgres;

--
-- TOC entry 909 (class 1247 OID 88436)
-- Name: projecttype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.projecttype AS ENUM (
    'SOLAR',
    'WIND',
    'HYDRO',
    'STORAGE',
    'HYBRID'
);


ALTER TYPE public.projecttype OWNER TO postgres;

--
-- TOC entry 903 (class 1247 OID 88408)
-- Name: proposalstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.proposalstatus AS ENUM (
    'DRAFT',
    'SUBMITTED',
    'UNDER_REVIEW',
    'APPROVED',
    'REJECTED',
    'AGREEMENT_SIGNED'
);


ALTER TYPE public.proposalstatus OWNER TO postgres;

--
-- TOC entry 891 (class 1247 OID 88358)
-- Name: taskstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.taskstatus AS ENUM (
    'PENDING',
    'ASSIGNED',
    'IN_PROGRESS',
    'COMPLETED',
    'REJECTED',
    'CANCELLED'
);


ALTER TYPE public.taskstatus OWNER TO postgres;

--
-- TOC entry 885 (class 1247 OID 88320)
-- Name: usertype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.usertype AS ENUM (
    'LANDOWNER',
    'INVESTOR',
    'ADVISOR',
    'ANALYST',
    'PROJECT_MANAGER',
    'GOVERNANCE',
    'ADMIN'
);


ALTER TYPE public.usertype OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 234 (class 1259 OID 88628)
-- Name: approval_rules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.approval_rules (
    id integer NOT NULL,
    name character varying,
    description text,
    project_type public.projecttype,
    region character varying,
    size_band_min double precision,
    size_band_max double precision,
    required_approvers json,
    approval_type character varying,
    is_active boolean,
    config json,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.approval_rules OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 88627)
-- Name: approval_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.approval_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.approval_rules_id_seq OWNER TO postgres;

--
-- TOC entry 5234 (class 0 OID 0)
-- Dependencies: 233
-- Name: approval_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.approval_rules_id_seq OWNED BY public.approval_rules.id;


--
-- TOC entry 254 (class 1259 OID 88863)
-- Name: approvals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.approvals (
    id integer NOT NULL,
    approval_type character varying,
    status public.approvalstatus,
    comments text,
    approved_by integer,
    approved_at timestamp without time zone,
    land_parcel_id integer,
    proposal_id integer,
    project_id integer,
    milestone_id integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.approvals OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 88862)
-- Name: approvals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.approvals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.approvals_id_seq OWNER TO postgres;

--
-- TOC entry 5235 (class 0 OID 0)
-- Dependencies: 253
-- Name: approvals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.approvals_id_seq OWNED BY public.approvals.id;


--
-- TOC entry 246 (class 1259 OID 88753)
-- Name: development_projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.development_projects (
    id integer NOT NULL,
    name character varying,
    description text,
    status public.projectstatus,
    project_type public.projecttype,
    total_capacity_mw double precision,
    total_investment double precision,
    target_completion_date timestamp without time zone,
    actual_completion_date timestamp without time zone,
    proposal_id integer,
    project_manager_id integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.development_projects OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 88752)
-- Name: development_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.development_projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.development_projects_id_seq OWNER TO postgres;

--
-- TOC entry 5236 (class 0 OID 0)
-- Dependencies: 245
-- Name: development_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.development_projects_id_seq OWNED BY public.development_projects.id;


--
-- TOC entry 256 (class 1259 OID 88904)
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    name character varying,
    file_path character varying,
    file_size integer,
    mime_type character varying,
    document_type character varying,
    checksum character varying,
    land_parcel_id integer,
    task_id integer,
    project_id integer,
    proposal_id integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 88903)
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO postgres;

--
-- TOC entry 5237 (class 0 OID 0)
-- Dependencies: 255
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- TOC entry 230 (class 1259 OID 88587)
-- Name: investment_opportunities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.investment_opportunities (
    id integer NOT NULL,
    title character varying,
    description text,
    status public.opportunitystatus,
    target_capacity_mw double precision,
    target_region character varying,
    investment_amount double precision,
    expected_returns double precision,
    investor_id integer,
    advisor_id integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.investment_opportunities OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 88586)
-- Name: investment_opportunities_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.investment_opportunities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.investment_opportunities_id_seq OWNER TO postgres;

--
-- TOC entry 5238 (class 0 OID 0)
-- Dependencies: 229
-- Name: investment_opportunities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.investment_opportunities_id_seq OWNED BY public.investment_opportunities.id;


--
-- TOC entry 240 (class 1259 OID 88684)
-- Name: investment_proposals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.investment_proposals (
    id integer NOT NULL,
    title character varying,
    description text,
    status public.proposalstatus,
    total_capacity_mw double precision,
    total_investment double precision,
    expected_completion_date timestamp without time zone,
    opportunity_id integer,
    advisor_id integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.investment_proposals OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 88683)
-- Name: investment_proposals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.investment_proposals_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.investment_proposals_id_seq OWNER TO postgres;

--
-- TOC entry 5239 (class 0 OID 0)
-- Dependencies: 239
-- Name: investment_proposals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.investment_proposals_id_seq OWNED BY public.investment_proposals.id;


--
-- TOC entry 228 (class 1259 OID 88569)
-- Name: land_parcels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.land_parcels (
    id integer NOT NULL,
    name character varying,
    address character varying,
    size_acres double precision,
    coordinates json,
    description text,
    status public.parcelstatus,
    landowner_id integer,
    feasibility_completed boolean,
    feasibility_score double precision,
    feasibility_notes text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.land_parcels OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 88568)
-- Name: land_parcels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.land_parcels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.land_parcels_id_seq OWNER TO postgres;

--
-- TOC entry 5240 (class 0 OID 0)
-- Dependencies: 227
-- Name: land_parcels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.land_parcels_id_seq OWNED BY public.land_parcels.id;


--
-- TOC entry 250 (class 1259 OID 88804)
-- Name: milestones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.milestones (
    id integer NOT NULL,
    title character varying,
    description text,
    status public.milestonestatus,
    target_date timestamp without time zone,
    completed_at timestamp without time zone,
    project_id integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.milestones OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 88803)
-- Name: milestones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.milestones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.milestones_id_seq OWNER TO postgres;

--
-- TOC entry 5241 (class 0 OID 0)
-- Dependencies: 249
-- Name: milestones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.milestones_id_seq OWNED BY public.milestones.id;


--
-- TOC entry 238 (class 1259 OID 88667)
-- Name: notification_templates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_templates (
    id integer NOT NULL,
    name character varying,
    notification_type public.notificationtype,
    channel public.notificationchannel,
    subject_template character varying,
    message_template text,
    variables json,
    is_active boolean,
    priority integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer,
    updated_at timestamp with time zone
);


ALTER TABLE public.notification_templates OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 88666)
-- Name: notification_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notification_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notification_templates_id_seq OWNER TO postgres;

--
-- TOC entry 5242 (class 0 OID 0)
-- Dependencies: 237
-- Name: notification_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notification_templates_id_seq OWNED BY public.notification_templates.id;


--
-- TOC entry 236 (class 1259 OID 88645)
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    title character varying,
    message text,
    notification_type public.notificationtype,
    channel public.notificationchannel,
    status public.notificationstatus,
    user_id integer,
    related_entity_type character varying,
    related_entity_id integer,
    data json,
    sent_at timestamp without time zone,
    delivered_at timestamp without time zone,
    read_at timestamp without time zone,
    failed_reason text,
    retry_count integer,
    max_retries integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 88644)
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO postgres;

--
-- TOC entry 5243 (class 0 OID 0)
-- Dependencies: 235
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- TOC entry 222 (class 1259 OID 88515)
-- Name: permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissions (
    id integer NOT NULL,
    name character varying,
    description text,
    resource character varying,
    action character varying,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.permissions OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 88514)
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permissions_id_seq OWNER TO postgres;

--
-- TOC entry 5244 (class 0 OID 0)
-- Dependencies: 221
-- Name: permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;


--
-- TOC entry 244 (class 1259 OID 88730)
-- Name: proposal_parcels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.proposal_parcels (
    id integer NOT NULL,
    proposal_id integer,
    land_parcel_id integer,
    allocated_capacity_mw double precision,
    allocated_investment double precision,
    notes text,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.proposal_parcels OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 88729)
-- Name: proposal_parcels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.proposal_parcels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.proposal_parcels_id_seq OWNER TO postgres;

--
-- TOC entry 5245 (class 0 OID 0)
-- Dependencies: 243
-- Name: proposal_parcels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.proposal_parcels_id_seq OWNED BY public.proposal_parcels.id;


--
-- TOC entry 226 (class 1259 OID 88548)
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_permissions (
    id integer NOT NULL,
    role_id integer,
    permission_id integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.role_permissions OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 88547)
-- Name: role_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.role_permissions_id_seq OWNER TO postgres;

--
-- TOC entry 5246 (class 0 OID 0)
-- Dependencies: 225
-- Name: role_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_permissions_id_seq OWNED BY public.role_permissions.id;


--
-- TOC entry 220 (class 1259 OID 88503)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying,
    description text,
    user_type public.usertype,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 88502)
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO postgres;

--
-- TOC entry 5247 (class 0 OID 0)
-- Dependencies: 219
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- TOC entry 252 (class 1259 OID 88826)
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    title character varying,
    description text,
    status public.taskstatus,
    priority character varying,
    assigned_to integer,
    due_date timestamp without time zone,
    completed_at timestamp without time zone,
    land_parcel_id integer,
    project_id integer,
    milestone_id integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 88825)
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

--
-- TOC entry 5248 (class 0 OID 0)
-- Dependencies: 251
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- TOC entry 242 (class 1259 OID 88708)
-- Name: template_milestones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.template_milestones (
    id integer NOT NULL,
    title character varying,
    description text,
    "order" integer,
    estimated_days integer,
    template_project_id integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.template_milestones OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 88707)
-- Name: template_milestones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.template_milestones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.template_milestones_id_seq OWNER TO postgres;

--
-- TOC entry 5249 (class 0 OID 0)
-- Dependencies: 241
-- Name: template_milestones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.template_milestones_id_seq OWNED BY public.template_milestones.id;


--
-- TOC entry 232 (class 1259 OID 88611)
-- Name: template_projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.template_projects (
    id integer NOT NULL,
    name character varying,
    description text,
    project_type public.projecttype,
    region character varying,
    size_band_min double precision,
    size_band_max double precision,
    config json,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.template_projects OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 88610)
-- Name: template_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.template_projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.template_projects_id_seq OWNER TO postgres;

--
-- TOC entry 5250 (class 0 OID 0)
-- Dependencies: 231
-- Name: template_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.template_projects_id_seq OWNED BY public.template_projects.id;


--
-- TOC entry 248 (class 1259 OID 88777)
-- Name: template_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.template_tasks (
    id integer NOT NULL,
    title character varying,
    description text,
    task_type character varying,
    priority character varying,
    estimated_hours double precision,
    template_project_id integer,
    template_milestone_id integer,
    created_at timestamp with time zone DEFAULT now(),
    created_by integer
);


ALTER TABLE public.template_tasks OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 88776)
-- Name: template_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.template_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.template_tasks_id_seq OWNER TO postgres;

--
-- TOC entry 5251 (class 0 OID 0)
-- Dependencies: 247
-- Name: template_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.template_tasks_id_seq OWNED BY public.template_tasks.id;


--
-- TOC entry 224 (class 1259 OID 88527)
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 88526)
-- Name: user_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_roles_id_seq OWNER TO postgres;

--
-- TOC entry 5252 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;


--
-- TOC entry 218 (class 1259 OID 88490)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying,
    email character varying,
    hashed_password character varying,
    user_type public.usertype,
    is_active boolean,
    phone character varying,
    company character varying,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 88489)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 5253 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4889 (class 2604 OID 88631)
-- Name: approval_rules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approval_rules ALTER COLUMN id SET DEFAULT nextval('public.approval_rules_id_seq'::regclass);


--
-- TOC entry 4909 (class 2604 OID 88866)
-- Name: approvals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals ALTER COLUMN id SET DEFAULT nextval('public.approvals_id_seq'::regclass);


--
-- TOC entry 4901 (class 2604 OID 88756)
-- Name: development_projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.development_projects ALTER COLUMN id SET DEFAULT nextval('public.development_projects_id_seq'::regclass);


--
-- TOC entry 4911 (class 2604 OID 88907)
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- TOC entry 4885 (class 2604 OID 88590)
-- Name: investment_opportunities id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_opportunities ALTER COLUMN id SET DEFAULT nextval('public.investment_opportunities_id_seq'::regclass);


--
-- TOC entry 4895 (class 2604 OID 88687)
-- Name: investment_proposals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_proposals ALTER COLUMN id SET DEFAULT nextval('public.investment_proposals_id_seq'::regclass);


--
-- TOC entry 4883 (class 2604 OID 88572)
-- Name: land_parcels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.land_parcels ALTER COLUMN id SET DEFAULT nextval('public.land_parcels_id_seq'::regclass);


--
-- TOC entry 4905 (class 2604 OID 88807)
-- Name: milestones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milestones ALTER COLUMN id SET DEFAULT nextval('public.milestones_id_seq'::regclass);


--
-- TOC entry 4893 (class 2604 OID 88670)
-- Name: notification_templates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_templates ALTER COLUMN id SET DEFAULT nextval('public.notification_templates_id_seq'::regclass);


--
-- TOC entry 4891 (class 2604 OID 88648)
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- TOC entry 4877 (class 2604 OID 88518)
-- Name: permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);


--
-- TOC entry 4899 (class 2604 OID 88733)
-- Name: proposal_parcels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_parcels ALTER COLUMN id SET DEFAULT nextval('public.proposal_parcels_id_seq'::regclass);


--
-- TOC entry 4881 (class 2604 OID 88551)
-- Name: role_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions ALTER COLUMN id SET DEFAULT nextval('public.role_permissions_id_seq'::regclass);


--
-- TOC entry 4875 (class 2604 OID 88506)
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- TOC entry 4907 (class 2604 OID 88829)
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- TOC entry 4897 (class 2604 OID 88711)
-- Name: template_milestones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_milestones ALTER COLUMN id SET DEFAULT nextval('public.template_milestones_id_seq'::regclass);


--
-- TOC entry 4887 (class 2604 OID 88614)
-- Name: template_projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_projects ALTER COLUMN id SET DEFAULT nextval('public.template_projects_id_seq'::regclass);


--
-- TOC entry 4903 (class 2604 OID 88780)
-- Name: template_tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_tasks ALTER COLUMN id SET DEFAULT nextval('public.template_tasks_id_seq'::regclass);


--
-- TOC entry 4879 (class 2604 OID 88530)
-- Name: user_roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);


--
-- TOC entry 4873 (class 2604 OID 88493)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 5205 (class 0 OID 88628)
-- Dependencies: 234
-- Data for Name: approval_rules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.approval_rules (id, name, description, project_type, region, size_band_min, size_band_max, required_approvers, approval_type, is_active, config, created_at, created_by) FROM stdin;
\.


--
-- TOC entry 5225 (class 0 OID 88863)
-- Dependencies: 254
-- Data for Name: approvals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.approvals (id, approval_type, status, comments, approved_by, approved_at, land_parcel_id, proposal_id, project_id, milestone_id, created_at, created_by) FROM stdin;
1	feasibility	APPROVED	Feasibility study meets all requirements	11	2025-09-04 11:21:52.182558	1	\N	\N	\N	2025-09-07 11:21:52.089736+05:30	5
2	proposal	APPROVED	Proposal approved for development	12	2025-09-06 11:21:52.182558	\N	1	\N	\N	2025-09-07 11:21:52.089736+05:30	5
3	milestone	PENDING	Awaiting environmental clearance	\N	\N	2	\N	\N	\N	2025-09-07 11:21:52.089736+05:30	6
\.


--
-- TOC entry 5217 (class 0 OID 88753)
-- Dependencies: 246
-- Data for Name: development_projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.development_projects (id, name, description, status, project_type, total_capacity_mw, total_investment, target_completion_date, actual_completion_date, proposal_id, project_manager_id, created_at, updated_at) FROM stdin;
1	California Solar Development Project	Large-scale solar development in California	IN_PROGRESS	SOLAR	500	750000000	2026-09-07 11:21:52.161773	\N	1	9	2025-09-07 11:21:52.089736+05:30	\N
2	Texas Wind Energy Project	Wind energy development in Texas	INITIATED	WIND	800	1200000000	2026-12-01 11:21:52.161773	\N	2	10	2025-09-07 11:21:52.089736+05:30	\N
\.


--
-- TOC entry 5227 (class 0 OID 88904)
-- Dependencies: 256
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents (id, name, file_path, file_size, mime_type, document_type, checksum, land_parcel_id, task_id, project_id, proposal_id, created_at, created_by) FROM stdin;
1	Feasibility Study Report - Site A	/documents/feasibility_site_a.pdf	2048000	application/pdf	feasibility_report	abc123def456	1	\N	\N	\N	2025-09-07 11:21:52.089736+05:30	7
2	Environmental Impact Assessment	/documents/eia_wind_site.pdf	1536000	application/pdf	environmental_assessment	def456ghi789	2	\N	\N	\N	2025-09-07 11:21:52.089736+05:30	8
3	Development Service Agreement	/documents/dsa_proposal_1.pdf	1024000	application/pdf	agreement	ghi789jkl012	\N	\N	\N	1	2025-09-07 11:21:52.089736+05:30	5
\.


--
-- TOC entry 5201 (class 0 OID 88587)
-- Dependencies: 230
-- Data for Name: investment_opportunities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.investment_opportunities (id, title, description, status, target_capacity_mw, target_region, investment_amount, expected_returns, investor_id, advisor_id, created_at, updated_at) FROM stdin;
1	Solar Development Opportunity - West Coast	Large-scale solar development opportunity in California	APPROVED	500	California	750000000	12.5	3	5	2025-09-07 11:21:52.089736+05:30	\N
2	Wind Energy Portfolio - Texas	Multi-site wind energy development in Texas	UNDER_REVIEW	800	Texas	1200000000	15	4	6	2025-09-07 11:21:52.089736+05:30	\N
\.


--
-- TOC entry 5211 (class 0 OID 88684)
-- Dependencies: 240
-- Data for Name: investment_proposals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.investment_proposals (id, title, description, status, total_capacity_mw, total_investment, expected_completion_date, opportunity_id, advisor_id, created_at, updated_at) FROM stdin;
1	California Solar Portfolio Proposal	Comprehensive solar development proposal for California sites	APPROVED	500	750000000	2026-09-07 11:21:52.147507	1	5	2025-09-07 11:21:52.089736+05:30	\N
2	Texas Wind Energy Proposal	Wind energy development proposal for Texas region	UNDER_REVIEW	800	1200000000	2026-12-01 11:21:52.147507	2	6	2025-09-07 11:21:52.089736+05:30	\N
\.


--
-- TOC entry 5199 (class 0 OID 88569)
-- Dependencies: 228
-- Data for Name: land_parcels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.land_parcels (id, name, address, size_acres, coordinates, description, status, landowner_id, feasibility_completed, feasibility_score, feasibility_notes, created_at, updated_at) FROM stdin;
1	Solar Farm Site A	123 Solar Lane, Desert Valley, CA	150	{"lat": 34.0522, "lng": -118.2437}	Prime solar development site with excellent sun exposure	REGISTERED	1	f	\N	\N	2025-09-07 11:21:52.089736+05:30	\N
2	Wind Energy Site B	456 Windy Ridge, Mountain View, TX	200	{"lat": 32.7767, "lng": -96.797}	High elevation site ideal for wind turbines	FEASIBILITY_COMPLETED	2	t	8.5	Excellent wind conditions, minimal environmental impact	2025-09-07 11:21:52.089736+05:30	\N
3	Hybrid Energy Complex	789 Renewable Blvd, Green City, OR	300	{"lat": 45.5152, "lng": -122.6784}	Large site suitable for solar + storage hybrid project	READY_FOR_PROPOSAL	1	t	9.2	Perfect for hybrid renewable energy development	2025-09-07 11:21:52.089736+05:30	\N
\.


--
-- TOC entry 5221 (class 0 OID 88804)
-- Dependencies: 250
-- Data for Name: milestones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.milestones (id, title, description, status, target_date, completed_at, project_id, created_at, created_by) FROM stdin;
1	Feasibility Complete	All feasibility studies completed and approved	COMPLETED	2025-08-28 11:21:52.178514	2025-09-02 11:21:52.178514	1	2025-09-07 11:21:52.089736+05:30	9
2	Permits Approved	All required permits obtained	IN_PROGRESS	2025-11-06 11:21:52.178514	\N	1	2025-09-07 11:21:52.089736+05:30	9
3	Environmental Clearance	Environmental impact assessment completed	PENDING	2025-12-06 11:21:52.178514	\N	2	2025-09-07 11:21:52.089736+05:30	10
\.


--
-- TOC entry 5209 (class 0 OID 88667)
-- Dependencies: 238
-- Data for Name: notification_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_templates (id, name, notification_type, channel, subject_template, message_template, variables, is_active, priority, created_at, created_by, updated_at) FROM stdin;
1	Task Assignment Email	TASK_ASSIGNED	EMAIL	New Task Assigned: {task_title}	You have been assigned a new task: {task_title}. Due date: {due_date}	["task_title", "due_date"]	t	1	2025-09-07 11:21:52.089736+05:30	13	\N
2	Approval Required	APPROVAL_REQUIRED	IN_APP	Approval Required: {approval_type}	Approval required for {approval_type}: {entity_name}	["approval_type", "entity_name"]	t	1	2025-09-07 11:21:52.089736+05:30	13	\N
\.


--
-- TOC entry 5207 (class 0 OID 88645)
-- Dependencies: 236
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, title, message, notification_type, channel, status, user_id, related_entity_type, related_entity_id, data, sent_at, delivered_at, read_at, failed_reason, retry_count, max_retries, created_at, created_by) FROM stdin;
\.


--
-- TOC entry 5193 (class 0 OID 88515)
-- Dependencies: 222
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissions (id, name, description, resource, action, created_at) FROM stdin;
\.


--
-- TOC entry 5215 (class 0 OID 88730)
-- Dependencies: 244
-- Data for Name: proposal_parcels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.proposal_parcels (id, proposal_id, land_parcel_id, allocated_capacity_mw, allocated_investment, notes, created_at) FROM stdin;
1	1	1	150	225000000	Primary solar site with excellent conditions	2025-09-07 11:21:52.089736+05:30
2	1	3	350	525000000	Hybrid solar + storage site	2025-09-07 11:21:52.089736+05:30
3	2	2	200	300000000	Wind energy development site	2025-09-07 11:21:52.089736+05:30
\.


--
-- TOC entry 5197 (class 0 OID 88548)
-- Dependencies: 226
-- Data for Name: role_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role_permissions (id, role_id, permission_id, created_at) FROM stdin;
\.


--
-- TOC entry 5191 (class 0 OID 88503)
-- Dependencies: 220
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name, description, user_type, created_at) FROM stdin;
\.


--
-- TOC entry 5223 (class 0 OID 88826)
-- Dependencies: 252
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, title, description, status, priority, assigned_to, due_date, completed_at, land_parcel_id, project_id, milestone_id, created_at, created_by) FROM stdin;
1	Site Feasibility Study	Conduct comprehensive feasibility study for solar site	COMPLETED	high	7	2025-10-07 11:21:52.167164	2025-09-02 11:21:52.167164	1	1	\N	2025-09-07 11:21:52.089736+05:30	5
2	Environmental Impact Assessment	Complete environmental impact assessment for wind site	IN_PROGRESS	high	8	2025-10-22 11:21:52.167164	\N	2	2	\N	2025-09-07 11:21:52.089736+05:30	6
3	Permit Application Submission	Submit all required permits for hybrid energy project	PENDING	urgent	7	2025-09-22 11:21:52.167164	\N	3	1	\N	2025-09-07 11:21:52.089736+05:30	9
\.


--
-- TOC entry 5213 (class 0 OID 88708)
-- Dependencies: 242
-- Data for Name: template_milestones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.template_milestones (id, title, description, "order", estimated_days, template_project_id, created_at, created_by) FROM stdin;
\.


--
-- TOC entry 5203 (class 0 OID 88611)
-- Dependencies: 232
-- Data for Name: template_projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.template_projects (id, name, description, project_type, region, size_band_min, size_band_max, config, created_at, created_by) FROM stdin;
1	Solar Farm Template - California	Standard template for solar farm development in California	SOLAR	California	100	500	{"required_milestones": ["feasibility", "permits", "construction"], "estimated_duration_days": 365, "required_approvals": ["environmental", "zoning", "utility"]}	2025-09-07 11:21:52.089736+05:30	13
2	Wind Farm Template - Texas	Standard template for wind farm development in Texas	WIND	Texas	200	1000	{"required_milestones": ["feasibility", "permits", "construction"], "estimated_duration_days": 450, "required_approvals": ["environmental", "aviation", "utility"]}	2025-09-07 11:21:52.089736+05:30	13
\.


--
-- TOC entry 5219 (class 0 OID 88777)
-- Dependencies: 248
-- Data for Name: template_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.template_tasks (id, title, description, task_type, priority, estimated_hours, template_project_id, template_milestone_id, created_at, created_by) FROM stdin;
\.


--
-- TOC entry 5195 (class 0 OID 88527)
-- Dependencies: 224
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (id, user_id, role_id, created_at) FROM stdin;
\.


--
-- TOC entry 5189 (class 0 OID 88490)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, hashed_password, user_type, is_active, phone, company, created_at, updated_at) FROM stdin;
1	Alice Landowner	alice@landowner.com	\N	LANDOWNER	t	555-0001	Land Holdings LLC	2025-09-07 11:21:52.089736+05:30	\N
2	Bob Property Owner	bob@property.com	\N	LANDOWNER	t	555-0002	Property Group Inc	2025-09-07 11:21:52.089736+05:30	\N
3	Charlie Investor	charlie@investor.com	\N	INVESTOR	t	555-0003	Green Energy Capital	2025-09-07 11:21:52.089736+05:30	\N
4	Diana Capital	diana@capital.com	\N	INVESTOR	t	555-0004	Renewable Ventures	2025-09-07 11:21:52.089736+05:30	\N
5	Eve Advisor	eve@advisor.com	\N	ADVISOR	t	555-0005	RenewMart Advisors	2025-09-07 11:21:52.089736+05:30	\N
6	Frank Consultant	frank@consultant.com	\N	ADVISOR	t	555-0006	Energy Solutions	2025-09-07 11:21:52.089736+05:30	\N
7	Grace Analyst	grace@analyst.com	\N	ANALYST	t	555-0007	Technical Services	2025-09-07 11:21:52.089736+05:30	\N
8	Henry Engineer	henry@engineer.com	\N	ANALYST	t	555-0008	Engineering Corp	2025-09-07 11:21:52.089736+05:30	\N
9	Ivy Manager	ivy@manager.com	\N	PROJECT_MANAGER	t	555-0009	Project Management Inc	2025-09-07 11:21:52.089736+05:30	\N
10	Jack Coordinator	jack@coordinator.com	\N	PROJECT_MANAGER	t	555-0010	Development Co	2025-09-07 11:21:52.089736+05:30	\N
11	Karen Governance	karen@governance.com	\N	GOVERNANCE	t	555-0011	Compliance Office	2025-09-07 11:21:52.089736+05:30	\N
12	Liam Approver	liam@approver.com	\N	GOVERNANCE	t	555-0012	Approval Board	2025-09-07 11:21:52.089736+05:30	\N
13	Maya Admin	maya@admin.com	\N	ADMIN	t	555-0013	RenewMart	2025-09-07 11:21:52.089736+05:30	\N
14	Sai Aryan	sai.namp@test.com	$2b$12$TabdZ5XAWLX2IYgWSqvOfOkMaFBTtXemXeVoMrGquwyz0/iQa6pEa	LANDOWNER	t	234567890	uibiub	2025-09-07 18:12:47.963362+05:30	\N
15	Admin User	admin@renewmart.com	$2b$12$.BNF/VEF7s1GNHKvSWcGf.ZQ5D48xWBrAGrXPayLYNPUfp.8ikJY.	ADMIN	t	+1234567890	RenewMart Inc	2025-09-07 20:46:00.83714+05:30	\N
16	Test User	test@example.com	$2b$12$fDthVIJeHsjloOBeoqC37eu8zzhDjavW1Y3m9UTatqV3HtcL4igWO	ANALYST	t	1234567890	Test Company	2025-09-08 16:41:07.06203+05:30	\N
\.


--
-- TOC entry 5254 (class 0 OID 0)
-- Dependencies: 233
-- Name: approval_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.approval_rules_id_seq', 1, false);


--
-- TOC entry 5255 (class 0 OID 0)
-- Dependencies: 253
-- Name: approvals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.approvals_id_seq', 3, true);


--
-- TOC entry 5256 (class 0 OID 0)
-- Dependencies: 245
-- Name: development_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.development_projects_id_seq', 2, true);


--
-- TOC entry 5257 (class 0 OID 0)
-- Dependencies: 255
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_id_seq', 3, true);


--
-- TOC entry 5258 (class 0 OID 0)
-- Dependencies: 229
-- Name: investment_opportunities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.investment_opportunities_id_seq', 2, true);


--
-- TOC entry 5259 (class 0 OID 0)
-- Dependencies: 239
-- Name: investment_proposals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.investment_proposals_id_seq', 2, true);


--
-- TOC entry 5260 (class 0 OID 0)
-- Dependencies: 227
-- Name: land_parcels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.land_parcels_id_seq', 3, true);


--
-- TOC entry 5261 (class 0 OID 0)
-- Dependencies: 249
-- Name: milestones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.milestones_id_seq', 3, true);


--
-- TOC entry 5262 (class 0 OID 0)
-- Dependencies: 237
-- Name: notification_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notification_templates_id_seq', 2, true);


--
-- TOC entry 5263 (class 0 OID 0)
-- Dependencies: 235
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- TOC entry 5264 (class 0 OID 0)
-- Dependencies: 221
-- Name: permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permissions_id_seq', 1, false);


--
-- TOC entry 5265 (class 0 OID 0)
-- Dependencies: 243
-- Name: proposal_parcels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.proposal_parcels_id_seq', 3, true);


--
-- TOC entry 5266 (class 0 OID 0)
-- Dependencies: 225
-- Name: role_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_permissions_id_seq', 1, false);


--
-- TOC entry 5267 (class 0 OID 0)
-- Dependencies: 219
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, false);


--
-- TOC entry 5268 (class 0 OID 0)
-- Dependencies: 251
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 3, true);


--
-- TOC entry 5269 (class 0 OID 0)
-- Dependencies: 241
-- Name: template_milestones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.template_milestones_id_seq', 1, false);


--
-- TOC entry 5270 (class 0 OID 0)
-- Dependencies: 231
-- Name: template_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.template_projects_id_seq', 2, true);


--
-- TOC entry 5271 (class 0 OID 0)
-- Dependencies: 247
-- Name: template_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.template_tasks_id_seq', 1, false);


--
-- TOC entry 5272 (class 0 OID 0)
-- Dependencies: 223
-- Name: user_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_roles_id_seq', 1, false);


--
-- TOC entry 5273 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 16, true);


--
-- TOC entry 4952 (class 2606 OID 88636)
-- Name: approval_rules approval_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approval_rules
    ADD CONSTRAINT approval_rules_pkey PRIMARY KEY (id);


--
-- TOC entry 4997 (class 2606 OID 88871)
-- Name: approvals approvals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals
    ADD CONSTRAINT approvals_pkey PRIMARY KEY (id);


--
-- TOC entry 4979 (class 2606 OID 88761)
-- Name: development_projects development_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.development_projects
    ADD CONSTRAINT development_projects_pkey PRIMARY KEY (id);


--
-- TOC entry 5000 (class 2606 OID 88912)
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- TOC entry 4942 (class 2606 OID 88595)
-- Name: investment_opportunities investment_opportunities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_opportunities
    ADD CONSTRAINT investment_opportunities_pkey PRIMARY KEY (id);


--
-- TOC entry 4964 (class 2606 OID 88692)
-- Name: investment_proposals investment_proposals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_proposals
    ADD CONSTRAINT investment_proposals_pkey PRIMARY KEY (id);


--
-- TOC entry 4940 (class 2606 OID 88577)
-- Name: land_parcels land_parcels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.land_parcels
    ADD CONSTRAINT land_parcels_pkey PRIMARY KEY (id);


--
-- TOC entry 4991 (class 2606 OID 88812)
-- Name: milestones milestones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milestones
    ADD CONSTRAINT milestones_pkey PRIMARY KEY (id);


--
-- TOC entry 4962 (class 2606 OID 88675)
-- Name: notification_templates notification_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_templates
    ADD CONSTRAINT notification_templates_pkey PRIMARY KEY (id);


--
-- TOC entry 4958 (class 2606 OID 88653)
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- TOC entry 4925 (class 2606 OID 88523)
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 4977 (class 2606 OID 88738)
-- Name: proposal_parcels proposal_parcels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_parcels
    ADD CONSTRAINT proposal_parcels_pkey PRIMARY KEY (id);


--
-- TOC entry 4935 (class 2606 OID 88554)
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 4921 (class 2606 OID 88511)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 4995 (class 2606 OID 88834)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 4972 (class 2606 OID 88716)
-- Name: template_milestones template_milestones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_milestones
    ADD CONSTRAINT template_milestones_pkey PRIMARY KEY (id);


--
-- TOC entry 4950 (class 2606 OID 88619)
-- Name: template_projects template_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_projects
    ADD CONSTRAINT template_projects_pkey PRIMARY KEY (id);


--
-- TOC entry 4987 (class 2606 OID 88785)
-- Name: template_tasks template_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_tasks
    ADD CONSTRAINT template_tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 4930 (class 2606 OID 88533)
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 4917 (class 2606 OID 88498)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4953 (class 1259 OID 88643)
-- Name: ix_approval_rules_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_approval_rules_id ON public.approval_rules USING btree (id);


--
-- TOC entry 4954 (class 1259 OID 88642)
-- Name: ix_approval_rules_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_approval_rules_name ON public.approval_rules USING btree (name);


--
-- TOC entry 4998 (class 1259 OID 88902)
-- Name: ix_approvals_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_approvals_id ON public.approvals USING btree (id);


--
-- TOC entry 4980 (class 1259 OID 88773)
-- Name: ix_development_projects_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_development_projects_id ON public.development_projects USING btree (id);


--
-- TOC entry 4981 (class 1259 OID 88772)
-- Name: ix_development_projects_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_development_projects_name ON public.development_projects USING btree (name);


--
-- TOC entry 4982 (class 1259 OID 88774)
-- Name: ix_development_projects_project_manager_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_development_projects_project_manager_id ON public.development_projects USING btree (project_manager_id);


--
-- TOC entry 4983 (class 1259 OID 88775)
-- Name: ix_development_projects_proposal_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_development_projects_proposal_id ON public.development_projects USING btree (proposal_id);


--
-- TOC entry 5001 (class 1259 OID 88938)
-- Name: ix_documents_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_documents_id ON public.documents USING btree (id);


--
-- TOC entry 4943 (class 1259 OID 88607)
-- Name: ix_investment_opportunities_advisor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_opportunities_advisor_id ON public.investment_opportunities USING btree (advisor_id);


--
-- TOC entry 4944 (class 1259 OID 88608)
-- Name: ix_investment_opportunities_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_opportunities_id ON public.investment_opportunities USING btree (id);


--
-- TOC entry 4945 (class 1259 OID 88609)
-- Name: ix_investment_opportunities_investor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_opportunities_investor_id ON public.investment_opportunities USING btree (investor_id);


--
-- TOC entry 4946 (class 1259 OID 88606)
-- Name: ix_investment_opportunities_title; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_opportunities_title ON public.investment_opportunities USING btree (title);


--
-- TOC entry 4965 (class 1259 OID 88703)
-- Name: ix_investment_proposals_advisor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_proposals_advisor_id ON public.investment_proposals USING btree (advisor_id);


--
-- TOC entry 4966 (class 1259 OID 88706)
-- Name: ix_investment_proposals_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_proposals_id ON public.investment_proposals USING btree (id);


--
-- TOC entry 4967 (class 1259 OID 88705)
-- Name: ix_investment_proposals_opportunity_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_proposals_opportunity_id ON public.investment_proposals USING btree (opportunity_id);


--
-- TOC entry 4968 (class 1259 OID 88704)
-- Name: ix_investment_proposals_title; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_investment_proposals_title ON public.investment_proposals USING btree (title);


--
-- TOC entry 4936 (class 1259 OID 88583)
-- Name: ix_land_parcels_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_land_parcels_id ON public.land_parcels USING btree (id);


--
-- TOC entry 4937 (class 1259 OID 88585)
-- Name: ix_land_parcels_landowner_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_land_parcels_landowner_id ON public.land_parcels USING btree (landowner_id);


--
-- TOC entry 4938 (class 1259 OID 88584)
-- Name: ix_land_parcels_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_land_parcels_name ON public.land_parcels USING btree (name);


--
-- TOC entry 4988 (class 1259 OID 88824)
-- Name: ix_milestones_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_milestones_id ON public.milestones USING btree (id);


--
-- TOC entry 4989 (class 1259 OID 88823)
-- Name: ix_milestones_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_milestones_project_id ON public.milestones USING btree (project_id);


--
-- TOC entry 4959 (class 1259 OID 88682)
-- Name: ix_notification_templates_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notification_templates_id ON public.notification_templates USING btree (id);


--
-- TOC entry 4960 (class 1259 OID 88681)
-- Name: ix_notification_templates_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_notification_templates_name ON public.notification_templates USING btree (name);


--
-- TOC entry 4955 (class 1259 OID 88665)
-- Name: ix_notifications_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_id ON public.notifications USING btree (id);


--
-- TOC entry 4956 (class 1259 OID 88664)
-- Name: ix_notifications_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);


--
-- TOC entry 4922 (class 1259 OID 88525)
-- Name: ix_permissions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);


--
-- TOC entry 4923 (class 1259 OID 88524)
-- Name: ix_permissions_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_permissions_name ON public.permissions USING btree (name);


--
-- TOC entry 4973 (class 1259 OID 88750)
-- Name: ix_proposal_parcels_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_proposal_parcels_id ON public.proposal_parcels USING btree (id);


--
-- TOC entry 4974 (class 1259 OID 88751)
-- Name: ix_proposal_parcels_land_parcel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_proposal_parcels_land_parcel_id ON public.proposal_parcels USING btree (land_parcel_id);


--
-- TOC entry 4975 (class 1259 OID 88749)
-- Name: ix_proposal_parcels_proposal_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_proposal_parcels_proposal_id ON public.proposal_parcels USING btree (proposal_id);


--
-- TOC entry 4931 (class 1259 OID 88566)
-- Name: ix_role_permissions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_permissions_id ON public.role_permissions USING btree (id);


--
-- TOC entry 4932 (class 1259 OID 88567)
-- Name: ix_role_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_permissions_permission_id ON public.role_permissions USING btree (permission_id);


--
-- TOC entry 4933 (class 1259 OID 88565)
-- Name: ix_role_permissions_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_permissions_role_id ON public.role_permissions USING btree (role_id);


--
-- TOC entry 4918 (class 1259 OID 88512)
-- Name: ix_roles_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_roles_id ON public.roles USING btree (id);


--
-- TOC entry 4919 (class 1259 OID 88513)
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- TOC entry 4992 (class 1259 OID 88860)
-- Name: ix_tasks_assigned_to; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_assigned_to ON public.tasks USING btree (assigned_to);


--
-- TOC entry 4993 (class 1259 OID 88861)
-- Name: ix_tasks_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_id ON public.tasks USING btree (id);


--
-- TOC entry 4969 (class 1259 OID 88727)
-- Name: ix_template_milestones_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_template_milestones_id ON public.template_milestones USING btree (id);


--
-- TOC entry 4970 (class 1259 OID 88728)
-- Name: ix_template_milestones_template_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_template_milestones_template_project_id ON public.template_milestones USING btree (template_project_id);


--
-- TOC entry 4947 (class 1259 OID 88626)
-- Name: ix_template_projects_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_template_projects_id ON public.template_projects USING btree (id);


--
-- TOC entry 4948 (class 1259 OID 88625)
-- Name: ix_template_projects_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_template_projects_name ON public.template_projects USING btree (name);


--
-- TOC entry 4984 (class 1259 OID 88801)
-- Name: ix_template_tasks_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_template_tasks_id ON public.template_tasks USING btree (id);


--
-- TOC entry 4985 (class 1259 OID 88802)
-- Name: ix_template_tasks_template_project_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_template_tasks_template_project_id ON public.template_tasks USING btree (template_project_id);


--
-- TOC entry 4926 (class 1259 OID 88545)
-- Name: ix_user_roles_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_roles_id ON public.user_roles USING btree (id);


--
-- TOC entry 4927 (class 1259 OID 88546)
-- Name: ix_user_roles_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_roles_role_id ON public.user_roles USING btree (role_id);


--
-- TOC entry 4928 (class 1259 OID 88544)
-- Name: ix_user_roles_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_roles_user_id ON public.user_roles USING btree (user_id);


--
-- TOC entry 4913 (class 1259 OID 88500)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4914 (class 1259 OID 88499)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 4915 (class 1259 OID 88501)
-- Name: ix_users_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_name ON public.users USING btree (name);


--
-- TOC entry 5010 (class 2606 OID 88637)
-- Name: approval_rules approval_rules_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approval_rules
    ADD CONSTRAINT approval_rules_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5032 (class 2606 OID 88872)
-- Name: approvals approvals_approved_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals
    ADD CONSTRAINT approvals_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);


--
-- TOC entry 5033 (class 2606 OID 88897)
-- Name: approvals approvals_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals
    ADD CONSTRAINT approvals_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5034 (class 2606 OID 88877)
-- Name: approvals approvals_land_parcel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals
    ADD CONSTRAINT approvals_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);


--
-- TOC entry 5035 (class 2606 OID 88892)
-- Name: approvals approvals_milestone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals
    ADD CONSTRAINT approvals_milestone_id_fkey FOREIGN KEY (milestone_id) REFERENCES public.milestones(id);


--
-- TOC entry 5036 (class 2606 OID 88887)
-- Name: approvals approvals_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals
    ADD CONSTRAINT approvals_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);


--
-- TOC entry 5037 (class 2606 OID 88882)
-- Name: approvals approvals_proposal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.approvals
    ADD CONSTRAINT approvals_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);


--
-- TOC entry 5020 (class 2606 OID 88767)
-- Name: development_projects development_projects_project_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.development_projects
    ADD CONSTRAINT development_projects_project_manager_id_fkey FOREIGN KEY (project_manager_id) REFERENCES public.users(id);


--
-- TOC entry 5021 (class 2606 OID 88762)
-- Name: development_projects development_projects_proposal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.development_projects
    ADD CONSTRAINT development_projects_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);


--
-- TOC entry 5038 (class 2606 OID 88933)
-- Name: documents documents_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5039 (class 2606 OID 88913)
-- Name: documents documents_land_parcel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);


--
-- TOC entry 5040 (class 2606 OID 88923)
-- Name: documents documents_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);


--
-- TOC entry 5041 (class 2606 OID 88928)
-- Name: documents documents_proposal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);


--
-- TOC entry 5042 (class 2606 OID 88918)
-- Name: documents documents_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- TOC entry 5007 (class 2606 OID 88601)
-- Name: investment_opportunities investment_opportunities_advisor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_opportunities
    ADD CONSTRAINT investment_opportunities_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES public.users(id);


--
-- TOC entry 5008 (class 2606 OID 88596)
-- Name: investment_opportunities investment_opportunities_investor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_opportunities
    ADD CONSTRAINT investment_opportunities_investor_id_fkey FOREIGN KEY (investor_id) REFERENCES public.users(id);


--
-- TOC entry 5014 (class 2606 OID 88698)
-- Name: investment_proposals investment_proposals_advisor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_proposals
    ADD CONSTRAINT investment_proposals_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES public.users(id);


--
-- TOC entry 5015 (class 2606 OID 88693)
-- Name: investment_proposals investment_proposals_opportunity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.investment_proposals
    ADD CONSTRAINT investment_proposals_opportunity_id_fkey FOREIGN KEY (opportunity_id) REFERENCES public.investment_opportunities(id);


--
-- TOC entry 5006 (class 2606 OID 88578)
-- Name: land_parcels land_parcels_landowner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.land_parcels
    ADD CONSTRAINT land_parcels_landowner_id_fkey FOREIGN KEY (landowner_id) REFERENCES public.users(id);


--
-- TOC entry 5025 (class 2606 OID 88818)
-- Name: milestones milestones_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milestones
    ADD CONSTRAINT milestones_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5026 (class 2606 OID 88813)
-- Name: milestones milestones_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milestones
    ADD CONSTRAINT milestones_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);


--
-- TOC entry 5013 (class 2606 OID 88676)
-- Name: notification_templates notification_templates_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_templates
    ADD CONSTRAINT notification_templates_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5011 (class 2606 OID 88659)
-- Name: notifications notifications_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5012 (class 2606 OID 88654)
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 5018 (class 2606 OID 88744)
-- Name: proposal_parcels proposal_parcels_land_parcel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_parcels
    ADD CONSTRAINT proposal_parcels_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);


--
-- TOC entry 5019 (class 2606 OID 88739)
-- Name: proposal_parcels proposal_parcels_proposal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.proposal_parcels
    ADD CONSTRAINT proposal_parcels_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);


--
-- TOC entry 5004 (class 2606 OID 88560)
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);


--
-- TOC entry 5005 (class 2606 OID 88555)
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- TOC entry 5027 (class 2606 OID 88835)
-- Name: tasks tasks_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id);


--
-- TOC entry 5028 (class 2606 OID 88855)
-- Name: tasks tasks_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5029 (class 2606 OID 88840)
-- Name: tasks tasks_land_parcel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);


--
-- TOC entry 5030 (class 2606 OID 88850)
-- Name: tasks tasks_milestone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_milestone_id_fkey FOREIGN KEY (milestone_id) REFERENCES public.milestones(id);


--
-- TOC entry 5031 (class 2606 OID 88845)
-- Name: tasks tasks_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);


--
-- TOC entry 5016 (class 2606 OID 88722)
-- Name: template_milestones template_milestones_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_milestones
    ADD CONSTRAINT template_milestones_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5017 (class 2606 OID 88717)
-- Name: template_milestones template_milestones_template_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_milestones
    ADD CONSTRAINT template_milestones_template_project_id_fkey FOREIGN KEY (template_project_id) REFERENCES public.template_projects(id);


--
-- TOC entry 5009 (class 2606 OID 88620)
-- Name: template_projects template_projects_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_projects
    ADD CONSTRAINT template_projects_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5022 (class 2606 OID 88796)
-- Name: template_tasks template_tasks_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_tasks
    ADD CONSTRAINT template_tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);


--
-- TOC entry 5023 (class 2606 OID 88791)
-- Name: template_tasks template_tasks_template_milestone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_tasks
    ADD CONSTRAINT template_tasks_template_milestone_id_fkey FOREIGN KEY (template_milestone_id) REFERENCES public.template_milestones(id);


--
-- TOC entry 5024 (class 2606 OID 88786)
-- Name: template_tasks template_tasks_template_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.template_tasks
    ADD CONSTRAINT template_tasks_template_project_id_fkey FOREIGN KEY (template_project_id) REFERENCES public.template_projects(id);


--
-- TOC entry 5002 (class 2606 OID 88539)
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);


--
-- TOC entry 5003 (class 2606 OID 88534)
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2025-09-08 20:08:59

--
-- PostgreSQL database dump complete
--

