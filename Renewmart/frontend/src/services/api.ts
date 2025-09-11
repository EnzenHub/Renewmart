import {
  AuthResponse,
  RefreshResponse,
  User,
  UserCreate,
  UserLogin,
  LandParcel,
  LandParcelCreate,
  Task,
  InvestmentOpportunity,
  InvestmentProposal,
  DevelopmentProject,
  Document,
  Approval,
  Notification,
  DashboardStats
} from '../types';

const API_BASE_URL = 'http://localhost:8001/api/v1';

class ApiService {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('access_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const config: RequestInit = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        if (response.status === 401) {
          // Token expired, try to refresh
          const refreshed = await this.refreshToken();
          if (refreshed) {
            // Retry the original request with new token
            (headers as Record<string, string>)['Authorization'] = `Bearer ${this.token}`;
            const retryResponse = await fetch(url, { ...config, headers });
            if (!retryResponse.ok) {
              throw new Error(`HTTP error! status: ${retryResponse.status}`);
            }
            return await retryResponse.json();
          } else {
            // Refresh failed, redirect to login
            this.logout();
            throw new Error('Authentication failed');
          }
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication Methods
  async login(credentials: UserLogin): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data: AuthResponse = await response.json();
    this.setToken(data.access_token);
    return data;
  }

  async register(userData: UserCreate): Promise<User> {
    const response = await this.request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    return response;
  }

  async refreshToken(): Promise<boolean> {
    try {
      const response = await this.request<RefreshResponse>('/auth/refresh', {
        method: 'POST',
      });
      this.setToken(response.access_token);
      return true;
    } catch (error) {
      console.error('Token refresh failed:', error);
      return false;
    }
  }

  async logout(): Promise<void> {
    try {
      await this.request('/auth/logout', {
        method: 'POST',
      });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      this.clearToken();
    }
  }

