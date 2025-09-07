// User Types
export interface User {
  id: number;
  name: string;
  email: string;
  user_type: UserType;
  phone?: string;
  company?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export enum UserType {
  ADMIN = 'admin',
  GOVERNANCE = 'governance',
  PROJECT_MANAGER = 'project_manager',
  ADVISOR = 'advisor',
  ANALYST = 'analyst',
  INVESTOR = 'investor',
  LANDOWNER = 'landowner'
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
  user_type: UserType;
  phone?: string;
  company?: string;
  is_active?: boolean;
}

export interface UserLogin {
  username: string;
  password: string;
}

// Authentication Types
export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RefreshResponse {
  access_token: string;
  token_type: string;
}

// Land Parcel Types
export interface LandParcel {
  id: number;
  name: string;
  address: string;
  size_acres: number;
  coordinates: {
    lat: number;
    lng: number;
  };
  description?: string;
  status: ParcelStatus;
  landowner_id: number;
  feasibility_completed: boolean;
  feasibility_score?: number;
  created_at: string;
  updated_at?: string;
}

export enum ParcelStatus {
  REGISTERED = 'registered',
  FEASIBILITY_ASSIGNED = 'feasibility_assigned',
  FEASIBILITY_IN_PROGRESS = 'feasibility_in_progress',
  FEASIBILITY_COMPLETED = 'feasibility_completed',
  FEASIBILITY_APPROVED = 'feasibility_approved',
  FEASIBILITY_REJECTED = 'feasibility_rejected',
  READY_FOR_PROPOSAL = 'ready_for_proposal',
  IN_PROPOSAL = 'in_proposal',
  PROPOSAL_APPROVED = 'proposal_approved',
  PROPOSAL_REJECTED = 'proposal_rejected',
  IN_DEVELOPMENT = 'in_development',
  READY_TO_BUILD = 'ready_to_build'
}

export interface LandParcelCreate {
  name: string;
  address: string;
  size_acres: number;
  coordinates: {
    lat: number;
    lng: number;
  };
  description?: string;
  landowner_id: number;
}

// Task Types
export interface Task {
  id: number;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  assigned_to?: number;
  due_date?: string;
  completed_at?: string;
  land_parcel_id?: number;
  project_id?: number;
  created_by: number;
  created_at: string;
}

export enum TaskStatus {
  PENDING = 'pending',
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  REJECTED = 'rejected',
  CANCELLED = 'cancelled'
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

// Investment Types
export interface InvestmentOpportunity {
  id: number;
  title: string;
  description: string;
  target_capacity_mw: number;
  target_region: string;
  investment_amount: number;
  expected_roi: number;
  status: OpportunityStatus;
  investor_id: number;
  advisor_id: number;
  created_at: string;
  updated_at?: string;
}

export enum OpportunityStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  UNDER_REVIEW = 'under_review',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  ACTIVE = 'active',
  COMPLETED = 'completed'
}

export interface InvestmentProposal {
  id: number;
  title: string;
  description: string;
  total_investment: number;
  expected_roi: number;
  payback_period_years: number;
  status: ProposalStatus;
  opportunity_id: number;
  advisor_id: number;
  created_at: string;
  updated_at?: string;
}

export enum ProposalStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  UNDER_REVIEW = 'under_review',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  AGREEMENT_SIGNED = 'agreement_signed'
}

// Project Types
export interface DevelopmentProject {
  id: number;
  name: string;
  description: string;
  project_type: ProjectType;
  status: ProjectStatus;
  start_date: string;
  target_completion_date: string;
  actual_completion_date?: string;
  budget: number;
  proposal_id: number;
  project_manager_id: number;
  created_at: string;
  updated_at?: string;
}

export enum ProjectType {
  SOLAR = 'solar',
  WIND = 'wind',
  HYDRO = 'hydro',
  GEOTHERMAL = 'geothermal',
  BIOMASS = 'biomass',
  STORAGE = 'storage'
}

export enum ProjectStatus {
  INITIATED = 'initiated',
  IN_PROGRESS = 'in_progress',
  STAGE_GATE = 'stage_gate',
  READY_TO_BUILD = 'ready_to_build',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled'
}

// Document Types
export interface Document {
  id: number;
  name: string;
  file_path: string;
  file_size: number;
  mime_type: string;
  document_type: DocumentType;
  checksum: string;
  land_parcel_id?: number;
  task_id?: number;
  project_id?: number;
  proposal_id?: number;
  created_by: number;
  created_at: string;
}

export enum DocumentType {
  FEASIBILITY_REPORT = 'feasibility_report',
  ENVIRONMENTAL_IMPACT_ASSESSMENT = 'environmental_impact_assessment',
  TECHNICAL_DESIGN = 'technical_design',
  FINANCIAL_MODEL = 'financial_model',
  LEGAL_DOCUMENT = 'legal_document',
  PERMIT = 'permit',
  AGREEMENT = 'agreement',
  OTHER = 'other'
}

// Approval Types
export interface Approval {
  id: number;
  title: string;
  description: string;
  approval_type: ApprovalType;
  status: ApprovalStatus;
  land_parcel_id?: number;
  project_id?: number;
  proposal_id?: number;
  created_by: number;
  approved_by?: number;
  approved_at?: string;
  comments?: string;
  created_at: string;
}

export enum ApprovalType {
  FEASIBILITY = 'feasibility',
  PROPOSAL = 'proposal',
  MILESTONE = 'milestone',
  FINAL = 'final'
}

export enum ApprovalStatus {
  PENDING = 'pending',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  CANCELLED = 'cancelled'
}

// Notification Types
export interface Notification {
  id: number;
  title: string;
  message: string;
  notification_type: NotificationType;
  channel: NotificationChannel;
  status: NotificationStatus;
  user_id: number;
  data?: Record<string, any>;
  read_at?: string;
  created_at: string;
}

export enum NotificationType {
  TASK_ASSIGNMENT = 'task_assignment',
  APPROVAL_REQUEST = 'approval_request',
  MILESTONE_COMPLETION = 'milestone_completion',
  SYSTEM_ANNOUNCEMENT = 'system_announcement',
  DEADLINE_REMINDER = 'deadline_reminder'
}

export enum NotificationChannel {
  EMAIL = 'email',
  SMS = 'sms',
  WEB_PUSH = 'web_push',
  IN_APP = 'in_app'
}

export enum NotificationStatus {
  PENDING = 'pending',
  SENT = 'sent',
  DELIVERED = 'delivered',
  FAILED = 'failed'
}

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Form Types
export interface LoginForm {
  username: string;
  password: string;
}

export interface RegisterForm {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  user_type: UserType;
  phone?: string;
  company?: string;
}

// Dashboard Types
export interface DashboardStats {
  totalUsers: number;
  totalParcels: number;
  activeParcels: number;
  pendingTasks: number;
  totalProjects: number;
  activeProjects: number;
  totalOpportunities: number;
  totalProposals: number;
}
