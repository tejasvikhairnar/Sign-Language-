import Link from 'next/link';
import { Bot, Camera, Mic, Play, Settings, History, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <Bot className="h-8 w-8 text-blue-600" />
              <span className="font-bold text-xl text-gray-900">SignAI</span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <Link href="#features" className="text-gray-600 hover:text-blue-600 transition-colors">Features</Link>
              <Link href="#demo" className="text-gray-600 hover:text-blue-600 transition-colors">Demo</Link>
              <Link href="/dashboard" className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center gap-2">
                Launch App <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-sm font-medium mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            Real-time Detection Live
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-slate-900 mb-6">
            Bridging Communication <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
              With AI-Powered Sign
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            Instant sign language translation powered by advanced computer vision. 
            Connect seamlessly with everyone, everywhere.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/dashboard" className="w-full sm:w-auto px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold text-lg hover:bg-blue-700 transition-all shadow-lg hover:shadow-blue-200 flex items-center justify-center gap-2">
              <Camera className="h-5 w-5" /> Start Detection
            </Link>
            <Link href="#demo" className="w-full sm:w-auto px-8 py-4 bg-white text-slate-700 border border-gray-200 rounded-xl font-semibold text-lg hover:bg-gray-50 transition-all flex items-center justify-center gap-2">
              <Play className="h-5 w-5" /> View Demo
            </Link>
          </div>

          {/* Tech Check Badges */}
          <div className="mt-12 flex flex-wrap justify-center gap-6 text-sm text-gray-500 font-medium">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-green-500" /> OpenCV Native
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-green-500" /> MediaPipe
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-green-500" /> 99.8% Accuracy
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Enterprise-Grade Features</h2>
            <p className="text-gray-600 max-w-xl mx-auto">Built for reliability and speed, ensuring seamless communication in any environment.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <div key={idx} className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                <div className="h-12 w-12 bg-blue-50 rounded-xl flex items-center justify-center mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <Bot className="h-6 w-6 text-blue-600" />
            <span className="font-bold text-lg text-slate-900">SignAI</span>
          </div>
          <p className="text-gray-500 text-sm">© 2026 SignAI Project. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

const features = [
  {
    icon: <Camera className="h-6 w-6 text-blue-600" />,
    title: "Real-time Vision",
    description: "Advanced hand tracking at 60fps using optimized MediaPipe models directly in your browser."
  },
  {
    icon: <Mic className="h-6 w-6 text-blue-600" />,
    title: "Voice Synthesis",
    description: "Convert recognized sign language gestures instantly into natural-sounding speech output."
  },
  {
    icon: <History className="h-6 w-6 text-blue-600" />,
    title: "Consultation Logs",
    description: "Automatically save transcriptions and export them as PDF reports for medical or legal records."
  }
];
