<<<<<<< HEAD
# migration.py
# Creates the schema (drops/creates public), types, tables, sequences, constraints, indexes
# and inserts the data from your dump. Uses psycopg (psycopg3).
#
# Connection uses environment variables: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD.

import os
import psycopg


DDL_DROP_CREATE_SCHEMA = """
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
COMMENT ON SCHEMA public IS 'standard public schema';
SET search_path TO public;
"""

DDL_ENUMS = """
CREATE TYPE public.approvalstatus AS ENUM ('PENDING','APPROVED','REJECTED','CANCELLED');
CREATE TYPE public.milestonestatus AS ENUM ('PENDING','IN_PROGRESS','COMPLETED','APPROVED','REJECTED');
CREATE TYPE public.notificationchannel AS ENUM ('EMAIL','SMS','WEB_PUSH','IN_APP');
CREATE TYPE public.notificationstatus AS ENUM ('PENDING','SENT','DELIVERED','FAILED','READ');
CREATE TYPE public.notificationtype AS ENUM ('TASK_ASSIGNED','TASK_COMPLETED','APPROVAL_REQUIRED','APPROVAL_DECISION','MILESTONE_REACHED','DEADLINE_REMINDER','SLA_BREACH','DOCUMENT_UPLOADED','STATUS_CHANGE');
CREATE TYPE public.opportunitystatus AS ENUM ('DRAFT','SUBMITTED','UNDER_REVIEW','APPROVED','REJECTED','EXPIRED');
CREATE TYPE public.parcelstatus AS ENUM ('REGISTERED','FEASIBILITY_ASSIGNED','FEASIBILITY_IN_PROGRESS','FEASIBILITY_COMPLETED','FEASIBILITY_APPROVED','FEASIBILITY_REJECTED','READY_FOR_PROPOSAL','IN_PROPOSAL','IN_DEVELOPMENT','READY_TO_BUILD');
CREATE TYPE public.projectstatus AS ENUM ('INITIATED','IN_PROGRESS','STAGE_GATE','READY_TO_BUILD','CANCELLED','COMPLETED');
CREATE TYPE public.projecttype AS ENUM ('SOLAR','WIND','HYDRO','STORAGE','HYBRID');
CREATE TYPE public.proposalstatus AS ENUM ('DRAFT','SUBMITTED','UNDER_REVIEW','APPROVED','REJECTED','AGREEMENT_SIGNED');
CREATE TYPE public.taskstatus AS ENUM ('PENDING','ASSIGNED','IN_PROGRESS','COMPLETED','REJECTED','CANCELLED');
CREATE TYPE public.usertype AS ENUM ('LANDOWNER','INVESTOR','ADVISOR','ANALYST','PROJECT_MANAGER','GOVERNANCE','ADMIN');
"""

DDL_TABLES = """
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

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying,
    description text,
    user_type public.usertype,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.permissions (
    id integer NOT NULL,
    name character varying,
    description text,
    resource character varying,
    action character varying,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.role_permissions (
    id integer NOT NULL,
    role_id integer,
    permission_id integer,
    created_at timestamp with time zone DEFAULT now()
);

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

CREATE TABLE public.proposal_parcels (
    id integer NOT NULL,
    proposal_id integer,
    land_parcel_id integer,
    allocated_capacity_mw double precision,
    allocated_investment double precision,
    notes text,
    created_at timestamp with time zone DEFAULT now()
);
"""

DDL_SEQUENCES_DEFAULTS = """
CREATE SEQUENCE public.users_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.roles_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.permissions_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.user_roles_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.role_permissions_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.land_parcels_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.investment_opportunities_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.investment_proposals_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.development_projects_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.milestones_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.tasks_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.documents_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.notifications_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.notification_templates_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.template_projects_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.template_milestones_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.template_tasks_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.approval_rules_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.approvals_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.proposal_parcels_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;
ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;
ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;
ALTER SEQUENCE public.role_permissions_id_seq OWNED BY public.role_permissions.id;
ALTER SEQUENCE public.land_parcels_id_seq OWNED BY public.land_parcels.id;
ALTER SEQUENCE public.investment_opportunities_id_seq OWNED BY public.investment_opportunities.id;
ALTER SEQUENCE public.investment_proposals_id_seq OWNED BY public.investment_proposals.id;
ALTER SEQUENCE public.development_projects_id_seq OWNED BY public.development_projects.id;
ALTER SEQUENCE public.milestones_id_seq OWNED BY public.milestones.id;
ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;
ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;
ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;
ALTER SEQUENCE public.notification_templates_id_seq OWNED BY public.notification_templates.id;
ALTER SEQUENCE public.template_projects_id_seq OWNED BY public.template_projects.id;
ALTER SEQUENCE public.template_milestones_id_seq OWNED BY public.template_milestones.id;
ALTER SEQUENCE public.template_tasks_id_seq OWNED BY public.template_tasks.id;
ALTER SEQUENCE public.approval_rules_id_seq OWNED BY public.approval_rules.id;
ALTER SEQUENCE public.approvals_id_seq OWNED BY public.approvals.id;
ALTER SEQUENCE public.proposal_parcels_id_seq OWNED BY public.proposal_parcels.id;

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);
ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);
ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);
ALTER TABLE ONLY public.role_permissions ALTER COLUMN id SET DEFAULT nextval('public.role_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.land_parcels ALTER COLUMN id SET DEFAULT nextval('public.land_parcels_id_seq'::regclass);
ALTER TABLE ONLY public.investment_opportunities ALTER COLUMN id SET DEFAULT nextval('public.investment_opportunities_id_seq'::regclass);
ALTER TABLE ONLY public.investment_proposals ALTER COLUMN id SET DEFAULT nextval('public.investment_proposals_id_seq'::regclass);
ALTER TABLE ONLY public.development_projects ALTER COLUMN id SET DEFAULT nextval('public.development_projects_id_seq'::regclass);
ALTER TABLE ONLY public.milestones ALTER COLUMN id SET DEFAULT nextval('public.milestones_id_seq'::regclass);
ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);
ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);
ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);
ALTER TABLE ONLY public.notification_templates ALTER COLUMN id SET DEFAULT nextval('public.notification_templates_id_seq'::regclass);
ALTER TABLE ONLY public.template_projects ALTER COLUMN id SET DEFAULT nextval('public.template_projects_id_seq'::regclass);
ALTER TABLE ONLY public.template_milestones ALTER COLUMN id SET DEFAULT nextval('public.template_milestones_id_seq'::regclass);
ALTER TABLE ONLY public.template_tasks ALTER COLUMN id SET DEFAULT nextval('public.template_tasks_id_seq'::regclass);
ALTER TABLE ONLY public.approval_rules ALTER COLUMN id SET DEFAULT nextval('public.approval_rules_id_seq'::regclass);
ALTER TABLE ONLY public.approvals ALTER COLUMN id SET DEFAULT nextval('public.approvals_id_seq'::regclass);
ALTER TABLE ONLY public.proposal_parcels ALTER COLUMN id SET DEFAULT nextval('public.proposal_parcels_id_seq'::regclass);
"""

