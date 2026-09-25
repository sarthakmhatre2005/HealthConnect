import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Stethoscope, 
  UserCheck, 
  Building2, 
  Calendar, 
  ShieldCheck, 
  HeartPulse, 
  ArrowRight, 
  CheckCircle2, 
  Sparkles,
  Activity,
  Cpu,
  Clock,
  Lock,
  Layers,
  HelpCircle
} from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      
      {/* 1. Hero Section (Step 3 & 4) */}
      <section className="relative overflow-hidden bg-gradient-to-b from-health-950 via-slate-900 to-slate-950 text-white pt-16 pb-20 lg:pt-24 lg:pb-28">
        {/* Subtle Background Glows */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-health-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-1/3 right-10 w-80 h-80 bg-tealAccent-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            
            {/* Hero Text */}
            <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
              
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/15 text-health-300 text-xs font-semibold backdrop-blur-sm shadow-inner">
                <Sparkles className="w-3.5 h-3.5 text-tealAccent-300" />
                <span>HEALTHCONNECT PLATFORM</span>
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight">
                Intelligent Healthcare,{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-health-300 via-tealAccent-300 to-emerald-300 block sm:inline">
                  Connected Around You
                </span>
              </h1>

              <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
                Get preliminary health insights, discover the right specialist, and manage your healthcare journey in one connected platform.
              </p>

              {/* CTAs (Step 3) */}
              <div className="pt-2 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
                <Link
                  to="/symptom-checker"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-health-600 hover:bg-health-500 text-white font-bold text-sm sm:text-base shadow-lg shadow-health-600/25 transition-all duration-200 active:scale-95"
                >
                  <Stethoscope className="w-5 h-5" />
                  CHECK YOUR SYMPTOMS
                  <ArrowRight className="w-4 h-4 ml-1" />
                </Link>

                <Link
                  to="/doctors"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-sm sm:text-base border border-white/20 backdrop-blur-sm transition-all active:scale-95"
                >
                  <UserCheck className="w-5 h-5 text-health-300" />
                  FIND A DOCTOR
                </Link>
              </div>

              {/* Patient Trust Highlights */}
              <div className="pt-6 border-t border-slate-800/80 grid grid-cols-3 gap-4 text-center lg:text-left">
                <div>
                  <div className="text-sm sm:text-base font-bold text-white flex items-center justify-center lg:justify-start gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-tealAccent-400" />
                    <span>Confidential</span>
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">Privacy-First Processing</div>
                </div>
                <div>
                  <div className="text-sm sm:text-base font-bold text-white flex items-center justify-center lg:justify-start gap-1.5">
                    <UserCheck className="w-4 h-4 text-health-400" />
                    <span>Verified</span>
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">Specialist Doctors</div>
                </div>
                <div>
                  <div className="text-sm sm:text-base font-bold text-white flex items-center justify-center lg:justify-start gap-1.5">
                    <Building2 className="w-4 h-4 text-emerald-400" />
                    <span>Accredited</span>
                  </div>
                  <div className="text-xs text-slate-400 mt-0.5">Hospitals & Centers</div>
                </div>
              </div>

            </div>

            {/* Hero Visual (Step 4) - Healthcare Ecosystem Visual */}
            <div className="lg:col-span-5 flex justify-center">
              <div className="w-full max-w-md rounded-2xl bg-slate-900/90 border border-slate-800 p-6 shadow-2xl backdrop-blur-sm space-y-4">
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-emerald-500" />
                    <span className="text-xs font-semibold text-slate-300">Connected Care Ecosystem</span>
                  </div>
                  <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-health-900/50 text-health-300 border border-health-700/50">Live</span>
                </div>

                {/* Visual Step 1: Patient Check */}
                <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-health-500/20 text-health-400 flex items-center justify-center shrink-0">
                    <Stethoscope className="w-5 h-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold text-white">1. Patient Health Check</div>
                    <div className="text-[11px] text-slate-400 truncate">Clinical symptom analysis & initial triage</div>
                  </div>
                  <span className="text-xs text-emerald-400 font-semibold">Active</span>
                </div>

                {/* Visual Step 2: Intelligent Routing */}
                <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-tealAccent-500/20 text-tealAccent-400 flex items-center justify-center shrink-0">
                    <Activity className="w-5 h-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold text-white">2. Health Guidance</div>
                    <div className="text-[11px] text-slate-400 truncate">Specialist matching & severity assessment</div>
                  </div>
                  <span className="text-xs text-tealAccent-400 font-semibold">Instant</span>
                </div>

                {/* Visual Step 3: Verified Specialist */}
                <div className="p-3.5 rounded-xl bg-slate-800/80 border border-slate-700/60 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0">
                    <UserCheck className="w-5 h-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold text-white">3. Professional Care</div>
                    <div className="text-[11px] text-slate-400 truncate">Schedule consultation with certified doctors</div>
                  </div>
                  <span className="text-xs text-indigo-400 font-semibold">Connected</span>
                </div>

              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 2. Patient-First Feature Section (Step 6) */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-widest text-health-600 mb-2">
              Patient-First Platform
            </h2>
            <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              Designed for Your Healthcare Journey
            </h3>
            <p className="mt-3 text-slate-600 text-sm sm:text-base leading-relaxed">
              HealthConnect brings together intelligent health awareness, trusted medical professionals, and seamless care coordination.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            {/* Card 1: AI Health Insights */}
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-all duration-200 flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-health-100 text-health-700 flex items-center justify-center mb-4">
                  <Stethoscope className="w-6 h-6" />
                </div>
                <h4 className="text-lg font-bold text-slate-900 mb-2">AI Health Insights</h4>
                <p className="text-sm text-slate-600 leading-relaxed mb-4">
                  Understand your symptoms with intelligent preliminary health analysis.
                </p>
              </div>
              <Link to="/symptom-checker" className="text-xs font-bold text-health-600 hover:text-health-700 inline-flex items-center gap-1">
                Check symptoms <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Card 2: Find the Right Specialist */}
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-all duration-200 flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-tealAccent-100 text-tealAccent-700 flex items-center justify-center mb-4">
                  <UserCheck className="w-6 h-6" />
                </div>
                <h4 className="text-lg font-bold text-slate-900 mb-2">Find the Right Specialist</h4>
                <p className="text-sm text-slate-600 leading-relaxed mb-4">
                  Discover healthcare professionals suited to your needs.
                </p>
              </div>
              <Link to="/doctors" className="text-xs font-bold text-health-600 hover:text-health-700 inline-flex items-center gap-1">
                Find doctors <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Card 3: Hospitals Around You */}
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-all duration-200 flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4">
                  <Building2 className="w-6 h-6" />
                </div>
                <h4 className="text-lg font-bold text-slate-900 mb-2">Hospitals Around You</h4>
                <p className="text-sm text-slate-600 leading-relaxed mb-4">
                  Explore healthcare facilities and available services.
                </p>
              </div>
              <Link to="/hospitals" className="text-xs font-bold text-health-600 hover:text-health-700 inline-flex items-center gap-1">
                Browse hospitals <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Card 4: Easy Appointments */}
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-all duration-200 flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center mb-4">
                  <Calendar className="w-6 h-6" />
                </div>
                <h4 className="text-lg font-bold text-slate-900 mb-2">Easy Appointments</h4>
                <p className="text-sm text-slate-600 leading-relaxed mb-4">
                  Book and manage consultations in one place.
                </p>
              </div>
              <Link to="/appointments" className="text-xs font-bold text-health-600 hover:text-health-700 inline-flex items-center gap-1">
                Manage appointments <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Card 5: Privacy-First */}
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-all duration-200 flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-cyan-100 text-cyan-700 flex items-center justify-center mb-4">
                  <Lock className="w-6 h-6" />
                </div>
                <h4 className="text-lg font-bold text-slate-900 mb-2">Privacy-First</h4>
                <p className="text-sm text-slate-600 leading-relaxed mb-4">
                  Designed with privacy-conscious healthcare processing.
                </p>
              </div>
              <span className="text-xs font-semibold text-tealAccent-700">
                Confidential processing
              </span>
            </div>

            {/* Card 6: Connected Care */}
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-all duration-200 flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center mb-4">
                  <HeartPulse className="w-6 h-6" />
                </div>
                <h4 className="text-lg font-bold text-slate-900 mb-2">Connected Care</h4>
                <p className="text-sm text-slate-600 leading-relaxed mb-4">
                  Move from symptom awareness to professional consultation.
                </p>
              </div>
              <Link to="/doctors" className="text-xs font-bold text-health-600 hover:text-health-700 inline-flex items-center gap-1">
                Explore specialists <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

          </div>
        </div>
      </section>

      {/* 3. Intelligent Health Analysis Section (Step 7) */}
      <section className="py-20 bg-slate-50 border-t border-slate-200/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-health-100 text-health-800 text-xs font-bold uppercase tracking-wider mb-2">
              <Sparkles className="w-3.5 h-3.5 text-health-600" />
              Intelligent Health Analysis
            </div>
            <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              A Structured Path from Symptoms to Care
            </h3>
            <p className="mt-3 text-slate-600 text-sm sm:text-base leading-relaxed">
              HealthConnect uses advanced AI techniques to analyze reported symptoms and provide preliminary health insights while helping users understand their next steps.
            </p>
          </div>

          {/* Simple Clean Workflow (Step 7) */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 text-center">
            {[
              { title: "Symptoms", desc: "Patient selects symptoms", icon: Stethoscope },
              { title: "AI Analysis", desc: "Multi-factor evaluation", icon: Activity },
              { title: "Health Insights", desc: "Top condition likelihoods", icon: Sparkles },
              { title: "Care Guidance", desc: "Severity & precautions", icon: ShieldCheck },
              { title: "Specialist", desc: "Targeted discipline match", icon: UserCheck },
              { title: "Consultation", desc: "Direct doctor appointment", icon: Calendar }
            ].map((step, idx) => (
              <div key={idx} className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs flex flex-col items-center justify-center">
                <div className="w-10 h-10 rounded-full bg-health-50 text-health-700 flex items-center justify-center mb-3">
                  <step.icon className="w-5 h-5" />
                </div>
                <div className="text-sm font-bold text-slate-900 mb-1">{step.title}</div>
                <div className="text-xs text-slate-500 leading-snug">{step.desc}</div>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* 4. Ready to Take the Next Step in Your Care */}
      <section className="py-20 bg-white border-t border-slate-200/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-health-950 text-white p-8 sm:p-12 shadow-xl border border-slate-800 text-center space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-health-500/20 text-health-300 text-xs font-semibold border border-health-500/30">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Proactive Health Management</span>
            </div>
            <h3 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
              Take Control of Your Health Today
            </h3>
            <p className="text-sm sm:text-base text-slate-300 max-w-2xl mx-auto leading-relaxed">
              Start with our symptom checker to receive instant preliminary health insights, or connect directly with accredited specialists across top hospital networks.
            </p>
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to="/symptom-checker"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-health-600 hover:bg-health-500 text-white font-bold text-sm shadow-lg shadow-health-600/25 transition-all active:scale-95"
              >
                <Stethoscope className="w-4 h-4" />
                CHECK YOUR SYMPTOMS
              </Link>
              <Link
                to="/doctors"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-sm border border-white/20 backdrop-blur-sm transition-all active:scale-95"
              >
                <UserCheck className="w-4 h-4 text-health-300" />
                FIND A DOCTOR
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Medical Disclaimer Section (Step 23) */}
      <section className="py-10 bg-slate-100 border-t border-slate-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-slate-600 mb-2">
            <HelpCircle className="w-4 h-4 text-health-600" />
            <span>Important Healthcare Information</span>
          </div>
          <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
            HealthConnect provides preliminary AI-assisted health information and is not a substitute for professional medical diagnosis or treatment. For emergency medical situations, seek immediate medical attention.
          </p>
        </div>
      </section>

    </div>
  );
};

export default Home;
