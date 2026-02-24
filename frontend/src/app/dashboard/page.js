'use client';
import { useState, useEffect, useRef } from 'react';
import { Camera, Mic, Volume2, History, Settings, MoreVertical, X, Play, Pause, RefreshCw, Power } from 'lucide-react';
import Link from 'next/link';

export default function Dashboard() {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState("Waiting for input...");
  const [detectedSign, setDetectedSign] = useState("-");
  const [confidence, setConfidence] = useState(0);
  const [timer, setTimer] = useState(0);
  
  // Polling for status updates
  useEffect(() => {
    let interval;
    if (isRecording) {
      interval = setInterval(async () => {
        try {
          const res = await fetch('/api/status');
          const data = await res.json();
          setDetectedSign(data.char);
          setTranscription(data.sentence);
          setTimer(data.timer);
          // Assuming backend might send confidence later, for now we mock or hide it if not available
        } catch (err) {
          console.error("Failed to fetch status:", err);
        }
      }, 500);
    }
    return () => clearInterval(interval);
  }, [isRecording]);

  const handleClear = async () => {
    try {
      await fetch('/api/clear');
      setTranscription("-");
    } catch (err) {
      console.error("Error clearing text:", err);
    }
  };

  const handleSpeak = async () => {
    try {
      await fetch('/api/speak');
    } catch (err) {
      console.error("Error invoking TTS:", err);
    }
  }

  const handleSpace = async () => {
    try {
      await fetch('/api/add_space');
    } catch (err) {
      console.error("Error adding space:", err);
    }
  };

  const handleBackspace = async () => {
    try {
      await fetch('/api/backspace');
    } catch (err) {
      console.error("Error invoking backspace:", err);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar - Fixed */}
      <aside className="w-20 bg-slate-900 flex flex-col items-center py-8 gap-8 z-20 fixed h-full left-0 top-0">
        <div className="p-2 bg-blue-600 rounded-xl">
          <Camera className="h-6 w-6 text-white" />
        </div>
        <nav className="flex-1 flex flex-col gap-6 w-full items-center">
          <NavItem href="/dashboard" icon={<Play />} active />
          <NavItem href="/history" icon={<History />} />
          <NavItem href="/settings" icon={<Settings />} />
        </nav>
      </aside>

      {/* Main Content - Scrollable */}
      <main className="flex-1 flex flex-col relative ml-20">
        {/* Header */}
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
          <h1 className="text-xl font-bold text-slate-800">Live Detection</h1>
          <div className="flex items-center gap-4">
             <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${isRecording ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
               <div className={`h-2 w-2 rounded-full ${isRecording ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
               {isRecording ? 'Camera Active' : 'Camera Off'}
             </div>
          </div>
        </header>

        {/* Dashboard Grid */}
        <div className="flex-1 p-6 grid grid-cols-12 gap-6">
          
          {/* Camear Feed Area */}
          <div className="col-span-12 lg:col-span-8 flex flex-col gap-4">
            <div className="flex-1 bg-black rounded-3xl overflow-hidden relative shadow-lg group">
              {isRecording ? (
                <div className="w-full h-full relative" >
                   {/* Live Video Feed */}
                   <img src="/api/video_feed" alt="Live Feed" className="w-full h-full object-cover" />
                   
                   {/* Overlay UI */}
                   <div className="absolute top-4 right-4 bg-black/50 backdrop-blur-md px-3 py-1 rounded-lg text-white text-xs font-mono">
                      LIVE
                   </div>
                   
                   {/* Timer Overlay */}
                   {timer > 0 && (
                      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                         <div className="h-20 w-20 rounded-full bg-black/60 backdrop-blur-md flex items-center justify-center border-4 border-blue-500">
                            <span className="text-4xl font-bold text-white">{timer}</span>
                         </div>
                      </div>
                   )}
                </div>
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center text-gray-500 gap-4">
                   <div className="h-20 w-20 rounded-full bg-slate-800 flex items-center justify-center mb-4">
                      <Camera className="h-10 w-10 text-slate-500" />
                   </div>
                   <p className="text-lg">Camera is turned off</p>
                   <button onClick={() => setIsRecording(true)} className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-full font-medium transition-colors">
                     Start Camera
                   </button>
                </div>
              )}
            </div>

            {/* Controls */}
            <div className="h-24 bg-white rounded-2xl border border-gray-200 shadow-sm flex items-center justify-between px-8">
               <div className="flex items-center gap-6">
                  <div className="flex flex-col gap-1">
                     <span className="text-xs text-gray-500 font-medium uppercase tracking-wider">Camera Control</span>
                     <button 
                        onClick={() => setIsRecording(!isRecording)} 
                        className={`h-12 px-6 rounded-xl flex items-center gap-2 font-medium transition-all ${isRecording ? 'bg-red-50 text-red-600 border border-red-100 hover:bg-red-100' : 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-200'}`}
                     >
                       <Power className="h-5 w-5" />
                       {isRecording ? "Turn Off" : "Turn On"}
                     </button>
                  </div>

                  <div className="h-10 w-px bg-gray-200 mx-2"></div>

                  <div className="flex flex-col gap-1">
                     <span className="text-xs text-gray-500 font-medium uppercase tracking-wider">Actions</span>
                     <div className="flex items-center gap-2">
                        <button onClick={handleSpace} className="h-12 px-4 rounded-xl bg-gray-50 text-slate-600 border border-gray-200 flex items-center justify-center hover:bg-gray-100 transition-colors font-medium text-sm" title="Add Space">
                          Space
                        </button>
                        <button onClick={handleBackspace} className="h-12 w-12 rounded-xl bg-gray-50 text-slate-600 border border-gray-200 flex items-center justify-center hover:bg-gray-100 transition-colors" title="Backspace">
                          <X className="h-5 w-5" />
                        </button>
                        <button onClick={handleClear} className="h-12 w-12 rounded-xl bg-red-50 text-red-600 border border-red-100 flex items-center justify-center hover:bg-red-100 transition-colors" title="Clear Transcript">
                          <RefreshCw className="h-5 w-5" />
                        </button>
                     </div>
                  </div>
               </div>
               
               <div className="flex items-center gap-4">
                  <button onClick={handleSpeak} className="flex items-center gap-2 px-6 py-3 bg-indigo-600 text-white rounded-xl font-medium hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200">
                     <Volume2 className="h-5 w-5" /> Speak Text
                  </button>
               </div>
            </div>
          </div>

          {/* Sidebar Stats - Now with Transcript */}
          <div className="col-span-12 lg:col-span-4 flex flex-col gap-6">
            <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-sm flex-1 flex flex-col overflow-hidden">
              <h3 className="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-blue-500"></div>
                Live Analysis
              </h3>
              
              <div className="flex-1 flex flex-col gap-6 overflow-y-auto pr-2">
                {/* Current Detection Card */}
                <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-6 text-white shadow-lg shadow-blue-200">
                   <p className="text-blue-100 text-sm font-medium mb-2">Detected Symbol</p>
                   <div className="flex items-end justify-between">
                     <div className="text-6xl font-bold tracking-tight">{isRecording ? detectedSign : "-"}</div>
                     <div className="text-blue-200 text-sm">Confidence: High</div>
                   </div>
                </div>

                {/* Transcript Section */}
                <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100 flex-1 flex flex-col">
                   <div className="flex items-center justify-between mb-4">
                     <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Transcript</p>
                     <span className="text-xs px-2 py-1 bg-white rounded-md border border-gray-100 text-gray-400">Auto-generated</span>
                   </div>
                   <div className="flex-1 bg-white rounded-xl border border-gray-200 p-4 font-mono text-lg text-slate-800 shadow-inner">
                      {transcription || <span className="text-gray-300 italic">Waiting for signs...</span>}
                   </div>
                </div>

                {/* Instructions */}
                <div className="bg-amber-50 rounded-xl p-4 border border-amber-100">
                   <h4 className="text-amber-800 text-sm font-bold mb-2">Quick Tips</h4>
                   <ul className="text-amber-700 text-xs space-y-1.5 list-disc pl-4 leading-relaxed">
                      <li>Hold hand steady for <b>3 seconds</b> to capture.</li>
                      <li>Ensure good lighting on your hands.</li>
                      <li>Use "Clear" to reset the transcript.</li>
                   </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function NavItem({ href, icon, active }) {
  return (
    <Link 
      href={href} 
      className={`h-12 w-12 rounded-xl flex items-center justify-center transition-all duration-200 ${active ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'text-slate-400 hover:bg-slate-800 hover:text-white'}`}
    >
      {icon}
    </Link>
  )
}