DDL_CONSTRAINTS_INDEXES = """
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.roles ADD CONSTRAINT roles_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.permissions ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.user_roles ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.role_permissions ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.land_parcels ADD CONSTRAINT land_parcels_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.investment_opportunities ADD CONSTRAINT investment_opportunities_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.investment_proposals ADD CONSTRAINT investment_proposals_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.development_projects ADD CONSTRAINT development_projects_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.milestones ADD CONSTRAINT milestones_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.tasks ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.documents ADD CONSTRAINT documents_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.notifications ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.notification_templates ADD CONSTRAINT notification_templates_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.template_projects ADD CONSTRAINT template_projects_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.template_milestones ADD CONSTRAINT template_milestones_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.template_tasks ADD CONSTRAINT template_tasks_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.approval_rules ADD CONSTRAINT approval_rules_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.approvals ADD CONSTRAINT approvals_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.proposal_parcels ADD CONSTRAINT proposal_parcels_pkey PRIMARY KEY (id);

CREATE INDEX ix_users_id ON public.users USING btree (id);
CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);
CREATE INDEX ix_users_name ON public.users USING btree (name);

CREATE INDEX ix_roles_id ON public.roles USING btree (id);
CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);
CREATE UNIQUE INDEX ix_permissions_name ON public.permissions USING btree (name);

CREATE INDEX ix_user_roles_id ON public.user_roles USING btree (id);
CREATE INDEX ix_user_roles_user_id ON public.user_roles USING btree (user_id);
CREATE INDEX ix_user_roles_role_id ON public.user_roles USING btree (role_id);

CREATE INDEX ix_role_permissions_id ON public.role_permissions USING btree (id);
CREATE INDEX ix_role_permissions_role_id ON public.role_permissions USING btree (role_id);
CREATE INDEX ix_role_permissions_permission_id ON public.role_permissions USING btree (permission_id);

CREATE INDEX ix_land_parcels_id ON public.land_parcels USING btree (id);
CREATE INDEX ix_land_parcels_name ON public.land_parcels USING btree (name);
CREATE INDEX ix_land_parcels_landowner_id ON public.land_parcels USING btree (landowner_id);

CREATE INDEX ix_investment_opportunities_id ON public.investment_opportunities USING btree (id);
CREATE INDEX ix_investment_opportunities_title ON public.investment_opportunities USING btree (title);
CREATE INDEX ix_investment_opportunities_investor_id ON public.investment_opportunities USING btree (investor_id);
CREATE INDEX ix_investment_opportunities_advisor_id ON public.investment_opportunities USING btree (advisor_id);

CREATE INDEX ix_investment_proposals_id ON public.investment_proposals USING btree (id);
CREATE INDEX ix_investment_proposals_title ON public.investment_proposals USING btree (title);
CREATE INDEX ix_investment_proposals_opportunity_id ON public.investment_proposals USING btree (opportunity_id);
CREATE INDEX ix_investment_proposals_advisor_id ON public.investment_proposals USING btree (advisor_id);

CREATE INDEX ix_development_projects_id ON public.development_projects USING btree (id);
CREATE INDEX ix_development_projects_name ON public.development_projects USING btree (name);
CREATE INDEX ix_development_projects_proposal_id ON public.development_projects USING btree (proposal_id);
CREATE INDEX ix_development_projects_project_manager_id ON public.development_projects USING btree (project_manager_id);

CREATE INDEX ix_milestones_id ON public.milestones USING btree (id);
CREATE INDEX ix_milestones_project_id ON public.milestones USING btree (project_id);

CREATE INDEX ix_tasks_id ON public.tasks USING btree (id);
CREATE INDEX ix_tasks_assigned_to ON public.tasks USING btree (assigned_to);

CREATE INDEX ix_documents_id ON public.documents USING btree (id);

CREATE INDEX ix_notifications_id ON public.notifications USING btree (id);
CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);

CREATE INDEX ix_notification_templates_id ON public.notification_templates USING btree (id);
CREATE UNIQUE INDEX ix_notification_templates_name ON public.notification_templates USING btree (name);

CREATE INDEX ix_template_projects_id ON public.template_projects USING btree (id);
CREATE INDEX ix_template_projects_name ON public.template_projects USING btree (name);

CREATE INDEX ix_template_milestones_id ON public.template_milestones USING btree (id);
CREATE INDEX ix_template_milestones_template_project_id ON public.template_milestones USING btree (template_project_id);

CREATE INDEX ix_template_tasks_id ON public.template_tasks USING btree (id);
CREATE INDEX ix_template_tasks_template_project_id ON public.template_tasks USING btree (template_project_id);

CREATE INDEX ix_approval_rules_id ON public.approval_rules USING btree (id);
CREATE INDEX ix_approval_rules_name ON public.approval_rules USING btree (name);

CREATE INDEX ix_proposal_parcels_id ON public.proposal_parcels USING btree (id);
CREATE INDEX ix_proposal_parcels_proposal_id ON public.proposal_parcels USING btree (proposal_id);
CREATE INDEX ix_proposal_parcels_land_parcel_id ON public.proposal_parcels USING btree (land_parcel_id);
"""

DDL_FOREIGN_KEYS = """
ALTER TABLE ONLY public.land_parcels
  ADD CONSTRAINT land_parcels_landowner_id_fkey FOREIGN KEY (landowner_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.investment_opportunities
  ADD CONSTRAINT investment_opportunities_investor_id_fkey FOREIGN KEY (investor_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.investment_opportunities
  ADD CONSTRAINT investment_opportunities_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.investment_proposals
  ADD CONSTRAINT investment_proposals_opportunity_id_fkey FOREIGN KEY (opportunity_id) REFERENCES public.investment_opportunities(id);
ALTER TABLE ONLY public.investment_proposals
  ADD CONSTRAINT investment_proposals_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.development_projects
  ADD CONSTRAINT development_projects_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.development_projects
  ADD CONSTRAINT development_projects_project_manager_id_fkey FOREIGN KEY (project_manager_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.milestones
  ADD CONSTRAINT milestones_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.milestones
  ADD CONSTRAINT milestones_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_milestone_id_fkey FOREIGN KEY (milestone_id) REFERENCES public.milestones(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.notifications
  ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.notifications
  ADD CONSTRAINT notifications_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.notification_templates
  ADD CONSTRAINT notification_templates_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.template_projects
  ADD CONSTRAINT template_projects_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.template_milestones
  ADD CONSTRAINT template_milestones_template_project_id_fkey FOREIGN KEY (template_project_id) REFERENCES public.template_projects(id);
ALTER TABLE ONLY public.template_milestones
  ADD CONSTRAINT template_milestones_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.template_tasks
  ADD CONSTRAINT template_tasks_template_project_id_fkey FOREIGN KEY (template_project_id) REFERENCES public.template_projects(id);
ALTER TABLE ONLY public.template_tasks
  ADD CONSTRAINT template_tasks_template_milestone_id_fkey FOREIGN KEY (template_milestone_id) REFERENCES public.template_milestones(id);
ALTER TABLE ONLY public.template_tasks
  ADD CONSTRAINT template_tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.approval_rules
  ADD CONSTRAINT approval_rules_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_milestone_id_fkey FOREIGN KEY (milestone_id) REFERENCES public.milestones(id);

ALTER TABLE ONLY public.proposal_parcels
  ADD CONSTRAINT proposal_parcels_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.proposal_parcels
  ADD CONSTRAINT proposal_parcels_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);

ALTER TABLE ONLY public.role_permissions
  ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);
ALTER TABLE ONLY public.role_permissions
  ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);

ALTER TABLE ONLY public.user_roles
  ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.user_roles
  ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);
"""

