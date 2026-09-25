import React, { useState } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import SeverityBadge from '../components/SeverityBadge';
import EmergencyAlert from '../components/EmergencyAlert';
import { 
  Activity, 
  UserCheck, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  HelpCircle, 
  ArrowRight, 
  ArrowLeft, 
  Stethoscope, 
  Sparkles, 
  Info,
  Calendar,
  ChevronDown,
  ChevronUp,
  Cpu,
  Layers,
  Terminal,
  Eye,
  FileText
} from 'lucide-react';

const AnalysisResult = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [technicalOpen, setTechnicalOpen] = useState(false);

  // Retrieve analysis result from navigation state
  const analysis = location.state?.result;

  if (!analysis) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center p-6 text-center">
        <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center text-slate-400 mb-4">
          <HelpCircle className="w-8 h-8" />
        </div>
        <h3 className="text-lg font-bold text-slate-800 mb-2">No Active Health Analysis Found</h3>
        <p className="text-xs text-slate-500 max-w-sm mb-6">
          Please complete the symptom intake first to receive preliminary health insights.
        </p>
        <Link
          to="/symptom-checker"
          className="px-5 py-2.5 rounded-xl bg-health-600 hover:bg-health-700 text-white font-semibold text-xs shadow-sm transition-all"
        >
          Start Symptom Check
        </Link>
      </div>
    );
  }

  const {
    predictions = [],
    top_condition = 'Undetermined',
    severity = 'MODERATE',
    emergency = false,
    emergency_message = '',
    emergency_event = '',
    specialist = 'General Physician',
    description = '',
    important_symptoms = [],
    input_symptoms = [],
    prevention = [],
    warning_signs = [],
    ensemble_architecture = {},
    disclaimer,
    image_analyzed = false,
    image_details = null,
    problem_description = '',
    patient_details = {},
    symptom_parameters = {},
    quantum_analysis = {}
  } = analysis;

  return (
    <div className="min-h-screen bg-slate-50 py-10">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Navigation & Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <Link
              to="/symptom-checker"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 mb-2 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Back to Symptom Intake
            </Link>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-health-100 text-health-700">
                <Sparkles className="w-4 h-4" />
              </span>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                AI Health Insights
              </h1>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Preliminary analysis based on your reported symptoms and clinical triage rules
            </p>
          </div>

          <div className="flex items-center gap-3">
            <SeverityBadge severity={severity} size="md" />
          </div>
        </div>

        {/* High Priority Emergency Banner if Triggered */}
        {emergency && (
          <EmergencyAlert
            message={emergency_message}
            emergencyEvent={emergency_event}
          />
        )}

        {/* Primary Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Top Possible Conditions & Clinical Overview (Priority 1, 2, 3) */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* Top 3 Conditions Card */}
            <div className="bg-white rounded-3xl p-6 sm:p-7 shadow-sm border border-slate-200/90">
              <div className="flex items-center justify-between mb-5">
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-health-600">
                    PRELIMINARY ASSESSMENT
                  </span>
                  <h2 className="text-xl font-bold text-slate-900">
                    Possible Health Conditions
                  </h2>
                </div>
                <span className="text-[11px] font-medium text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full">
                  AI-Estimated Likelihood
                </span>
              </div>

              <div className="space-y-4">
                {predictions.map((pred, index) => {
                  const isTop = index === 0;
                  const probPct = pred.confidence_percent || Math.round(pred.probability * 100);

                  return (
                    <div
                      key={pred.disease}
                      className={`p-4 rounded-2xl border transition-all ${
                        isTop
                          ? 'bg-gradient-to-br from-health-50/60 to-tealAccent-50/30 border-health-300 ring-2 ring-health-500/10'
                          : 'bg-slate-50/70 border-slate-200'
                      }`}
                    >
                      <div className="flex items-start justify-between gap-3 mb-2">
                        <div className="flex items-center gap-2.5">
                          <span
                            className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                              isTop ? 'bg-health-600 text-white' : 'bg-slate-200 text-slate-600'
                            }`}
                          >
                            #{index + 1}
                          </span>
                          <div>
                            <h4 className="text-base font-bold text-slate-900">
                              {pred.disease}
                            </h4>
                            <span className="text-[11px] text-slate-500">
                              {isTop ? 'Primary Condition Candidate' : 'Alternative Condition'}
                            </span>
                          </div>
                        </div>

                        <div className="text-right">
                          <span className="text-xs text-slate-400 font-medium block">
                            Estimated Likelihood
                          </span>
                          <span
                            className={`text-base font-extrabold ${
                              isTop ? 'text-health-700' : 'text-slate-700'
                            }`}
                          >
                            {probPct}%
                          </span>
                        </div>
                      </div>

                      {/* Progress Bar */}
                      <div className="w-full bg-slate-200 rounded-full h-2 overflow-hidden mt-1">
                        <div
                          className={`h-2 rounded-full transition-all duration-700 ${
                            isTop
                              ? 'bg-gradient-to-r from-health-600 to-tealAccent-500'
                              : 'bg-slate-400'
                          }`}
                          style={{ width: `${probPct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Primary Condition Overview */}
              {description && (
                <div className="mt-6 pt-5 border-t border-slate-100">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5">
                    About {top_condition}
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
                    {description}
                  </p>
                </div>
              )}
            </div>

            {/* Contributing Symptoms Highlight */}
            {important_symptoms.length > 0 && (
              <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-200/90">
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="w-5 h-5 text-health-600" />
                  <h3 className="text-base font-bold text-slate-900">
                    Contributing Symptoms
                  </h3>
                </div>
                <p className="text-xs text-slate-500 mb-4">
                  These symptoms you reported contributed most directly to the health insight:
                </p>

                <div className="flex flex-wrap gap-2">
                  {important_symptoms.map((sym, i) => (
                    <span
                      key={i}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-health-50 text-health-800 border border-health-200 text-xs font-semibold"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 text-health-600" />
                      {sym}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Visual Information Note (Only shown if image was analyzed) */}
            {image_analyzed && (
              <div className="bg-white rounded-3xl p-6 shadow-sm border border-tealAccent-200/90 bg-gradient-to-br from-tealAccent-50/40 to-white">
                <div className="flex items-start gap-3">
                  <div className="w-9 h-9 rounded-xl bg-tealAccent-100 text-tealAccent-700 flex items-center justify-center shrink-0">
                    <Eye className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Visual Information Verified
                    </h3>
                    <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                      Visual information was considered as part of this assessment. Medical photo metadata and color/texture descriptors were safely processed alongside your reported symptoms.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Natural Problem Description Summary */}
            {problem_description && (
              <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-200/90">
                <div className="flex items-center gap-2 mb-2">
                  <FileText className="w-4 h-4 text-health-600" />
                  <h3 className="text-sm font-bold text-slate-900">
                    Reported Problem Description
                  </h3>
                </div>
                <p className="text-xs text-slate-700 italic bg-slate-50 p-3.5 rounded-2xl border border-slate-200/70 leading-relaxed">
                  "{problem_description}"
                </p>
              </div>
            )}

          </div>

          {/* Right Column: Specialist Referral, Guidance & Warning Signs (Priority 4, 5, 6, 7, 8, 9) */}
          <div className="lg:col-span-5 space-y-6">
            
            {/* Recommended Specialist Card with Direct Action (Priority 6 & 8 & 9) */}
            <div className="bg-gradient-to-br from-slate-900 to-health-950 text-white rounded-3xl p-6 shadow-md border border-slate-800">
              <span className="text-[11px] font-bold uppercase tracking-wider text-health-400 block mb-1">
                RECOMMENDED SPECIALIST
              </span>
              <h3 className="text-xl font-extrabold text-white mb-2">
                Consult a {specialist}
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed mb-5">
                Based on your symptom cluster, consulting a certified {specialist} is recommended for comprehensive evaluation and personalized clinical care.
              </p>

              <div className="space-y-2.5">
                <Link
                  to={`/doctors?specialization=${encodeURIComponent(specialist)}`}
                  className="w-full py-3 px-4 rounded-xl bg-health-600 hover:bg-health-500 text-white font-bold text-xs sm:text-sm shadow-md transition-all active:scale-[0.98] flex items-center justify-center gap-2"
                >
                  <UserCheck className="w-4 h-4" />
                  Find a Doctor ({specialist})
                  <ArrowRight className="w-4 h-4" />
                </Link>

                <Link
                  to="/hospitals"
                  className="w-full py-2.5 px-4 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-2 border border-white/15"
                >
                  Explore Nearby Hospitals
                </Link>
              </div>
            </div>

            {/* Red-Flag Warning Signs (Priority 5) */}
            {warning_signs && warning_signs.length > 0 && (
              <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-200/90">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-5 h-5 text-amber-500" />
                  <h3 className="text-base font-bold text-slate-900">
                    Warning Signs to Watch For
                  </h3>
                </div>
                <p className="text-xs text-slate-500 mb-3">
                  Seek immediate medical attention if you develop any of these warning signs:
                </p>

                <ul className="space-y-2">
                  {warning_signs.map((sign, i) => (
                    <li key={i} className="p-2.5 rounded-xl bg-amber-50/70 border border-amber-200 text-xs text-amber-900 font-medium flex items-start gap-2">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                      <span>{sign}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommended Precautions & Care (Priority 7) */}
            {prevention && prevention.length > 0 && (
              <div className="bg-white rounded-3xl p-6 shadow-sm border border-slate-200/90">
                <div className="flex items-center gap-2 mb-3">
                  <ShieldCheck className="w-5 h-5 text-emerald-600" />
                  <h3 className="text-base font-bold text-slate-900">
                    General Health Guidance
                  </h3>
                </div>

                <ul className="space-y-2.5">
                  {prevention.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs text-slate-700 leading-relaxed">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

          </div>

        </div>

        {/* Optional Secondary Section: How HealthConnect Analyzes Your Symptoms (Requirements 9 & 10) */}
        <div className="bg-white rounded-3xl border border-slate-200/90 overflow-hidden shadow-sm">
          <button
            onClick={() => setTechnicalOpen(!technicalOpen)}
            className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-health-50 text-health-700 flex items-center justify-center">
                <Cpu className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900">How HealthConnect analyzes your symptoms</h3>
                <p className="text-xs text-slate-500">Optional technical overview of how our clinical AI pipeline processes your inputs.</p>
              </div>
            </div>
            {technicalOpen ? <ChevronUp className="w-5 h-5 text-slate-400" /> : <ChevronDown className="w-5 h-5 text-slate-400" />}
          </button>

          {technicalOpen && (
            <div className="px-6 pb-6 pt-3 border-t border-slate-100 bg-slate-50/50 space-y-5 text-xs text-slate-700">
              
              {/* 4-Step Analysis Pipeline Flow */}
              <div>
                <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Analysis Pipeline Flow
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-2 text-center">
                  <div className="p-2.5 rounded-xl bg-white border border-slate-200 font-semibold text-slate-800">
                    1. Symptoms
                  </div>
                  <div className="p-2.5 rounded-xl bg-white border border-slate-200 font-semibold text-slate-800">
                    2. Feature Processing
                  </div>
                  <div className="p-2.5 rounded-xl bg-white border border-slate-200 font-semibold text-slate-800">
                    3. Advanced AI Analysis
                  </div>
                  <div className="p-2.5 rounded-xl bg-white border border-slate-200 font-semibold text-slate-800">
                    4. Health Insights
                  </div>
                </div>
              </div>

              {/* Required Concise Statement */}
              <div className="p-4 rounded-xl bg-white border border-slate-200">
                <p className="text-xs text-slate-700 font-medium leading-relaxed">
                  HealthConnect uses a hybrid AI architecture combining classical machine learning and quantum machine learning techniques.
                </p>
              </div>

              {/* Secondary Technical Reference */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="p-3.5 rounded-xl bg-white border border-slate-200">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Classical ML Models</div>
                  <div className="font-bold text-slate-900 mt-1">Random Forest + XGBoost</div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    Multi-tree soft-voting classification ensemble
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-white border border-slate-200">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Quantum ML Models</div>
                  <div className="font-bold text-slate-900 mt-1">4-Qubit Simulator (PennyLane)</div>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    {quantum_analysis?.simulator || 'PennyLane default.qubit (QNN, VQC & QSVM)'}
                  </div>
                </div>
              </div>

              {/* Quantum Expectation Values & Feature Mapping if available */}
              {quantum_analysis?.expectation_values && (
                <div className="p-3.5 rounded-xl bg-white border border-slate-200 space-y-2">
                  <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                    4-Qubit Circuit Statevector Measurements & Expectation Values
                  </div>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
                    {quantum_analysis.expectation_values.map((ev, idx) => (
                      <div key={idx} className="p-2 rounded-lg bg-slate-50 border border-slate-200/80">
                        <span className="text-[10px] font-semibold text-slate-400 block">Qubit {idx} ⟨Z_{idx}⟩</span>
                        <span className="text-xs font-mono font-bold text-slate-800">{ev.toFixed(4)}</span>
                      </div>
                    ))}
                  </div>
                  {quantum_analysis.circuits_evaluated && (
                    <div className="text-[10px] text-slate-400 pt-1">
                      Circuits: {quantum_analysis.circuits_evaluated.join(' • ')}
                    </div>
                  )}
                </div>
              )}

              <div className="text-[11px] text-slate-500 pt-1">
                Evaluated {input_symptoms.length} symptoms against local clinical knowledge base and triage safety guidelines.
              </div>

            </div>
          )}
        </div>

        {/* Visible Medical Disclaimer (Step 23) */}
        <div className="p-5 rounded-2xl bg-slate-100 border border-slate-200 text-xs text-slate-600 leading-relaxed flex items-start gap-3">
          <Info className="w-5 h-5 text-slate-500 shrink-0 mt-0.5" />
          <div>
            <strong className="text-slate-800 block mb-0.5 font-semibold">
              Medical Decision Support Disclaimer
            </strong>
            {disclaimer || "HealthConnect provides preliminary AI-assisted health information and is not a substitute for professional medical diagnosis or treatment. Seek immediate medical attention in emergencies."}
          </div>
        </div>

      </div>
    </div>
  );
};

export default AnalysisResult;