  // Token Management
  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('access_token', token);
  }

  clearToken(): void {
    this.token = null;
    localStorage.removeItem('access_token');
  }

  getToken(): string | null {
    return this.token;
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }

  // User Methods
  async getUsers(skip: number = 0, limit: number = 100, userType?: string): Promise<User[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (userType) {
      params.append('user_type', userType);
    }

    return this.request<User[]>(`/users/?${params}`);
  }

  async getUser(userId: number): Promise<User> {
    return this.request<User>(`/users/${userId}`);
  }

  async createUser(userData: UserCreate): Promise<User> {
    return this.request<User>('/users/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUser(userId: number, userData: Partial<User>): Promise<User> {
    return this.request<User>(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async deleteUser(userId: number): Promise<void> {
    return this.request<void>(`/users/${userId}`, {
      method: 'DELETE',
    });
  }

  // Land Parcel Methods
  async getLandParcels(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    landownerId?: number
  ): Promise<LandParcel[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (status) {
      params.append('status', status);
    }

    if (landownerId) {
      params.append('landowner_id', landownerId.toString());
    }

    return this.request<LandParcel[]>(`/land-parcels/?${params}`);
  }

  async getLandParcel(parcelId: number): Promise<LandParcel> {
    return this.request<LandParcel>(`/land-parcels/${parcelId}`);
  }

  async createLandParcel(parcelData: LandParcelCreate): Promise<LandParcel> {
    return this.request<LandParcel>('/land-parcels/', {
      method: 'POST',
      body: JSON.stringify(parcelData),
    });
  }

  async updateLandParcel(parcelId: number, parcelData: Partial<LandParcel>): Promise<LandParcel> {
    return this.request<LandParcel>(`/land-parcels/${parcelId}`, {
      method: 'PUT',
      body: JSON.stringify(parcelData),
    });
  }

  async deleteLandParcel(parcelId: number): Promise<void> {
    return this.request<void>(`/land-parcels/${parcelId}`, {
      method: 'DELETE',
    });
  }

  async assignFeasibilityStudy(parcelId: number, analystId: number, dueDate?: string): Promise<void> {
    return this.request<void>(`/land-parcels/${parcelId}/feasibility`, {
      method: 'POST',
      body: JSON.stringify({
        analyst_id: analystId,
        due_date: dueDate,
      }),
    });
  }

  async updateParcelStatus(parcelId: number, newStatus: string, comments?: string): Promise<void> {
    return this.request<void>(`/land-parcels/${parcelId}/state/transitions`, {
      method: 'POST',
      body: JSON.stringify({
        new_status: newStatus,
        comments,
      }),
    });
  }

  // Task Methods
  async getTasks(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    assigneeId?: number
  ): Promise<Task[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (status) {
      params.append('status', status);
    }

    if (assigneeId) {
      params.append('assignee_id', assigneeId.toString());
    }

    return this.request<Task[]>(`/tasks/?${params}`);
  }

  async getTask(taskId: number): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}`);
  }

  async createTask(taskData: Partial<Task>): Promise<Task> {
    return this.request<Task>('/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(taskId: number, taskData: Partial<Task>): Promise<Task> {
    return this.request<Task>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId: number): Promise<void> {
    return this.request<void>(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async assignTask(taskId: number, assigneeId: number): Promise<void> {
    return this.request<void>(`/tasks/${taskId}/assign`, {
      method: 'PATCH',
      body: JSON.stringify({ assignee_id: assigneeId }),
    });
  }

  async acceptTask(taskId: number): Promise<void> {
    return this.request<void>(`/tasks/${taskId}/accept`, {
      method: 'PATCH',
    });
  }

  async completeTask(taskId: number, completionNotes?: string): Promise<void> {
    return this.request<void>(`/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completion_notes: completionNotes }),
    });
  }

  async rejectTask(taskId: number, rejectionReason?: string): Promise<void> {
    return this.request<void>(`/tasks/${taskId}/reject`, {
      method: 'PATCH',
      body: JSON.stringify({ rejection_reason: rejectionReason }),
    });
  }

  async getUserTasks(userId: number): Promise<Task[]> {
    return this.request<Task[]>(`/tasks/assignee/${userId}`);
  }

  // Investment Opportunity Methods
  async getOpportunities(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    investorId?: number,
    advisorId?: number,
    region?: string
  ): Promise<InvestmentOpportunity[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (status) params.append('status', status);
    if (investorId) params.append('investor_id', investorId.toString());
    if (advisorId) params.append('advisor_id', advisorId.toString());
    if (region) params.append('region', region);

    return this.request<InvestmentOpportunity[]>(`/opportunities/?${params}`);
  }

  async getOpportunity(opportunityId: number): Promise<InvestmentOpportunity> {
    return this.request<InvestmentOpportunity>(`/opportunities/${opportunityId}`);
  }

  async createOpportunity(opportunityData: Partial<InvestmentOpportunity>): Promise<InvestmentOpportunity> {
    return this.request<InvestmentOpportunity>('/opportunities/', {
      method: 'POST',
      body: JSON.stringify(opportunityData),
    });
  }

  async updateOpportunity(opportunityId: number, opportunityData: Partial<InvestmentOpportunity>): Promise<InvestmentOpportunity> {
    return this.request<InvestmentOpportunity>(`/opportunities/${opportunityId}`, {
      method: 'PUT',
      body: JSON.stringify(opportunityData),
    });
  }

  async deleteOpportunity(opportunityId: number): Promise<void> {
    return this.request<void>(`/opportunities/${opportunityId}`, {
      method: 'DELETE',
    });
  }

  async updateOpportunityStatus(opportunityId: number, newStatus: string, comments?: string): Promise<void> {
    return this.request<void>(`/opportunities/${opportunityId}/state`, {
      method: 'PATCH',
      body: JSON.stringify({
        new_status: newStatus,
        comments,
      }),
    });
  }

  // Investment Proposal Methods
  async getProposals(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    opportunityId?: number,
    advisorId?: number
  ): Promise<InvestmentProposal[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (status) params.append('status', status);
    if (opportunityId) params.append('opportunity_id', opportunityId.toString());
    if (advisorId) params.append('advisor_id', advisorId.toString());

    return this.request<InvestmentProposal[]>(`/proposals/?${params}`);
  }

  async getProposal(proposalId: number): Promise<InvestmentProposal> {
    return this.request<InvestmentProposal>(`/proposals/${proposalId}`);
  }

  async createProposal(opportunityId: number, proposalData: Partial<InvestmentProposal>): Promise<InvestmentProposal> {
    return this.request<InvestmentProposal>(`/opportunities/${opportunityId}/proposals`, {
      method: 'POST',
      body: JSON.stringify(proposalData),
    });
  }

  async updateProposal(proposalId: number, proposalData: Partial<InvestmentProposal>): Promise<InvestmentProposal> {
    return this.request<InvestmentProposal>(`/proposals/${proposalId}`, {
      method: 'PUT',
      body: JSON.stringify(proposalData),
    });
  }

  async deleteProposal(proposalId: number): Promise<void> {
    return this.request<void>(`/proposals/${proposalId}`, {
      method: 'DELETE',
    });
  }

  async approveProposal(proposalId: number, comments?: string): Promise<void> {
    return this.request<void>(`/proposals/${proposalId}/approve`, {
      method: 'POST',
      body: JSON.stringify({ comments }),
    });
  }

  async rejectProposal(proposalId: number, rejectionReason?: string): Promise<void> {
    return this.request<void>(`/proposals/${proposalId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ rejection_reason: rejectionReason }),
    });
  }

  // Development Project Methods
  async getProjects(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    projectType?: string,
    projectManagerId?: number
  ): Promise<DevelopmentProject[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (status) params.append('status', status);
    if (projectType) params.append('project_type', projectType);
    if (projectManagerId) params.append('project_manager_id', projectManagerId.toString());

    return this.request<DevelopmentProject[]>(`/projects/?${params}`);
  }

  async getProject(projectId: number): Promise<DevelopmentProject> {
    return this.request<DevelopmentProject>(`/projects/${projectId}`);
  }

  async createProject(proposalId: number, projectData: Partial<DevelopmentProject>): Promise<DevelopmentProject> {
    return this.request<DevelopmentProject>(`/proposals/${proposalId}/projects`, {
      method: 'POST',
      body: JSON.stringify(projectData),
    });
  }

  async updateProject(projectId: number, projectData: Partial<DevelopmentProject>): Promise<DevelopmentProject> {
    return this.request<DevelopmentProject>(`/projects/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify(projectData),
    });
  }

  async deleteProject(projectId: number): Promise<void> {
    return this.request<void>(`/projects/${projectId}`, {
      method: 'DELETE',
    });
  }

  async updateProjectStatus(projectId: number, newStatus: string, comments?: string): Promise<void> {
    return this.request<void>(`/projects/${projectId}/status`, {
      method: 'PATCH',
      body: JSON.stringify({
        new_status: newStatus,
        comments,
      }),
    });
  }

  // Document Methods
  async getDocuments(
    skip: number = 0,
    limit: number = 100,
    documentType?: string,
    landParcelId?: number,
    taskId?: number,
    projectId?: number,
    proposalId?: number
  ): Promise<Document[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (documentType) params.append('document_type', documentType);
    if (landParcelId) params.append('land_parcel_id', landParcelId.toString());
    if (taskId) params.append('task_id', taskId.toString());
    if (projectId) params.append('project_id', projectId.toString());
    if (proposalId) params.append('proposal_id', proposalId.toString());

    return this.request<Document[]>(`/documents/?${params}`);
  }

  async getDocument(documentId: number): Promise<Document> {
    return this.request<Document>(`/documents/${documentId}`);
  }

  async uploadDocument(
    file: File,
    documentType: string,
    landParcelId?: number,
    taskId?: number,
    projectId?: number,
    proposalId?: number
  ): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);

    if (landParcelId) formData.append('land_parcel_id', landParcelId.toString());
    if (taskId) formData.append('task_id', taskId.toString());
    if (projectId) formData.append('project_id', projectId.toString());
    if (proposalId) formData.append('proposal_id', proposalId.toString());

    const url = `${this.baseURL}/documents/upload`;
    const headers: HeadersInit = {};

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result.document;
  }

  async downloadDocument(documentId: number): Promise<Blob> {
    const response = await fetch(`${this.baseURL}/documents/${documentId}/download`, {
      headers: this.token ? { 'Authorization': `Bearer ${this.token}` } : {},
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.blob();
  }

  async deleteDocument(documentId: number): Promise<void> {
    return this.request<void>(`/documents/${documentId}`, {
      method: 'DELETE',
    });
  }

  // Approval Methods
  async getApprovals(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    approvalType?: string
  ): Promise<Approval[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (status) params.append('status', status);
    if (approvalType) params.append('approval_type', approvalType);

    return this.request<Approval[]>(`/approvals/?${params}`);
  }

  async getPendingApprovals(): Promise<Approval[]> {
    return this.request<Approval[]>('/approvals/pending');
  }

  async getApproval(approvalId: number): Promise<Approval> {
    return this.request<Approval>(`/approvals/${approvalId}`);
  }

  async createApproval(approvalData: Partial<Approval>): Promise<Approval> {
    return this.request<Approval>('/approvals/', {
      method: 'POST',
      body: JSON.stringify(approvalData),
    });
  }

  async updateApproval(approvalId: number, approvalData: Partial<Approval>): Promise<Approval> {
    return this.request<Approval>(`/approvals/${approvalId}`, {
      method: 'PUT',
      body: JSON.stringify(approvalData),
    });
  }

  async deleteApproval(approvalId: number): Promise<void> {
    return this.request<void>(`/approvals/${approvalId}`, {
      method: 'DELETE',
    });
  }

  async makeApprovalDecision(approvalId: number, decision: string, comments?: string): Promise<void> {
    return this.request<void>(`/approvals/${approvalId}/decision`, {
      method: 'POST',
      body: JSON.stringify({
        decision,
        comments,
      }),
    });
  }

  async cancelApproval(approvalId: number, reason?: string): Promise<void> {
    return this.request<void>(`/approvals/${approvalId}/cancel`, {
      method: 'PATCH',
      body: JSON.stringify({ reason }),
    });
  }

  // Notification Methods
  async getNotifications(
    skip: number = 0,
    limit: number = 100,
    status?: string,
    notificationType?: string,
    channel?: string
  ): Promise<Notification[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    if (status) params.append('status', status);
    if (notificationType) params.append('notification_type', notificationType);
    if (channel) params.append('channel', channel);

    return this.request<Notification[]>(`/notifications/?${params}`);
  }

  async getUnreadNotifications(): Promise<Notification[]> {
    return this.request<Notification[]>('/notifications/unread');
  }

  async getNotification(notificationId: number): Promise<Notification> {
    return this.request<Notification>(`/notifications/${notificationId}`);
  }

  async markNotificationAsRead(notificationId: number): Promise<void> {
    return this.request<void>(`/notifications/${notificationId}/read`, {
      method: 'PATCH',
    });
  }

  async markNotificationAsUnread(notificationId: number): Promise<void> {
    return this.request<void>(`/notifications/${notificationId}/unread`, {
      method: 'PATCH',
    });
  }

  async markAllNotificationsAsRead(): Promise<void> {
    return this.request<void>('/notifications/read-all', {
      method: 'PATCH',
    });
  }

  async deleteNotification(notificationId: number): Promise<void> {
    return this.request<void>(`/notifications/${notificationId}`, {
      method: 'DELETE',
    });
  }

  async deleteAllNotifications(): Promise<void> {
    return this.request<void>('/notifications/', {
      method: 'DELETE',
    });
  }

  // Dashboard Methods
  async getDashboardStats(): Promise<DashboardStats> {
    // Since we don't have a specific dashboard endpoint, we'll aggregate data
    const [users, parcels, tasks, projects, opportunities, proposals] = await Promise.all([
      this.getUsers(0, 1),
      this.getLandParcels(0, 1),
      this.getTasks(0, 1),
      this.getProjects(0, 1),
      this.getOpportunities(0, 1),
      this.getProposals(0, 1),
    ]);

    // Get more detailed counts
    const [allUsers, allParcels, allTasks, allProjects, allOpportunities, allProposals] = await Promise.all([
      this.getUsers(0, 1000),
      this.getLandParcels(0, 1000),
      this.getTasks(0, 1000),
      this.getProjects(0, 1000),
      this.getOpportunities(0, 1000),
      this.getProposals(0, 1000),
    ]);

    return {
      totalUsers: allUsers.length,
      totalParcels: allParcels.length,
      activeParcels: allParcels.filter(p => p.status === 'feasibility_in_progress' || p.status === 'in_development').length,
      pendingTasks: allTasks.filter(t => t.status === 'pending' || t.status === 'assigned').length,
      totalProjects: allProjects.length,
      activeProjects: allProjects.filter(p => p.status === 'in_progress' || p.status === 'stage_gate').length,
      totalOpportunities: allOpportunities.length,
      totalProposals: allProposals.length,
    };
  }

  // Health Check
  async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    return this.request<{ status: string; service: string; version: string }>('/health');
  }
}

// Create and export a singleton instance
export const apiService = new ApiService();
export default apiService;