DML_INSERTS = """
-- users
INSERT INTO public.users (id, name, email, hashed_password, user_type, is_active, phone, company, created_at, updated_at) VALUES
(1,'Alice Landowner','alice@landowner.com',NULL,'LANDOWNER',true,'555-0001','Land Holdings LLC','2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Bob Property Owner','bob@property.com',NULL,'LANDOWNER',true,'555-0002','Property Group Inc','2025-09-07 11:21:52.089736+05:30',NULL),
(3,'Charlie Investor','charlie@investor.com',NULL,'INVESTOR',true,'555-0003','Green Energy Capital','2025-09-07 11:21:52.089736+05:30',NULL),
(4,'Diana Capital','diana@capital.com',NULL,'INVESTOR',true,'555-0004','Renewable Ventures','2025-09-07 11:21:52.089736+05:30',NULL),
(5,'Eve Advisor','eve@advisor.com',NULL,'ADVISOR',true,'555-0005','RenewMart Advisors','2025-09-07 11:21:52.089736+05:30',NULL),
(6,'Frank Consultant','frank@consultant.com',NULL,'ADVISOR',true,'555-0006','Energy Solutions','2025-09-07 11:21:52.089736+05:30',NULL),
(7,'Grace Analyst','grace@analyst.com',NULL,'ANALYST',true,'555-0007','Technical Services','2025-09-07 11:21:52.089736+05:30',NULL),
(8,'Henry Engineer','henry@engineer.com',NULL,'ANALYST',true,'555-0008','Engineering Corp','2025-09-07 11:21:52.089736+05:30',NULL),
(9,'Ivy Manager','ivy@manager.com',NULL,'PROJECT_MANAGER',true,'555-0009','Project Management Inc','2025-09-07 11:21:52.089736+05:30',NULL),
(10,'Jack Coordinator','jack@coordinator.com',NULL,'PROJECT_MANAGER',true,'555-0010','Development Co','2025-09-07 11:21:52.089736+05:30',NULL),
(11,'Karen Governance','karen@governance.com',NULL,'GOVERNANCE',true,'555-0011','Compliance Office','2025-09-07 11:21:52.089736+05:30',NULL),
(12,'Liam Approver','liam@approver.com',NULL,'GOVERNANCE',true,'555-0012','Approval Board','2025-09-07 11:21:52.089736+05:30',NULL),
(13,'Maya Admin','maya@admin.com',NULL,'ADMIN',true,'555-0013','RenewMart','2025-09-07 11:21:52.089736+05:30',NULL),
(14,'Sai Aryan','sai.namp@test.com','$2b$12$TabdZ5XAWLX2IYgWSqvOfOkMaFBTtXemXeVoMrGquwyz0/iQa6pEa','LANDOWNER',true,'234567890','uibiub','2025-09-07 18:12:47.963362+05:30',NULL),
(15,'Admin User','admin@renewmart.com','$2b$12$.BNF/VEF7s1GNHKvSWcGf.ZQ5D48xWBrAGrXPayLYNPUfp.8ikJY.','ADMIN',true,'+1234567890','RenewMart Inc','2025-09-07 20:46:00.83714+05:30',NULL),
(16,'Test User','test@example.com','$2b$12$fDthVIJeHsjloOBeoqC37eu8zzhDjavW1Y3m9UTatqV3HtcL4igWO','ANALYST',true,'1234567890','Test Company','2025-09-08 16:41:07.06203+05:30',NULL);

-- investment_opportunities
INSERT INTO public.investment_opportunities (id,title,description,status,target_capacity_mw,target_region,investment_amount,expected_returns,investor_id,advisor_id,created_at,updated_at) VALUES
(1,'Solar Development Opportunity - West Coast','Large-scale solar development opportunity in California','APPROVED',500,'California',750000000,12.5,3,5,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Wind Energy Portfolio - Texas','Multi-site wind energy development in Texas','UNDER_REVIEW',800,'Texas',1200000000,15,4,6,'2025-09-07 11:21:52.089736+05:30',NULL);

-- investment_proposals
INSERT INTO public.investment_proposals (id,title,description,status,total_capacity_mw,total_investment,expected_completion_date,opportunity_id,advisor_id,created_at,updated_at) VALUES
(1,'California Solar Portfolio Proposal','Comprehensive solar development proposal for California sites','APPROVED',500,750000000,'2026-09-07 11:21:52.147507',1,5,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Texas Wind Energy Proposal','Wind energy development proposal for Texas region','UNDER_REVIEW',800,1200000000,'2026-12-01 11:21:52.147507',2,6,'2025-09-07 11:21:52.089736+05:30',NULL);

-- land_parcels
INSERT INTO public.land_parcels (id,name,address,size_acres,coordinates,description,status,landowner_id,feasibility_completed,feasibility_score,feasibility_notes,created_at,updated_at) VALUES
(1,'Solar Farm Site A','123 Solar Lane, Desert Valley, CA',150,'{"lat": 34.0522, "lng": -118.2437}','Prime solar development site with excellent sun exposure','REGISTERED',1,false,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Wind Energy Site B','456 Windy Ridge, Mountain View, TX',200,'{"lat": 32.7767, "lng": -96.797}','High elevation site ideal for wind turbines','FEASIBILITY_COMPLETED',2,true,8.5,'Excellent wind conditions, minimal environmental impact','2025-09-07 11:21:52.089736+05:30',NULL),
(3,'Hybrid Energy Complex','789 Renewable Blvd, Green City, OR',300,'{"lat": 45.5152, "lng": -122.6784}','Large site suitable for solar + storage hybrid project','READY_FOR_PROPOSAL',1,true,9.2,'Perfect for hybrid renewable energy development','2025-09-07 11:21:52.089736+05:30',NULL);

-- development_projects
INSERT INTO public.development_projects (id,name,description,status,project_type,total_capacity_mw,total_investment,target_completion_date,actual_completion_date,proposal_id,project_manager_id,created_at,updated_at) VALUES
(1,'California Solar Development Project','Large-scale solar development in California','IN_PROGRESS','SOLAR',500,750000000,'2026-09-07 11:21:52.161773',NULL,1,9,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Texas Wind Energy Project','Wind energy development in Texas','INITIATED','WIND',800,1200000000,'2026-12-01 11:21:52.161773',NULL,2,10,'2025-09-07 11:21:52.089736+05:30',NULL);

-- milestones
INSERT INTO public.milestones (id,title,description,status,target_date,completed_at,project_id,created_at,created_by) VALUES
(1,'Feasibility Complete','All feasibility studies completed and approved','COMPLETED','2025-08-28 11:21:52.178514','2025-09-02 11:21:52.178514',1,'2025-09-07 11:21:52.089736+05:30',9),
(2,'Permits Approved','All required permits obtained','IN_PROGRESS','2025-11-06 11:21:52.178514',NULL,1,'2025-09-07 11:21:52.089736+05:30',9),
(3,'Environmental Clearance','Environmental impact assessment completed','PENDING','2025-12-06 11:21:52.178514',NULL,2,'2025-09-07 11:21:52.089736+05:30',10);

-- approvals
INSERT INTO public.approvals (id,approval_type,status,comments,approved_by,approved_at,land_parcel_id,proposal_id,project_id,milestone_id,created_at,created_by) VALUES
(1,'feasibility','APPROVED','Feasibility study meets all requirements',11,'2025-09-04 11:21:52.182558',1,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',5),
(2,'proposal','APPROVED','Proposal approved for development',12,'2025-09-06 11:21:52.182558',NULL,1,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',5),
(3,'milestone','PENDING','Awaiting environmental clearance',NULL,NULL,2,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',6);

-- tasks
INSERT INTO public.tasks (id,title,description,status,priority,assigned_to,due_date,completed_at,land_parcel_id,project_id,milestone_id,created_at,created_by) VALUES
(1,'Site Feasibility Study','Conduct comprehensive feasibility study for solar site','COMPLETED','high',7,'2025-10-07 11:21:52.167164','2025-09-02 11:21:52.167164',1,1,NULL,'2025-09-07 11:21:52.089736+05:30',5),
(2,'Environmental Impact Assessment','Complete environmental impact assessment for wind site','IN_PROGRESS','high',8,'2025-10-22 11:21:52.167164',NULL,2,2,NULL,'2025-09-07 11:21:52.089736+05:30',6),
(3,'Permit Application Submission','Submit all required permits for hybrid energy project','PENDING','urgent',7,'2025-09-22 11:21:52.167164',NULL,3,1,NULL,'2025-09-07 11:21:52.089736+05:30',9);

-- documents
INSERT INTO public.documents (id,name,file_path,file_size,mime_type,document_type,checksum,land_parcel_id,task_id,project_id,proposal_id,created_at,created_by) VALUES
(1,'Feasibility Study Report - Site A','/documents/feasibility_site_a.pdf',2048000,'application/pdf','feasibility_report','abc123def456',1,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',7),
(2,'Environmental Impact Assessment','/documents/eia_wind_site.pdf',1536000,'application/pdf','environmental_assessment','def456ghi789',2,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',8),
(3,'Development Service Agreement','/documents/dsa_proposal_1.pdf',1024000,'application/pdf','agreement','ghi789jkl012',NULL,NULL,NULL,1,'2025-09-07 11:21:52.089736+05:30',5);

-- notification_templates
INSERT INTO public.notification_templates (id,name,notification_type,channel,subject_template,message_template,variables,is_active,priority,created_at,created_by,updated_at) VALUES
(1,'Task Assignment Email','TASK_ASSIGNED','EMAIL','New Task Assigned: {task_title}','You have been assigned a new task: {task_title}. Due date: {due_date}','["task_title", "due_date"]',true,1,'2025-09-07 11:21:52.089736+05:30',13,NULL),
(2,'Approval Required','APPROVAL_REQUIRED','IN_APP','Approval Required: {approval_type}','Approval required for {approval_type}: {entity_name}','["approval_type", "entity_name"]',true,1,'2025-09-07 11:21:52.089736+05:30',13,NULL);

-- template_projects
INSERT INTO public.template_projects (id,name,description,project_type,region,size_band_min,size_band_max,config,created_at,created_by) VALUES
(1,'Solar Farm Template - California','Standard template for solar farm development in California','SOLAR','California',100,500,'{"required_milestones": ["feasibility", "permits", "construction"], "estimated_duration_days": 365, "required_approvals": ["environmental", "zoning", "utility"]}','2025-09-07 11:21:52.089736+05:30',13),
(2,'Wind Farm Template - Texas','Standard template for wind farm development in Texas','WIND','Texas',200,1000,'{"required_milestones": ["feasibility", "permits", "construction"], "estimated_duration_days": 450, "required_approvals": ["environmental", "aviation", "utility"]}','2025-09-07 11:21:52.089736+05:30',13);

-- proposal_parcels
INSERT INTO public.proposal_parcels (id,proposal_id,land_parcel_id,allocated_capacity_mw,allocated_investment,notes,created_at) VALUES
(1,1,1,150,225000000,'Primary solar site with excellent conditions','2025-09-07 11:21:52.089736+05:30'),
(2,1,3,350,525000000,'Hybrid solar + storage site','2025-09-07 11:21:52.089736+05:30'),
(3,2,2,200,300000000,'Wind energy development site','2025-09-07 11:21:52.089736+05:30');
"""

