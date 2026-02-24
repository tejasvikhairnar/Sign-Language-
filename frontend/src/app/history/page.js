'use client';
import { History, Search, Filter, Download, ArrowLeft, Trash2 } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';

export default function HistoryPage() {
  const [logs, setLogs] = useState([
    { id: 1, sign: "Hello", confidence: 98, timestamp: "2024-03-10 10:42:15", duration: "2s" },
    { id: 2, sign: "Welcome", confidence: 95, timestamp: "2024-03-10 10:42:20", duration: "1.5s" },
    { id: 3, sign: "Thanks", confidence: 92, timestamp: "2024-03-10 10:42:28", duration: "1s" },
    { id: 4, sign: "Doctor", confidence: 88, timestamp: "2024-03-10 10:43:05", duration: "3s" },
    { id: 5, sign: "Pain", confidence: 91, timestamp: "2024-03-10 10:43:12", duration: "2s" },
    { id: 6, sign: "Medicine", confidence: 85, timestamp: "2024-03-10 10:44:00", duration: "2.5s" },
  ]);

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-5xl mx-auto py-12 px-6">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="p-2 hover:bg-white rounded-full transition-colors">
              <ArrowLeft className="h-6 w-6 text-slate-600" />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-slate-900">Detection History</h1>
              <p className="text-slate-500">View and manage your past translation logs.</p>
            </div>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-slate-700 rounded-lg hover:bg-gray-50 transition-colors shadow-sm">
            <Download className="h-4 w-4" /> Export CSV
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm mb-6 flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
            <input 
              type="text" 
              placeholder="Search signs..." 
              className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
            />
          </div>
          <button className="px-4 py-2 flex items-center gap-2 text-slate-600 border border-gray-200 rounded-lg hover:bg-gray-50">
            <Filter className="h-4 w-4" /> Filter
          </button>
        </div>

        {/* Table */}
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Detected Sign</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Confidence</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Timestamp</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Duration</th>
                <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-blue-50/30 transition-colors group">
                  <td className="px-6 py-4">
                    <span className="font-medium text-slate-900">{log.sign}</span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                       <span className={`text-sm font-medium ${log.confidence > 90 ? 'text-green-600' : 'text-amber-600'}`}>
                         {log.confidence}%
                       </span>
                       <div className="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div className={`h-full rounded-full ${log.confidence > 90 ? 'bg-green-500' : 'bg-amber-500'}`} style={{ width: `${log.confidence}%` }}></div>
                       </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {log.timestamp}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {log.duration}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="p-2 text-gray-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
