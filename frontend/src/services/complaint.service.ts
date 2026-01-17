import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api/v1';

export class ComplaintService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async listComplaints(filters?: {
    status?: string;
    severity?: string;
    limit?: number;
    offset?: number;
  }) {
    const response = await this.client.get('/complaints', { params: filters });
    return response.data;
  }

  async getComplaint(id: string) {
    const response = await this.client.get(`/complaints/${id}`);
    return response.data;
  }

  async createComplaint(data: {
    customerId: string;
    subject: string;
    description: string;
    severity: string;
  }) {
    const response = await this.client.post('/complaints', data);
    return response.data;
  }

  async updateComplaint(
    id: string,
    data: {
      status?: string;
      resolution?: string;
    }
  ) {
    const response = await this.client.put(`/complaints/${id}`, data);
    return response.data;
  }
}

export const complaintService = new ComplaintService();