DML_SEQUENCES_SETVAL = """
SELECT pg_catalog.setval('public.users_id_seq', 16, true);
SELECT pg_catalog.setval('public.roles_id_seq', 1, false);
SELECT pg_catalog.setval('public.permissions_id_seq', 1, false);
SELECT pg_catalog.setval('public.user_roles_id_seq', 1, false);
SELECT pg_catalog.setval('public.role_permissions_id_seq', 1, false);
SELECT pg_catalog.setval('public.land_parcels_id_seq', 3, true);
SELECT pg_catalog.setval('public.investment_opportunities_id_seq', 2, true);
SELECT pg_catalog.setval('public.investment_proposals_id_seq', 2, true);
SELECT pg_catalog.setval('public.development_projects_id_seq', 2, true);
SELECT pg_catalog.setval('public.milestones_id_seq', 3, true);
SELECT pg_catalog.setval('public.tasks_id_seq', 3, true);
SELECT pg_catalog.setval('public.documents_id_seq', 3, true);
SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);
SELECT pg_catalog.setval('public.notification_templates_id_seq', 2, true);
SELECT pg_catalog.setval('public.template_projects_id_seq', 2, true);
SELECT pg_catalog.setval('public.template_milestones_id_seq', 1, false);
SELECT pg_catalog.setval('public.template_tasks_id_seq', 1, false);
SELECT pg_catalog.setval('public.approval_rules_id_seq', 1, false);
SELECT pg_catalog.setval('public.approvals_id_seq', 3, true);
SELECT pg_catalog.setval('public.proposal_parcels_id_seq', 3, true);
"""

