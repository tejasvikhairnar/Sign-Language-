'use client';
import { Settings, User, Bell, Shield, Moon, Volume2, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-3xl mx-auto py-12 px-6">
        <div className="flex items-center gap-4 mb-8">
          <Link href="/dashboard" className="p-2 hover:bg-white rounded-full transition-colors">
            <ArrowLeft className="h-6 w-6 text-slate-600" />
          </Link>
          <h1 className="text-2xl font-bold text-slate-900">Settings</h1>
        </div>

        <div className="space-y-6">
          <Section title="General">
             <ToggleItem icon={<Moon />} label="Dark Mode" description="Use darker colors for low-light environments" />
             <ToggleItem icon={<Volume2 />} label="Voice Output" description="Read out detected signs automatically" checked />
          </Section>

          <Section title="Detection">
             <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                   <div className="p-2 bg-blue-50 rounded-lg text-blue-600">
                      <Settings className="h-5 w-5" />
                   </div>
                   <div>
                      <p className="font-medium text-slate-900">Sensitivity</p>
                      <p className="text-sm text-slate-500">Adjust detection threshold</p>
                   </div>
                </div>
                <div className="w-32">
                   <input type="range" className="w-full accent-blue-600" />
                </div>
             </div>
          </Section>

          <Section title="Account">
             <ButtonItem icon={<User />} label="Profile Settings" />
             <ButtonItem icon={<Bell />} label="Notifications" />
             <ButtonItem icon={<Shield />} label="Privacy & Security" />
          </Section>
        </div>
      </div>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-50 bg-gray-50/50">
        <h2 className="font-semibold text-slate-900">{title}</h2>
      </div>
      <div className="p-2">
        {children}
      </div>
    </div>
  )
}

function ToggleItem({ icon, label, description, checked }) {
  return (
    <div className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-xl transition-colors">
       <div className="flex items-center gap-3">
          <div className="p-2 bg-gray-100 rounded-lg text-slate-600">
             {icon}
          </div>
          <div>
             <p className="font-medium text-slate-900">{label}</p>
             {description && <p className="text-sm text-slate-500">{description}</p>}
          </div>
       </div>
       <div className={`w-12 h-6 rounded-full relative transition-colors ${checked ? 'bg-blue-600' : 'bg-gray-200'}`}>
          <div className={`absolute top-1 bottom-1 w-4 bg-white rounded-full shadow-sm transition-all ${checked ? 'left-7' : 'left-1'}`} />
       </div>
    </div>
  )
}

function ButtonItem({ icon, label }) {
  return (
    <button className="w-full flex items-center justify-between p-4 hover:bg-gray-50 rounded-xl transition-colors text-left">
       <div className="flex items-center gap-3">
          <div className="p-2 bg-gray-100 rounded-lg text-slate-600">
             {icon}
          </div>
          <p className="font-medium text-slate-900">{label}</p>
       </div>
       <ArrowLeft className="h-4 w-4 text-gray-400 rotate-180" />
    </button>
  )
}
