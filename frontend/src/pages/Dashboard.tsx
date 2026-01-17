import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ComplaintCard } from '@/components/complaint/ComplaintCard';
import { SummaryPanel } from '@/components/summary/SummaryPanel';
import { ResolutionPanel } from '@/components/resolution/ResolutionPanel';
import { complaintService } from '@/services/complaint.service';
import { Loader2 } from 'lucide-react';

interface Complaint {
  id: string;
  customerId: string;
  subject: string;
  description: string;
  status: 'open' | 'in-progress' | 'resolved' | 'escalated';
  createdAt: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export const Dashboard: React.FC = () => {
  const [selectedComplaintId, setSelectedComplaintId] = useState<string | null>(null);

  // Fetch complaints
  const { data: complaints = [], isLoading, error } = useQuery({
    queryKey: ['complaints'],
    queryFn: () => complaintService.listComplaints(),
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  const selectedComplaint = complaints.find((c) => c.id === selectedComplaintId);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Header */}
      <header className="border-b border-slate-700 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-white">SmartResolve Dashboard</h1>
          <p className="text-slate-400 mt-1">AI-Powered Complaint Intelligence Platform</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Complaints List */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800 rounded-lg border border-slate-700 shadow-lg">
              <div className="p-4 border-b border-slate-700">
                <h2 className="text-xl font-semibold text-white">Complaints</h2>
                <p className="text-slate-400 text-sm mt-1">{complaints.length} active</p>
              </div>

              {isLoading ? (
                <div className="flex items-center justify-center p-8">
                  <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
                </div>
              ) : error ? (
                <div className="p-6 text-center">
                  <p className="text-red-400">Failed to load complaints</p>
                </div>
              ) : complaints.length === 0 ? (
                <div className="p-6 text-center">
                  <p className="text-slate-400">No complaints found</p>
                </div>
              ) : (
                <div className="divide-y divide-slate-700 max-h-96 overflow-y-auto">
                  {complaints.map((complaint) => (
                    <ComplaintCard
                      key={complaint.id}
                      complaint={complaint}
                      isSelected={selectedComplaintId === complaint.id}
                      onSelect={() => setSelectedComplaintId(complaint.id)}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Details Panels */}
          <div className="lg:col-span-2 space-y-6">
            {selectedComplaint ? (
              <>
                {/* Summary Panel */}
                <SummaryPanel complaintId={selectedComplaint.id} />

                {/* Resolution Panel */}
                <ResolutionPanel complaintId={selectedComplaint.id} />
              </>
            ) : (
              <div className="bg-slate-800 rounded-lg border border-slate-700 p-8 text-center">
                <p className="text-slate-400">Select a complaint to view details</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