def main():
    conn = psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "renewmart_db"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "RenewMart_Password")
    )
    try:
        with conn:
            with conn.cursor() as cur:
                # Speed up DDL; ensure fresh start
                cur.execute("SET client_min_messages = WARNING;")
                cur.execute(DDL_DROP_CREATE_SCHEMA)
                cur.execute(DDL_ENUMS)
                cur.execute(DDL_TABLES)
                cur.execute(DDL_SEQUENCES_DEFAULTS)
                cur.execute(DDL_CONSTRAINTS_INDEXES)
                cur.execute(DDL_FOREIGN_KEYS)
                cur.execute(DML_INSERTS)
                cur.execute(DML_SEQUENCES_SETVAL)
        print("Migration completed successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
=======
# migration.py
# Creates the schema (drops/creates public), types, tables, sequences, constraints, indexes
# and inserts the data from your dump. Uses psycopg (psycopg3).
#
# Connection uses environment variables: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD.

import os
import psycopg


DDL_DROP_CREATE_SCHEMA = """
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
COMMENT ON SCHEMA public IS 'standard public schema';
SET search_path TO public;
"""

DDL_ENUMS = """
CREATE TYPE public.approvalstatus AS ENUM ('PENDING','APPROVED','REJECTED','CANCELLED');
CREATE TYPE public.milestonestatus AS ENUM ('PENDING','IN_PROGRESS','COMPLETED','APPROVED','REJECTED');
CREATE TYPE public.notificationchannel AS ENUM ('EMAIL','SMS','WEB_PUSH','IN_APP');
CREATE TYPE public.notificationstatus AS ENUM ('PENDING','SENT','DELIVERED','FAILED','READ');
CREATE TYPE public.notificationtype AS ENUM ('TASK_ASSIGNED','TASK_COMPLETED','APPROVAL_REQUIRED','APPROVAL_DECISION','MILESTONE_REACHED','DEADLINE_REMINDER','SLA_BREACH','DOCUMENT_UPLOADED','STATUS_CHANGE');
CREATE TYPE public.opportunitystatus AS ENUM ('DRAFT','SUBMITTED','UNDER_REVIEW','APPROVED','REJECTED','EXPIRED');
CREATE TYPE public.parcelstatus AS ENUM ('REGISTERED','FEASIBILITY_ASSIGNED','FEASIBILITY_IN_PROGRESS','FEASIBILITY_COMPLETED','FEASIBILITY_APPROVED','FEASIBILITY_REJECTED','READY_FOR_PROPOSAL','IN_PROPOSAL','IN_DEVELOPMENT','READY_TO_BUILD');
CREATE TYPE public.projectstatus AS ENUM ('INITIATED','IN_PROGRESS','STAGE_GATE','READY_TO_BUILD','CANCELLED','COMPLETED');
CREATE TYPE public.projecttype AS ENUM ('SOLAR','WIND','HYDRO','STORAGE','HYBRID');
CREATE TYPE public.proposalstatus AS ENUM ('DRAFT','SUBMITTED','UNDER_REVIEW','APPROVED','REJECTED','AGREEMENT_SIGNED');
CREATE TYPE public.taskstatus AS ENUM ('PENDING','ASSIGNED','IN_PROGRESS','COMPLETED','REJECTED','CANCELLED');
CREATE TYPE public.usertype AS ENUM ('LANDOWNER','INVESTOR','ADVISOR','ANALYST','PROJECT_MANAGER','GOVERNANCE','ADMIN');
"""

DDL_TABLES = """
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

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying,
    description text,
    user_type public.usertype,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.permissions (
    id integer NOT NULL,
    name character varying,
    description text,
    resource character varying,
    action character varying,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.user_roles (
    id integer NOT NULL,
    user_id integer,
    role_id integer,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE public.role_permissions (
    id integer NOT NULL,
    role_id integer,
    permission_id integer,
    created_at timestamp with time zone DEFAULT now()
);

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

CREATE TABLE public.proposal_parcels (
    id integer NOT NULL,
    proposal_id integer,
    land_parcel_id integer,
    allocated_capacity_mw double precision,
    allocated_investment double precision,
    notes text,
    created_at timestamp with time zone DEFAULT now()
);
"""

DDL_SEQUENCES_DEFAULTS = """
CREATE SEQUENCE public.users_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.roles_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.permissions_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.user_roles_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.role_permissions_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.land_parcels_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.investment_opportunities_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.investment_proposals_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.development_projects_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.milestones_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.tasks_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.documents_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.notifications_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.notification_templates_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.template_projects_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.template_milestones_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.template_tasks_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.approval_rules_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.approvals_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
CREATE SEQUENCE public.proposal_parcels_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;
ALTER SEQUENCE public.permissions_id_seq OWNED BY public.permissions.id;
ALTER SEQUENCE public.user_roles_id_seq OWNED BY public.user_roles.id;
ALTER SEQUENCE public.role_permissions_id_seq OWNED BY public.role_permissions.id;
ALTER SEQUENCE public.land_parcels_id_seq OWNED BY public.land_parcels.id;
ALTER SEQUENCE public.investment_opportunities_id_seq OWNED BY public.investment_opportunities.id;
ALTER SEQUENCE public.investment_proposals_id_seq OWNED BY public.investment_proposals.id;
ALTER SEQUENCE public.development_projects_id_seq OWNED BY public.development_projects.id;
ALTER SEQUENCE public.milestones_id_seq OWNED BY public.milestones.id;
ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;
ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;
ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;
ALTER SEQUENCE public.notification_templates_id_seq OWNED BY public.notification_templates.id;
ALTER SEQUENCE public.template_projects_id_seq OWNED BY public.template_projects.id;
ALTER SEQUENCE public.template_milestones_id_seq OWNED BY public.template_milestones.id;
ALTER SEQUENCE public.template_tasks_id_seq OWNED BY public.template_tasks.id;
ALTER SEQUENCE public.approval_rules_id_seq OWNED BY public.approval_rules.id;
ALTER SEQUENCE public.approvals_id_seq OWNED BY public.approvals.id;
ALTER SEQUENCE public.proposal_parcels_id_seq OWNED BY public.proposal_parcels.id;

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);
ALTER TABLE ONLY public.permissions ALTER COLUMN id SET DEFAULT nextval('public.permissions_id_seq'::regclass);
ALTER TABLE ONLY public.user_roles ALTER COLUMN id SET DEFAULT nextval('public.user_roles_id_seq'::regclass);
ALTER TABLE ONLY public.role_permissions ALTER COLUMN id SET DEFAULT nextval('public.role_permissions_id_seq'::regclass);
ALTER TABLE ONLY public.land_parcels ALTER COLUMN id SET DEFAULT nextval('public.land_parcels_id_seq'::regclass);
ALTER TABLE ONLY public.investment_opportunities ALTER COLUMN id SET DEFAULT nextval('public.investment_opportunities_id_seq'::regclass);
ALTER TABLE ONLY public.investment_proposals ALTER COLUMN id SET DEFAULT nextval('public.investment_proposals_id_seq'::regclass);
ALTER TABLE ONLY public.development_projects ALTER COLUMN id SET DEFAULT nextval('public.development_projects_id_seq'::regclass);
ALTER TABLE ONLY public.milestones ALTER COLUMN id SET DEFAULT nextval('public.milestones_id_seq'::regclass);
ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);
ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);
ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);
ALTER TABLE ONLY public.notification_templates ALTER COLUMN id SET DEFAULT nextval('public.notification_templates_id_seq'::regclass);
ALTER TABLE ONLY public.template_projects ALTER COLUMN id SET DEFAULT nextval('public.template_projects_id_seq'::regclass);
ALTER TABLE ONLY public.template_milestones ALTER COLUMN id SET DEFAULT nextval('public.template_milestones_id_seq'::regclass);
ALTER TABLE ONLY public.template_tasks ALTER COLUMN id SET DEFAULT nextval('public.template_tasks_id_seq'::regclass);
ALTER TABLE ONLY public.approval_rules ALTER COLUMN id SET DEFAULT nextval('public.approval_rules_id_seq'::regclass);
ALTER TABLE ONLY public.approvals ALTER COLUMN id SET DEFAULT nextval('public.approvals_id_seq'::regclass);
ALTER TABLE ONLY public.proposal_parcels ALTER COLUMN id SET DEFAULT nextval('public.proposal_parcels_id_seq'::regclass);
"""

DDL_CONSTRAINTS_INDEXES = """
ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.roles ADD CONSTRAINT roles_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.permissions ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.user_roles ADD CONSTRAINT user_roles_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.role_permissions ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.land_parcels ADD CONSTRAINT land_parcels_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.investment_opportunities ADD CONSTRAINT investment_opportunities_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.investment_proposals ADD CONSTRAINT investment_proposals_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.development_projects ADD CONSTRAINT development_projects_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.milestones ADD CONSTRAINT milestones_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.tasks ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.documents ADD CONSTRAINT documents_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.notifications ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.notification_templates ADD CONSTRAINT notification_templates_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.template_projects ADD CONSTRAINT template_projects_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.template_milestones ADD CONSTRAINT template_milestones_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.template_tasks ADD CONSTRAINT template_tasks_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.approval_rules ADD CONSTRAINT approval_rules_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.approvals ADD CONSTRAINT approvals_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.proposal_parcels ADD CONSTRAINT proposal_parcels_pkey PRIMARY KEY (id);

CREATE INDEX ix_users_id ON public.users USING btree (id);
CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);
CREATE INDEX ix_users_name ON public.users USING btree (name);

CREATE INDEX ix_roles_id ON public.roles USING btree (id);
CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);

CREATE INDEX ix_permissions_id ON public.permissions USING btree (id);
CREATE UNIQUE INDEX ix_permissions_name ON public.permissions USING btree (name);

CREATE INDEX ix_user_roles_id ON public.user_roles USING btree (id);
CREATE INDEX ix_user_roles_user_id ON public.user_roles USING btree (user_id);
CREATE INDEX ix_user_roles_role_id ON public.user_roles USING btree (role_id);

CREATE INDEX ix_role_permissions_id ON public.role_permissions USING btree (id);
CREATE INDEX ix_role_permissions_role_id ON public.role_permissions USING btree (role_id);
CREATE INDEX ix_role_permissions_permission_id ON public.role_permissions USING btree (permission_id);

CREATE INDEX ix_land_parcels_id ON public.land_parcels USING btree (id);
CREATE INDEX ix_land_parcels_name ON public.land_parcels USING btree (name);
CREATE INDEX ix_land_parcels_landowner_id ON public.land_parcels USING btree (landowner_id);

CREATE INDEX ix_investment_opportunities_id ON public.investment_opportunities USING btree (id);
CREATE INDEX ix_investment_opportunities_title ON public.investment_opportunities USING btree (title);
CREATE INDEX ix_investment_opportunities_investor_id ON public.investment_opportunities USING btree (investor_id);
CREATE INDEX ix_investment_opportunities_advisor_id ON public.investment_opportunities USING btree (advisor_id);

CREATE INDEX ix_investment_proposals_id ON public.investment_proposals USING btree (id);
CREATE INDEX ix_investment_proposals_title ON public.investment_proposals USING btree (title);
CREATE INDEX ix_investment_proposals_opportunity_id ON public.investment_proposals USING btree (opportunity_id);
CREATE INDEX ix_investment_proposals_advisor_id ON public.investment_proposals USING btree (advisor_id);

CREATE INDEX ix_development_projects_id ON public.development_projects USING btree (id);
CREATE INDEX ix_development_projects_name ON public.development_projects USING btree (name);
CREATE INDEX ix_development_projects_proposal_id ON public.development_projects USING btree (proposal_id);
CREATE INDEX ix_development_projects_project_manager_id ON public.development_projects USING btree (project_manager_id);

CREATE INDEX ix_milestones_id ON public.milestones USING btree (id);
CREATE INDEX ix_milestones_project_id ON public.milestones USING btree (project_id);

CREATE INDEX ix_tasks_id ON public.tasks USING btree (id);
CREATE INDEX ix_tasks_assigned_to ON public.tasks USING btree (assigned_to);

CREATE INDEX ix_documents_id ON public.documents USING btree (id);

CREATE INDEX ix_notifications_id ON public.notifications USING btree (id);
CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);

CREATE INDEX ix_notification_templates_id ON public.notification_templates USING btree (id);
CREATE UNIQUE INDEX ix_notification_templates_name ON public.notification_templates USING btree (name);

CREATE INDEX ix_template_projects_id ON public.template_projects USING btree (id);
CREATE INDEX ix_template_projects_name ON public.template_projects USING btree (name);

CREATE INDEX ix_template_milestones_id ON public.template_milestones USING btree (id);
CREATE INDEX ix_template_milestones_template_project_id ON public.template_milestones USING btree (template_project_id);

CREATE INDEX ix_template_tasks_id ON public.template_tasks USING btree (id);
CREATE INDEX ix_template_tasks_template_project_id ON public.template_tasks USING btree (template_project_id);

CREATE INDEX ix_approval_rules_id ON public.approval_rules USING btree (id);
CREATE INDEX ix_approval_rules_name ON public.approval_rules USING btree (name);

CREATE INDEX ix_proposal_parcels_id ON public.proposal_parcels USING btree (id);
CREATE INDEX ix_proposal_parcels_proposal_id ON public.proposal_parcels USING btree (proposal_id);
CREATE INDEX ix_proposal_parcels_land_parcel_id ON public.proposal_parcels USING btree (land_parcel_id);
"""

DDL_FOREIGN_KEYS = """
ALTER TABLE ONLY public.land_parcels
  ADD CONSTRAINT land_parcels_landowner_id_fkey FOREIGN KEY (landowner_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.investment_opportunities
  ADD CONSTRAINT investment_opportunities_investor_id_fkey FOREIGN KEY (investor_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.investment_opportunities
  ADD CONSTRAINT investment_opportunities_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.investment_proposals
  ADD CONSTRAINT investment_proposals_opportunity_id_fkey FOREIGN KEY (opportunity_id) REFERENCES public.investment_opportunities(id);
ALTER TABLE ONLY public.investment_proposals
  ADD CONSTRAINT investment_proposals_advisor_id_fkey FOREIGN KEY (advisor_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.development_projects
  ADD CONSTRAINT development_projects_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.development_projects
  ADD CONSTRAINT development_projects_project_manager_id_fkey FOREIGN KEY (project_manager_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.milestones
  ADD CONSTRAINT milestones_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.milestones
  ADD CONSTRAINT milestones_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_milestone_id_fkey FOREIGN KEY (milestone_id) REFERENCES public.milestones(id);
ALTER TABLE ONLY public.tasks
  ADD CONSTRAINT tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.documents
  ADD CONSTRAINT documents_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.notifications
  ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.notifications
  ADD CONSTRAINT notifications_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.notification_templates
  ADD CONSTRAINT notification_templates_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.template_projects
  ADD CONSTRAINT template_projects_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.template_milestones
  ADD CONSTRAINT template_milestones_template_project_id_fkey FOREIGN KEY (template_project_id) REFERENCES public.template_projects(id);
ALTER TABLE ONLY public.template_milestones
  ADD CONSTRAINT template_milestones_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.template_tasks
  ADD CONSTRAINT template_tasks_template_project_id_fkey FOREIGN KEY (template_project_id) REFERENCES public.template_projects(id);
ALTER TABLE ONLY public.template_tasks
  ADD CONSTRAINT template_tasks_template_milestone_id_fkey FOREIGN KEY (template_milestone_id) REFERENCES public.template_milestones(id);
ALTER TABLE ONLY public.template_tasks
  ADD CONSTRAINT template_tasks_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.approval_rules
  ADD CONSTRAINT approval_rules_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);

ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES public.users(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.development_projects(id);
ALTER TABLE ONLY public.approvals
  ADD CONSTRAINT approvals_milestone_id_fkey FOREIGN KEY (milestone_id) REFERENCES public.milestones(id);

ALTER TABLE ONLY public.proposal_parcels
  ADD CONSTRAINT proposal_parcels_proposal_id_fkey FOREIGN KEY (proposal_id) REFERENCES public.investment_proposals(id);
ALTER TABLE ONLY public.proposal_parcels
  ADD CONSTRAINT proposal_parcels_land_parcel_id_fkey FOREIGN KEY (land_parcel_id) REFERENCES public.land_parcels(id);

ALTER TABLE ONLY public.role_permissions
  ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);
ALTER TABLE ONLY public.role_permissions
  ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id);

ALTER TABLE ONLY public.user_roles
  ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
ALTER TABLE ONLY public.user_roles
  ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id);
"""

DML_INSERTS = """
-- users
INSERT INTO public.users (id, name, email, hashed_password, user_type, is_active, phone, company, created_at, updated_at) VALUES
(1,'Alice Landowner','alice@landowner.com',NULL,'LANDOWNER',true,'555-0001','Land Holdings LLC','2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Bob Property Owner','bob@property.com',NULL,'LANDOWNER',true,'555-0002','Property Group Inc','2025-09-07 11:21:52.089736+05:30',NULL),
(3,'Charlie Investor','charlie@investor.com',NULL,'INVESTOR',true,'555-0003','Green Energy Capital','2025-09-07 11:21:52.089736+05:30',NULL),
(4,'Diana Capital','diana@capital.com',NULL,'INVESTOR',true,'555-0004','Renewable Ventures','2025-09-07 11:21:52.089736+05:30',NULL),
(5,'Eve Advisor','eve@advisor.com',NULL,'ADVISOR',true,'555-0005','RenewMart Advisors','2025-09-07 11:21:52.089736+05:30',NULL),
(6,'Frank Consultant','frank@consultant.com',NULL,'ADVISOR',true,'555-0006','Energy Solutions','2025-09-07 11:21:52.089736+05:30',NULL),
(7,'Grace Analyst','grace@analyst.com',NULL,'ANALYST',true,'555-0007','Technical Services','2025-09-07 11:21:52.089736+05:30',NULL),
(8,'Henry Engineer','henry@engineer.com',NULL,'ANALYST',true,'555-0008','Engineering Corp','2025-09-07 11:21:52.089736+05:30',NULL),
(9,'Ivy Manager','ivy@manager.com',NULL,'PROJECT_MANAGER',true,'555-0009','Project Management Inc','2025-09-07 11:21:52.089736+05:30',NULL),
(10,'Jack Coordinator','jack@coordinator.com',NULL,'PROJECT_MANAGER',true,'555-0010','Development Co','2025-09-07 11:21:52.089736+05:30',NULL),
(11,'Karen Governance','karen@governance.com',NULL,'GOVERNANCE',true,'555-0011','Compliance Office','2025-09-07 11:21:52.089736+05:30',NULL),
(12,'Liam Approver','liam@approver.com',NULL,'GOVERNANCE',true,'555-0012','Approval Board','2025-09-07 11:21:52.089736+05:30',NULL),
(13,'Maya Admin','maya@admin.com',NULL,'ADMIN',true,'555-0013','RenewMart','2025-09-07 11:21:52.089736+05:30',NULL),
(14,'Sai Aryan','sai.namp@test.com','$2b$12$TabdZ5XAWLX2IYgWSqvOfOkMaFBTtXemXeVoMrGquwyz0/iQa6pEa','LANDOWNER',true,'234567890','uibiub','2025-09-07 18:12:47.963362+05:30',NULL),
(15,'Admin User','admin@renewmart.com','$2b$12$.BNF/VEF7s1GNHKvSWcGf.ZQ5D48xWBrAGrXPayLYNPUfp.8ikJY.','ADMIN',true,'+1234567890','RenewMart Inc','2025-09-07 20:46:00.83714+05:30',NULL),
(16,'Test User','test@example.com','$2b$12$fDthVIJeHsjloOBeoqC37eu8zzhDjavW1Y3m9UTatqV3HtcL4igWO','ANALYST',true,'1234567890','Test Company','2025-09-08 16:41:07.06203+05:30',NULL);

-- investment_opportunities
INSERT INTO public.investment_opportunities (id,title,description,status,target_capacity_mw,target_region,investment_amount,expected_returns,investor_id,advisor_id,created_at,updated_at) VALUES
(1,'Solar Development Opportunity - West Coast','Large-scale solar development opportunity in California','APPROVED',500,'California',750000000,12.5,3,5,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Wind Energy Portfolio - Texas','Multi-site wind energy development in Texas','UNDER_REVIEW',800,'Texas',1200000000,15,4,6,'2025-09-07 11:21:52.089736+05:30',NULL);

-- investment_proposals
INSERT INTO public.investment_proposals (id,title,description,status,total_capacity_mw,total_investment,expected_completion_date,opportunity_id,advisor_id,created_at,updated_at) VALUES
(1,'California Solar Portfolio Proposal','Comprehensive solar development proposal for California sites','APPROVED',500,750000000,'2026-09-07 11:21:52.147507',1,5,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Texas Wind Energy Proposal','Wind energy development proposal for Texas region','UNDER_REVIEW',800,1200000000,'2026-12-01 11:21:52.147507',2,6,'2025-09-07 11:21:52.089736+05:30',NULL);

-- land_parcels
INSERT INTO public.land_parcels (id,name,address,size_acres,coordinates,description,status,landowner_id,feasibility_completed,feasibility_score,feasibility_notes,created_at,updated_at) VALUES
(1,'Solar Farm Site A','123 Solar Lane, Desert Valley, CA',150,'{"lat": 34.0522, "lng": -118.2437}','Prime solar development site with excellent sun exposure','REGISTERED',1,false,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Wind Energy Site B','456 Windy Ridge, Mountain View, TX',200,'{"lat": 32.7767, "lng": -96.797}','High elevation site ideal for wind turbines','FEASIBILITY_COMPLETED',2,true,8.5,'Excellent wind conditions, minimal environmental impact','2025-09-07 11:21:52.089736+05:30',NULL),
(3,'Hybrid Energy Complex','789 Renewable Blvd, Green City, OR',300,'{"lat": 45.5152, "lng": -122.6784}','Large site suitable for solar + storage hybrid project','READY_FOR_PROPOSAL',1,true,9.2,'Perfect for hybrid renewable energy development','2025-09-07 11:21:52.089736+05:30',NULL);

-- development_projects
INSERT INTO public.development_projects (id,name,description,status,project_type,total_capacity_mw,total_investment,target_completion_date,actual_completion_date,proposal_id,project_manager_id,created_at,updated_at) VALUES
(1,'California Solar Development Project','Large-scale solar development in California','IN_PROGRESS','SOLAR',500,750000000,'2026-09-07 11:21:52.161773',NULL,1,9,'2025-09-07 11:21:52.089736+05:30',NULL),
(2,'Texas Wind Energy Project','Wind energy development in Texas','INITIATED','WIND',800,1200000000,'2026-12-01 11:21:52.161773',NULL,2,10,'2025-09-07 11:21:52.089736+05:30',NULL);

-- milestones
INSERT INTO public.milestones (id,title,description,status,target_date,completed_at,project_id,created_at,created_by) VALUES
(1,'Feasibility Complete','All feasibility studies completed and approved','COMPLETED','2025-08-28 11:21:52.178514','2025-09-02 11:21:52.178514',1,'2025-09-07 11:21:52.089736+05:30',9),
(2,'Permits Approved','All required permits obtained','IN_PROGRESS','2025-11-06 11:21:52.178514',NULL,1,'2025-09-07 11:21:52.089736+05:30',9),
(3,'Environmental Clearance','Environmental impact assessment completed','PENDING','2025-12-06 11:21:52.178514',NULL,2,'2025-09-07 11:21:52.089736+05:30',10);

-- approvals
INSERT INTO public.approvals (id,approval_type,status,comments,approved_by,approved_at,land_parcel_id,proposal_id,project_id,milestone_id,created_at,created_by) VALUES
(1,'feasibility','APPROVED','Feasibility study meets all requirements',11,'2025-09-04 11:21:52.182558',1,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',5),
(2,'proposal','APPROVED','Proposal approved for development',12,'2025-09-06 11:21:52.182558',NULL,1,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',5),
(3,'milestone','PENDING','Awaiting environmental clearance',NULL,NULL,2,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',6);

-- tasks
INSERT INTO public.tasks (id,title,description,status,priority,assigned_to,due_date,completed_at,land_parcel_id,project_id,milestone_id,created_at,created_by) VALUES
(1,'Site Feasibility Study','Conduct comprehensive feasibility study for solar site','COMPLETED','high',7,'2025-10-07 11:21:52.167164','2025-09-02 11:21:52.167164',1,1,NULL,'2025-09-07 11:21:52.089736+05:30',5),
(2,'Environmental Impact Assessment','Complete environmental impact assessment for wind site','IN_PROGRESS','high',8,'2025-10-22 11:21:52.167164',NULL,2,2,NULL,'2025-09-07 11:21:52.089736+05:30',6),
(3,'Permit Application Submission','Submit all required permits for hybrid energy project','PENDING','urgent',7,'2025-09-22 11:21:52.167164',NULL,3,1,NULL,'2025-09-07 11:21:52.089736+05:30',9);

-- documents
INSERT INTO public.documents (id,name,file_path,file_size,mime_type,document_type,checksum,land_parcel_id,task_id,project_id,proposal_id,created_at,created_by) VALUES
(1,'Feasibility Study Report - Site A','/documents/feasibility_site_a.pdf',2048000,'application/pdf','feasibility_report','abc123def456',1,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',7),
(2,'Environmental Impact Assessment','/documents/eia_wind_site.pdf',1536000,'application/pdf','environmental_assessment','def456ghi789',2,NULL,NULL,NULL,'2025-09-07 11:21:52.089736+05:30',8),
(3,'Development Service Agreement','/documents/dsa_proposal_1.pdf',1024000,'application/pdf','agreement','ghi789jkl012',NULL,NULL,NULL,1,'2025-09-07 11:21:52.089736+05:30',5);

-- notification_templates
INSERT INTO public.notification_templates (id,name,notification_type,channel,subject_template,message_template,variables,is_active,priority,created_at,created_by,updated_at) VALUES
(1,'Task Assignment Email','TASK_ASSIGNED','EMAIL','New Task Assigned: {task_title}','You have been assigned a new task: {task_title}. Due date: {due_date}','["task_title", "due_date"]',true,1,'2025-09-07 11:21:52.089736+05:30',13,NULL),
(2,'Approval Required','APPROVAL_REQUIRED','IN_APP','Approval Required: {approval_type}','Approval required for {approval_type}: {entity_name}','["approval_type", "entity_name"]',true,1,'2025-09-07 11:21:52.089736+05:30',13,NULL);

-- template_projects
INSERT INTO public.template_projects (id,name,description,project_type,region,size_band_min,size_band_max,config,created_at,created_by) VALUES
(1,'Solar Farm Template - California','Standard template for solar farm development in California','SOLAR','California',100,500,'{"required_milestones": ["feasibility", "permits", "construction"], "estimated_duration_days": 365, "required_approvals": ["environmental", "zoning", "utility"]}','2025-09-07 11:21:52.089736+05:30',13),
(2,'Wind Farm Template - Texas','Standard template for wind farm development in Texas','WIND','Texas',200,1000,'{"required_milestones": ["feasibility", "permits", "construction"], "estimated_duration_days": 450, "required_approvals": ["environmental", "aviation", "utility"]}','2025-09-07 11:21:52.089736+05:30',13);

-- proposal_parcels
INSERT INTO public.proposal_parcels (id,proposal_id,land_parcel_id,allocated_capacity_mw,allocated_investment,notes,created_at) VALUES
(1,1,1,150,225000000,'Primary solar site with excellent conditions','2025-09-07 11:21:52.089736+05:30'),
(2,1,3,350,525000000,'Hybrid solar + storage site','2025-09-07 11:21:52.089736+05:30'),
(3,2,2,200,300000000,'Wind energy development site','2025-09-07 11:21:52.089736+05:30');
"""

DML_SEQUENCES_SETVAL = """
SELECT pg_catalog.setval('public.users_id_seq', 16, true);
SELECT pg_catalog.setval('public.roles_id_seq', 1, false);
SELECT pg_catalog.setval('public.permissions_id_seq', 1, false);
SELECT pg_catalog.setval('public.user_roles_id_seq', 1, false);
SELECT pg_catalog.setval('public.role_permissions_id_seq', 1, false);
SELECT pg_catalog.setval('public.land_parcels_id_seq', 3, true);
SELECT pg_catalog.setval('public.investment_opportunities_id_seq', 2, true);
SELECT pg_catalog.setval('public.investment_proposals_id_seq', 2, true);
SELECT pg_catalog.setval('public.development_projects_id_seq', 2, true);
SELECT pg_catalog.setval('public.milestones_id_seq', 3, true);
SELECT pg_catalog.setval('public.tasks_id_seq', 3, true);
SELECT pg_catalog.setval('public.documents_id_seq', 3, true);
SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);
SELECT pg_catalog.setval('public.notification_templates_id_seq', 2, true);
SELECT pg_catalog.setval('public.template_projects_id_seq', 2, true);
SELECT pg_catalog.setval('public.template_milestones_id_seq', 1, false);
SELECT pg_catalog.setval('public.template_tasks_id_seq', 1, false);
SELECT pg_catalog.setval('public.approval_rules_id_seq', 1, false);
SELECT pg_catalog.setval('public.approvals_id_seq', 3, true);
SELECT pg_catalog.setval('public.proposal_parcels_id_seq', 3, true);
"""

def main():
    conn = psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "srenew_mart"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "sai")
    )
    try:
        with conn:
            with conn.cursor() as cur:
                # Speed up DDL; ensure fresh start
                cur.execute("SET client_min_messages = WARNING;")
                cur.execute(DDL_DROP_CREATE_SCHEMA)
                cur.execute(DDL_ENUMS)
                cur.execute(DDL_TABLES)
                cur.execute(DDL_SEQUENCES_DEFAULTS)
                cur.execute(DDL_CONSTRAINTS_INDEXES)
                cur.execute(DDL_FOREIGN_KEYS)
                cur.execute(DML_INSERTS)
                cur.execute(DML_SEQUENCES_SETVAL)
        print("Migration completed successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
>>>>>>> 50eb228c0c6aa14c1361d7a1680c9c2dd3a74e61
    main()