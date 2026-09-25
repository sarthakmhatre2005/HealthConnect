import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { symptomAPI } from '../services/api';
import { 
  Stethoscope, 
  Search, 
  X, 
  Check, 
  AlertCircle, 
  Activity, 
  ArrowRight, 
  ArrowLeft, 
  Clock, 
  Sparkles, 
  ShieldCheck,
  Camera,
  Upload,
  Trash2,
  FileText,
  Info,
  AlertTriangle,
  Eye,
  User,
  Heart,
  Pill,
  Thermometer,
  Sliders,
  CheckCircle2,
  ChevronRight,
  ChevronDown
} from 'lucide-react';

const COMMON_CONDITIONS = [
  'Hypertension (High Blood Pressure)',
  'Type 2 Diabetes',
  'Asthma / Respiratory Illness',
  'Heart Disease / CAD',
  'Thyroid Disorder',
  'Kidney Disease',
  'None'
];

const SymptomChecker = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  // Guided Steps: 1 = Patient Details, 2 = Describe Problem, 3 = Symptoms & Parameters, 4 = Optional Photo & Review, 5 = Analyzing animation
  const [step, setStep] = useState(1);

  // STEP 1: Patient Details
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('Male');
  const [existingConditions, setExistingConditions] = useState([]);
  const [customCondition, setCustomCondition] = useState('');
  const [medications, setMedications] = useState('');
  const [allergies, setAllergies] = useState('');

  // STEP 2: Natural Problem Description
  const [problemDescription, setProblemDescription] = useState('');
  const [nlpLoading, setNlpLoading] = useState(false);
  const [nlpExtracted, setNlpExtracted] = useState(null);
  const [nlpApplied, setNlpApplied] = useState(false);

  // STEP 3: Symptoms & Dynamic Parameters
  const [allSymptoms, setAllSymptoms] = useState([]);
  const [categories, setCategories] = useState({});
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');
  const [symptomParams, setSymptomParams] = useState({});
  const [paramSchemas, setParamSchemas] = useState({});
  const [validationErrors, setValidationErrors] = useState({});

  // STEP 4: Optional Visual Image Upload
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [imageError, setImageError] = useState(null);
  const [hasVisualSymptom, setHasVisualSymptom] = useState(false);

  // Status & Progress State
  const [loadingMetadata, setLoadingMetadata] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisStage, setAnalysisStage] = useState(0);
  const [error, setError] = useState(null);

  // Fetch symptom catalog and parameter schemas on mount
  useEffect(() => {
    loadMetadata();
  }, []);

  const loadMetadata = async () => {
    try {
      setLoadingMetadata(true);
      const [symRes, paramRes] = await Promise.all([
        symptomAPI.getSymptomsList(),
        symptomAPI.getParameterMetadata()
      ]);

      if (symRes.data?.success && symRes.data?.data) {
        setAllSymptoms(symRes.data.data.symptoms || []);
        setCategories(symRes.data.data.categories || {});
      }

      if (paramRes.data?.success && paramRes.data?.data?.definitions) {
        setParamSchemas(paramRes.data.data.definitions);
      }
    } catch (e) {
      console.error('Failed to load metadata:', e);
      setError('Could not connect to medical catalog. Please ensure the backend is running.');
    } finally {
      setLoadingMetadata(false);
    }
  };

  // Check if visual complaint is present (dermatological symptoms or NLP flag)
  useEffect(() => {
    const visualKeys = [
      'skin_rash', 'nodal_skin_eruptions', 'yellowish_skin', 'red_spots_over_body',
      'pus_filled_pimples', 'blackheads', 'skin_peeling', 'blister', 'yellow_crust_ooze',
      'dischromic_patches', 'bruising', 'itching'
    ];
    const isVisualSymptom = selectedSymptoms.some(s => {
      const clean = s.toLowerCase().replace(/ /g, '_');
      return visualKeys.includes(clean);
    });
    setHasVisualSymptom(isVisualSymptom || Boolean(nlpExtracted?.has_visual_mention));
  }, [selectedSymptoms, nlpExtracted]);

  // Handle NLP Extraction from free-text problem description
  const handleExtractNlp = async () => {
    if (!problemDescription.trim()) return;
    setNlpLoading(true);
    setError(null);
    try {
      const res = await symptomAPI.extractNlp(problemDescription);
      if (res.data?.success) {
        setNlpExtracted(res.data);
        // Pre-select extracted symptoms that aren't already selected
        const newSyms = res.data.extracted_symptoms_display || [];
        const merged = Array.from(new Set([...selectedSymptoms, ...newSyms]));
        setSelectedSymptoms(merged);
        setNlpApplied(true);
      }
    } catch (e) {
      console.warn('NLP extraction notice:', e);
    } finally {
      setNlpLoading(false);
    }
  };

  // Toggle symptom selection
  const handleToggleSymptom = (symptom) => {
    if (selectedSymptoms.includes(symptom)) {
      setSelectedSymptoms(selectedSymptoms.filter((s) => s !== symptom));
      // Clean up params
      const cleanKey = symptom.toLowerCase().replace(/ /g, '_');
      const updated = { ...symptomParams };
      delete updated[cleanKey];
      setSymptomParams(updated);
    } else {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
    setError(null);
  };

  // Update parameter values for a specific symptom
  const handleParamChange = (symptomKey, paramName, value) => {
    const cleanSym = symptomKey.toLowerCase().replace(/ /g, '_');
    setSymptomParams(prev => ({
      ...prev,
      [cleanSym]: {
        ...(prev[cleanSym] || {}),
        [paramName]: value
      }
    }));
    // Clear validation error if any
    const errKey = `${cleanSym}.${paramName}`;
    if (validationErrors[errKey]) {
      const copy = { ...validationErrors };
      delete copy[errKey];
      setValidationErrors(copy);
    }
  };

  // Toggle existing medical condition
  const handleToggleCondition = (cond) => {
    if (cond === 'None') {
      setExistingConditions(['None']);
      return;
    }
    let updated = existingConditions.filter(c => c !== 'None');
    if (updated.includes(cond)) {
      updated = updated.filter(c => c !== cond);
    } else {
      updated = [...updated, cond];
    }
    setExistingConditions(updated);
  };

  const handleAddCustomCondition = () => {
    if (customCondition.trim() && !existingConditions.includes(customCondition.trim())) {
      setExistingConditions([...existingConditions.filter(c => c !== 'None'), customCondition.trim()]);
      setCustomCondition('');
    }
  };

  // Handle Image Selection
  const handleImageChange = (e) => {
    setImageError(null);
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setImageError('Only JPG, JPEG, PNG, or WEBP image formats are allowed.');
      return;
    }

    // Validate size (max 5 MB)
    if (file.size > 5 * 1024 * 1024) {
      setImageError('Image file exceeds the 5 MB limit. Please select a smaller photo.');
      return;
    }

    setImageFile(file);
    const reader = new FileReader();
    reader.onload = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleRemoveImage = () => {
    setImageFile(null);
    setImagePreview(null);
    setImageError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // Validate step navigation
  const handleNextStep = async () => {
    setError(null);
    if (step === 1) {
      if (age && (parseInt(age) < 1 || parseInt(age) > 120)) {
        setError('Please enter a valid age between 1 and 120 years.');
        return;
      }
      setStep(2);
    } else if (step === 2) {
      // If user typed problem description, auto-run NLP extraction if not yet extracted
      if (problemDescription.trim() && !nlpApplied) {
        await handleExtractNlp();
      }
      setStep(3);
    } else if (step === 3) {
      if (selectedSymptoms.length === 0) {
        setError('Please select at least one symptom or describe your symptoms in Step 2.');
        return;
      }
      setStep(4);
    }
  };

  // Submit complete multimodal intake
  const handleSubmitAnalysis = async () => {
    if (selectedSymptoms.length === 0) {
      setError('Please select at least one symptom to perform clinical analysis.');
      setStep(3);
      return;
    }

    setAnalyzing(true);
    setError(null);

    // Dynamic animation sequence stages
    const stages = [
      'Processing reported symptoms & parameters...',
      'Evaluating clinical knowledge base & disease patterns...',
      'Executing dual ensemble: Random Forest & XGBoost...',
      '4-Qubit Quantum Feature Encoding: QNN, VQC & QSVM Simulator...',
      'Applying emergency triage safety rules...',
      'Preparing personalized health insights...'
    ];

    let currentStage = 0;
    const interval = setInterval(() => {
      currentStage = (currentStage + 1) % stages.length;
      setAnalysisStage(currentStage);
    }, 450);

    try {
      const patientDetailsObj = {
        age: age ? parseInt(age) : null,
        gender: gender,
        existing_conditions: existingConditions,
        current_medications: medications,
        allergies: allergies,
        duration: '1-2 days',
        severity: 'Moderate'
      };

      let response;
      if (imageFile) {
        // Multipart/form-data upload with attached photo
        const formData = new FormData();
        formData.append('symptoms', JSON.stringify(selectedSymptoms));
        formData.append('problem_description', problemDescription);
        formData.append('patient_details', JSON.stringify(patientDetailsObj));
        formData.append('symptom_parameters', JSON.stringify(symptomParams));
        formData.append('image', imageFile);

        response = await symptomAPI.analyzeSymptoms(formData, true);
      } else {
        // Standard JSON payload
        const payload = {
          symptoms: selectedSymptoms,
          problem_description: problemDescription,
          patient_details: patientDetailsObj,
          symptom_parameters: symptomParams,
          age: age ? parseInt(age) : null,
          gender: gender,
          duration: '1-2 days',
          severity: 'Moderate'
        };

        response = await symptomAPI.analyzeSymptoms(payload, false);
      }

      clearInterval(interval);

      if (response.data && response.data.success) {
        navigate('/symptom-results', { state: { result: response.data } });
      } else {
        setError(response.data?.error || 'Clinical analysis could not be generated.');
        setAnalyzing(false);
      }
    } catch (err) {
      clearInterval(interval);
      setError(err.message || 'An error occurred during symptom analysis.');
      setAnalyzing(false);
    }
  };

  // Filtered symptoms catalog based on category and search query
  const getFilteredSymptoms = () => {
    let list = allSymptoms;
    if (activeCategory !== 'All' && categories[activeCategory]) {
      list = categories[activeCategory];
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter((s) => s.toLowerCase().includes(q));
    }
    return list;
  };

  const filteredSymptoms = getFilteredSymptoms();

  // -------------------------------------------------------------------
  // STEP 5: Full Screen Medical Loading Animation
  // -------------------------------------------------------------------
  if (analyzing) {
    const stageMessages = [
      { title: 'Processing Your Symptoms', desc: 'Validating clinical parameters and patient context...' },
      { title: 'Evaluating Health Patterns', desc: 'Matching against 41 disease profiles & triage database...' },
      { title: 'Dual Classical ML Ensemble', desc: 'Running Random Forest (120 trees) & XGBoost classifier...' },
      { title: '4-Qubit Quantum Feature Encoding', desc: 'Simulating parameterized quantum circuits (PennyLane QNN/VQC/QSVM)...' },
      { title: 'Emergency Safety Triage', desc: 'Screening for acute red-flag indicators & urgency criteria...' },
      { title: 'Finalizing Health Insights', desc: 'Preparing explainable condition likelihood & specialist referral...' }
    ];
    const current = stageMessages[analysisStage] || stageMessages[0];

    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center p-6 text-center animate-in fade-in">
        <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-health-600 to-tealAccent-500 text-white flex items-center justify-center shadow-xl shadow-health-600/20 mb-8 relative">
          <Activity className="w-10 h-10 animate-spin" />
          <div className="absolute -top-1 -right-1 w-4 h-4 bg-tealAccent-400 rounded-full animate-ping" />
        </div>

        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mb-2">
          {current.title}
        </h2>
        
        <p className="text-sm text-slate-600 max-w-md mb-8 leading-relaxed">
          {current.desc}
        </p>

        {/* Progress Stages Bar */}
        <div className="w-full max-w-md bg-slate-100 rounded-2xl p-4 border border-slate-200/90 shadow-sm space-y-2.5 text-xs text-left">
          <div className="flex items-center justify-between text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">
            <span>Multi-Stage AI Analysis</span>
            <span>Step {analysisStage + 1} of 6</span>
          </div>
          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-health-600 to-tealAccent-500 transition-all duration-300 rounded-full"
              style={{ width: `${((analysisStage + 1) / 6) * 100}%` }}
            />
          </div>
          <div className="pt-2 text-[11px] text-slate-500 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-health-600" />
            <span>Dual Classical ML Ensemble + 4-Qubit Quantum Simulator</span>
          </div>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------------
  // MAIN INTAKE UI (Steps 1 to 4)
  // -------------------------------------------------------------------
  return (
    <div className="min-h-screen bg-slate-50 py-8 sm:py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6">
        
        {/* Header */}
        <div className="text-center max-w-2xl mx-auto mb-8">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-health-100 text-health-800 text-xs font-bold uppercase tracking-wider mb-3">
            <Stethoscope className="w-3.5 h-3.5 text-health-600" />
            Next-Generation Health Consultation Intake
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Tell us what you're experiencing
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 mt-2">
            Describe your problem naturally, provide specific symptom parameters, and optionally attach a photo for visual skin complaints.
          </p>
        </div>

        {/* 4-Step Progress Navigation Header */}
        <div className="mb-8 max-w-2xl mx-auto">
          <div className="flex items-center justify-between relative">
            <div className="absolute left-0 top-1/2 -translate-y-1/2 h-1 w-full bg-slate-200 -z-0" />
            <div
              className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-health-600 transition-all duration-300 -z-0"
              style={{ width: step === 1 ? '0%' : step === 2 ? '33%' : step === 3 ? '66%' : '100%' }}
            />

            {[
              { num: 1, label: 'Patient Details' },
              { num: 2, label: 'Problem Description' },
              { num: 3, label: 'Symptoms & Parameters' },
              { num: 4, label: 'Photo & Review' }
            ].map((s) => (
              <button
                key={s.num}
                type="button"
                onClick={() => {
                  if (s.num < step) setStep(s.num);
                }}
                className={`w-9 h-9 rounded-full flex items-center justify-center font-bold text-xs relative z-10 transition-all ${
                  step >= s.num
                    ? 'bg-health-600 text-white ring-4 ring-health-100 shadow-sm'
                    : 'bg-slate-200 text-slate-500'
                } ${s.num < step ? 'cursor-pointer hover:bg-health-700' : ''}`}
                aria-label={`Step ${s.num}: ${s.label}`}
              >
                {step > s.num ? <Check className="w-4 h-4" /> : s.num}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-4 text-center text-[10px] sm:text-[11px] font-bold text-slate-500 uppercase tracking-wider mt-2.5">
            <span>1. Details</span>
            <span>2. Describe</span>
            <span>3. Symptoms</span>
            <span>4. Photo & Review</span>
          </div>
        </div>

        {/* Error Notification */}
        {error && (
          <div className="mb-6 max-w-2xl mx-auto p-4 rounded-2xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-center gap-2.5 animate-in fade-in">
            <AlertCircle className="w-5 h-5 shrink-0 text-red-600" />
            <span>{error}</span>
          </div>
        )}

        {/* ============================================================= */}
        {/* STEP 1: PATIENT DETAILS                                       */}
        {/* ============================================================= */}
        {step === 1 && (
          <div className="max-w-2xl mx-auto bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200/90 animate-in fade-in space-y-6">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-health-600">STEP 1 OF 4</span>
              <h2 className="text-xl font-bold text-slate-900 mt-0.5">Patient Details & Context</h2>
              <p className="text-xs text-slate-500 mt-1">
                Providing basic health context helps us calibrate symptom significance and tailor clinical decision support. Unnecessary details are never mandatory.
              </p>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Age */}
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                    Age (Years) <span className="text-slate-400 font-normal">(Optional)</span>
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="120"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    placeholder="E.g., 34"
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none"
                  />
                  <span className="text-[10px] text-slate-400 mt-1 block">Helps adjust baseline risk factors</span>
                </div>

                {/* Biological Sex */}
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                    Biological Sex <span className="text-slate-400 font-normal">(Optional)</span>
                  </label>
                  <select
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none bg-white"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other / Prefer not to say</option>
                  </select>
                  <span className="text-[10px] text-slate-400 mt-1 block">For sex-specific clinical profiles</span>
                </div>
              </div>

              {/* Existing Conditions */}
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center justify-between">
                  <span>Relevant Existing Medical Conditions</span>
                  <span className="text-[10px] text-slate-400 font-normal">Optional</span>
                </label>
                <div className="flex flex-wrap gap-1.5 mb-2">
                  {COMMON_CONDITIONS.map((cond) => {
                    const active = existingConditions.includes(cond);
                    return (
                      <button
                        key={cond}
                        type="button"
                        onClick={() => handleToggleCondition(cond)}
                        className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                          active
                            ? 'bg-health-600 text-white shadow-2xs font-semibold'
                            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                        }`}
                      >
                        {cond}
                      </button>
                    );
                  })}
                </div>

                {/* Write-in condition input */}
                <div className="flex gap-2 mt-2">
                  <input
                    type="text"
                    value={customCondition}
                    onChange={(e) => setCustomCondition(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleAddCustomCondition(); } }}
                    placeholder="Add other pre-existing condition..."
                    className="flex-1 px-3 py-2 rounded-xl border border-slate-300 text-xs text-slate-900 outline-none focus:ring-2 focus:ring-health-500"
                  />
                  <button
                    type="button"
                    onClick={handleAddCustomCondition}
                    className="px-3.5 py-2 rounded-xl bg-slate-200 hover:bg-slate-300 text-slate-800 text-xs font-semibold"
                  >
                    Add
                  </button>
                </div>
              </div>

              {/* Current Medications (Optional) */}
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1 flex items-center justify-between">
                  <span>Current Medications If Any</span>
                  <span className="text-[10px] text-slate-400 font-normal">Optional</span>
                </label>
                <input
                  type="text"
                  value={medications}
                  onChange={(e) => setMedications(e.target.value)}
                  placeholder="E.g., Metformin 500mg, Lisinopril 10mg, Aspirin..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none"
                />
              </div>

              {/* Allergies (Optional) */}
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1 flex items-center justify-between">
                  <span>Known Allergies If Any</span>
                  <span className="text-[10px] text-slate-400 font-normal">Optional</span>
                </label>
                <input
                  type="text"
                  value={allergies}
                  onChange={(e) => setAllergies(e.target.value)}
                  placeholder="E.g., Penicillin, Sulfa drugs, Peanuts, Latex..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none"
                />
              </div>

              {/* Informative Note */}
              <div className="p-3.5 rounded-2xl bg-health-50/70 border border-health-200/80 text-xs text-health-800 flex items-start gap-2.5">
                <Info className="w-4 h-4 text-health-600 shrink-0 mt-0.5" />
                <span>
                  All information is evaluated locally and confidentially for medical awareness and decision support. None of your data is used for third-party advertising.
                </span>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 flex justify-end">
              <button
                type="button"
                onClick={handleNextStep}
                className="px-6 py-2.5 rounded-xl bg-health-600 hover:bg-health-700 text-white font-bold text-sm shadow-md transition-all flex items-center gap-2"
              >
                Continue to Problem Description <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* ============================================================= */}
        {/* STEP 2: DESCRIBE YOUR PROBLEM (Natural Language Intake)       */}
        {/* ============================================================= */}
        {step === 2 && (
          <div className="max-w-2xl mx-auto bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200/90 animate-in fade-in space-y-6">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-health-600">STEP 2 OF 4</span>
              <h2 className="text-xl font-bold text-slate-900 mt-0.5">Describe What You're Experiencing</h2>
              <p className="text-xs text-slate-500 mt-1">
                Tell us about your problem in your own words. Our offline clinical parser will help identify your symptoms automatically.
              </p>
            </div>

            {/* Prompt Guides */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80">
              <span className="text-[11px] font-bold text-slate-600 uppercase tracking-wider block mb-2">
                Helpful details you can include:
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs text-slate-600">
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-medium">📍 Where it started</div>
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-medium">⏱ When it started</div>
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-medium">📈 How it changed</div>
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-medium">⚡ What it feels like</div>
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-medium">🔄 Better or worse</div>
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 font-medium">🩺 Other symptoms</div>
              </div>
            </div>

            {/* Large Text Area */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Your Health Complaint Description
              </label>
              <textarea
                rows="5"
                value={problemDescription}
                onChange={(e) => {
                  setProblemDescription(e.target.value);
                  setNlpApplied(false);
                }}
                placeholder="Tell us what you're experiencing in your own words. For example: I've had a red, itchy patch on my arm for three days and it seems to be getting larger, with mild fever and shivering."
                className="w-full px-4 py-3 rounded-2xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none leading-relaxed"
              />
            </div>

            {/* Instant Deterministic NLP Extractor Action */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <button
                type="button"
                onClick={handleExtractNlp}
                disabled={nlpLoading || !problemDescription.trim()}
                className="px-4 py-2 rounded-xl bg-tealAccent-50 hover:bg-tealAccent-100 text-tealAccent-900 border border-tealAccent-300 text-xs font-bold transition-colors flex items-center gap-2 self-start disabled:opacity-50"
              >
                <Sparkles className="w-4 h-4 text-tealAccent-600" />
                {nlpLoading ? 'Analyzing Text...' : 'Analyze Description Signals'}
              </button>

              <span className="text-[11px] text-slate-400">
                100% Offline Local Clinical Parser (No external LLM)
              </span>
            </div>

            {/* NLP Extraction Feedback Banner */}
            {nlpExtracted && (
              <div className="p-4 rounded-2xl bg-gradient-to-br from-health-50/70 to-tealAccent-50/50 border border-health-200 space-y-2 text-xs">
                <div className="flex items-center gap-1.5 font-bold text-health-900">
                  <CheckCircle2 className="w-4 h-4 text-health-600" />
                  <span>Clinical Signals Extracted From Your Description</span>
                </div>

                <div className="space-y-1.5 text-slate-700">
                  {nlpExtracted.extracted_symptoms_display?.length > 0 ? (
                    <div>
                      <span className="font-semibold text-slate-800">Identified Symptoms: </span>
                      <div className="inline-flex flex-wrap gap-1 mt-1">
                        {nlpExtracted.extracted_symptoms_display.map((s) => (
                          <span key={s} className="px-2.5 py-0.5 rounded-lg bg-white border border-health-300 text-health-900 font-bold text-xs">
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="text-slate-500">No specific clinical symptoms detected directly. You can select them manually in the next step.</div>
                  )}

                  <div className="flex flex-wrap gap-4 pt-1 text-[11px] text-slate-600">
                    <span><strong>Duration Cue:</strong> {nlpExtracted.duration}</span>
                    <span><strong>Severity Cue:</strong> {nlpExtracted.severity}</span>
                    {nlpExtracted.locations?.length > 0 && (
                      <span><strong>Locations:</strong> {nlpExtracted.locations.join(', ')}</span>
                    )}
                  </div>

                  {nlpExtracted.has_visual_mention && (
                    <div className="mt-1 pt-1.5 border-t border-health-200/60 text-tealAccent-900 font-semibold flex items-center gap-1.5">
                      <Eye className="w-3.5 h-3.5 text-tealAccent-700" />
                      <span>Visual complaint identified (Photo upload will be available in Step 4).</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Navigation */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors flex items-center gap-1.5"
              >
                <ArrowLeft className="w-3.5 h-3.5" /> Previous
              </button>

              <button
                type="button"
                onClick={handleNextStep}
                className="px-6 py-2.5 rounded-xl bg-health-600 hover:bg-health-700 text-white font-bold text-sm shadow-md transition-all flex items-center gap-2"
              >
                Continue to Symptoms & Parameters <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* ============================================================= */}
        {/* STEP 3: SYMPTOMS & DYNAMIC PARAMETERS                        */}
        {/* ============================================================= */}
        {step === 3 && (
          <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200/90 animate-in fade-in space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-health-600">STEP 3 OF 4</span>
                <h2 className="text-xl font-bold text-slate-900 mt-0.5">Symptoms & Specific Parameters</h2>
                <p className="text-xs text-slate-500 mt-1">
                  Select and refine your symptoms. Each selected symptom asks relevant follow-up questions tailored to your complaint.
                </p>
              </div>

              {/* Selected Count Badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-health-50 text-health-800 text-xs font-bold self-start sm:self-auto border border-health-200">
                <span>Selected Symptoms: {selectedSymptoms.length}</span>
              </div>
            </div>

            {/* Search Input */}
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search 132 clinical symptoms (e.g., Fever, Headache, Chest Pain, Cough, Skin Rash)..."
                className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-health-500 outline-none"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Selected Symptoms Chips */}
            {selectedSymptoms.length > 0 && (
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <div className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 flex items-center justify-between">
                  <span>Selected Symptoms ({selectedSymptoms.length})</span>
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedSymptoms([]);
                      setSymptomParams({});
                    }}
                    className="text-[11px] text-red-600 hover:underline font-semibold"
                  >
                    Clear All
                  </button>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {selectedSymptoms.map((sym) => (
                    <span
                      key={sym}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-health-600 text-white text-xs font-medium shadow-2xs"
                    >
                      {sym}
                      <button
                        type="button"
                        onClick={() => handleToggleSymptom(sym)}
                        className="hover:bg-health-700 rounded p-0.5"
                      >
                        <X className="w-3 h-3" />
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Category Filter Tabs */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-2 scrollbar-none">
              <button
                type="button"
                onClick={() => setActiveCategory('All')}
                className={`px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-colors ${
                  activeCategory === 'All'
                    ? 'bg-slate-900 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                All Categories
              </button>
              {Object.keys(categories).map((cat) => (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setActiveCategory(cat)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-colors ${
                    activeCategory === cat
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>

            {/* Symptoms Selection Grid (Accordion / Scroll) */}
            <div className="border border-slate-200/90 rounded-2xl p-2 max-h-56 overflow-y-auto">
              {loadingMetadata ? (
                <div className="py-8 text-center text-xs text-slate-400">Loading clinical catalog...</div>
              ) : filteredSymptoms.length === 0 ? (
                <div className="py-8 text-center text-xs text-slate-500">No symptoms found for "{searchQuery}".</div>
              ) : (
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-1.5">
                  {filteredSymptoms.map((sym) => {
                    const isSelected = selectedSymptoms.includes(sym);
                    return (
                      <button
                        key={sym}
                        type="button"
                        onClick={() => handleToggleSymptom(sym)}
                        className={`p-2 rounded-xl text-xs text-left font-medium transition-all flex items-start justify-between gap-1.5 ${
                          isSelected
                            ? 'bg-health-50 border border-health-400 text-health-900 shadow-2xs font-semibold'
                            : 'bg-slate-50/70 border border-slate-200/70 text-slate-700 hover:bg-slate-100'
                        }`}
                      >
                        <span className="leading-snug">{sym}</span>
                        {isSelected ? (
                          <Check className="w-3.5 h-3.5 text-health-600 shrink-0 mt-0.5" />
                        ) : (
                          <span className="w-3.5 h-3.5 rounded-full border border-slate-300 shrink-0 mt-0.5" />
                        )}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            {/* ========================================================= */}
            {/* DYNAMIC SYMPTOM-SPECIFIC PARAMETER CARDS                 */}
            {/* ========================================================= */}
            {selectedSymptoms.length > 0 && (
              <div className="space-y-4 pt-4 border-t border-slate-200">
                <div className="flex items-center gap-2">
                  <Sliders className="w-4 h-4 text-health-600" />
                  <h3 className="text-base font-bold text-slate-900">
                    Tell us more about each symptom
                  </h3>
                </div>
                <p className="text-xs text-slate-500">
                  Adaptive parameters tailored to your specific complaints. Answering these questions sharpens our clinical risk stratification.
                </p>

                <div className="space-y-4">
                  {selectedSymptoms.map((sym) => {
                    const cleanKey = sym.toLowerCase().replace(/ /g, '_');
                    // Find schema
                    const schema = paramSchemas[cleanKey] || paramSchemas[cleanKey.replace(/fever/g, 'high_fever')] || {
                      symptom: cleanKey,
                      title: sym,
                      parameters: [
                        { name: 'duration', label: `How long have you experienced ${sym}?`, type: 'select', options: ['Less than 24 hours', '1-2 days', '3-7 days', '1-2 weeks', 'More than 2 weeks'], default: '1-2 days' },
                        { name: 'impact', label: 'Impact on daily routine', type: 'select', options: ['Mild', 'Moderate', 'Severe'], default: 'Moderate' },
                        { name: 'severity', label: `${sym} Severity (1-10)`, type: 'slider', default: 5 }
                      ]
                    };

                    const currentValues = symptomParams[cleanKey] || {};

                    return (
                      <div key={sym} className="p-5 rounded-2xl bg-slate-50/90 border border-slate-200 space-y-4">
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <span className="w-2 h-2 rounded-full bg-health-600" />
                            {schema.title || sym}
                          </h4>
                          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                            Symptom Parameters
                          </span>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                          {schema.parameters?.map((param) => {
                            const val = currentValues[param.name] !== undefined ? currentValues[param.name] : param.default;
                            const err = validationErrors[`${cleanKey}.${param.name}`];

                            return (
                              <div key={param.name} className={`space-y-1 ${param.type === 'slider' || param.type === 'multi-select' ? 'sm:col-span-2' : ''}`}>
                                <label className="block text-xs font-semibold text-slate-700">
                                  {param.label}
                                </label>

                                {/* Parameter Type: NUMBER */}
                                {param.type === 'number' && (
                                  <div className="flex items-center gap-2">
                                    <input
                                      type="number"
                                      step={param.validation?.step || 0.1}
                                      min={param.validation?.min}
                                      max={param.validation?.max}
                                      value={val || ''}
                                      onChange={(e) => handleParamChange(cleanKey, param.name, parseFloat(e.target.value))}
                                      className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs text-slate-900 focus:ring-2 focus:ring-health-500 outline-none bg-white"
                                    />
                                    {param.unit && (
                                      <span className="text-xs font-bold text-slate-600 bg-slate-200 px-2.5 py-2 rounded-xl">
                                        {param.unit}
                                      </span>
                                    )}
                                  </div>
                                )}

                                {/* Parameter Type: SELECT */}
                                {param.type === 'select' && (
                                  <select
                                    value={val || ''}
                                    onChange={(e) => handleParamChange(cleanKey, param.name, e.target.value)}
                                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs text-slate-900 focus:ring-2 focus:ring-health-500 outline-none bg-white"
                                  >
                                    {param.options?.map((opt) => (
                                      <option key={opt} value={opt}>{opt}</option>
                                    ))}
                                  </select>
                                )}

                                {/* Parameter Type: MULTI-SELECT */}
                                {param.type === 'multi-select' && (
                                  <div className="flex flex-wrap gap-1.5 pt-1">
                                    {param.options?.map((opt) => {
                                      const isChecked = Array.isArray(val) && val.includes(opt);
                                      return (
                                        <button
                                          key={opt}
                                          type="button"
                                          onClick={() => {
                                            const currentList = Array.isArray(val) ? val : [];
                                            const nextList = isChecked
                                              ? currentList.filter(item => item !== opt)
                                              : [...currentList, opt];
                                            handleParamChange(cleanKey, param.name, nextList);
                                          }}
                                          className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                                            isChecked
                                              ? 'bg-health-600 text-white shadow-2xs font-semibold'
                                              : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                                          }`}
                                        >
                                          {opt}
                                        </button>
                                      );
                                    })}
                                  </div>
                                )}

                                {/* Parameter Type: BOOLEAN */}
                                {param.type === 'boolean' && (
                                  <div className="flex items-center gap-2 pt-0.5">
                                    <button
                                      type="button"
                                      onClick={() => handleParamChange(cleanKey, param.name, true)}
                                      className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                                        val === true
                                          ? 'bg-health-600 text-white border-health-600 shadow-2xs'
                                          : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                                      }`}
                                    >
                                      Yes
                                    </button>
                                    <button
                                      type="button"
                                      onClick={() => handleParamChange(cleanKey, param.name, false)}
                                      className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition-all ${
                                        val === false
                                          ? 'bg-slate-800 text-white border-slate-800 shadow-2xs'
                                          : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                                      }`}
                                    >
                                      No
                                    </button>
                                  </div>
                                )}

                                {/* Parameter Type: SLIDER */}
                                {param.type === 'slider' && (
                                  <div className="space-y-1 pt-1">
                                    <div className="flex items-center justify-between text-xs text-slate-500 font-semibold">
                                      <span>Mild (1)</span>
                                      <span className="text-health-700 font-extrabold text-sm">{val || 5} / 10</span>
                                      <span>Severe (10)</span>
                                    </div>
                                    <input
                                      type="range"
                                      min={param.validation?.min || 1}
                                      max={param.validation?.max || 10}
                                      step={1}
                                      value={val || 5}
                                      onChange={(e) => handleParamChange(cleanKey, param.name, parseInt(e.target.value))}
                                      className="w-full accent-health-600 cursor-pointer"
                                    />
                                  </div>
                                )}

                                {/* Validation error message */}
                                {err && <p className="text-[11px] text-red-600 font-medium">{err}</p>}
                                {param.help && <p className="text-[10px] text-slate-400">{param.help}</p>}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Navigation */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <button
                type="button"
                onClick={() => setStep(2)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors flex items-center gap-1.5"
              >
                <ArrowLeft className="w-3.5 h-3.5" /> Previous
              </button>

              <button
                type="button"
                onClick={handleNextStep}
                className="px-6 py-2.5 rounded-xl bg-health-600 hover:bg-health-700 text-white font-bold text-sm shadow-md transition-all flex items-center gap-2"
              >
                Continue to Photo & Review <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* ============================================================= */}
        {/* STEP 4: OPTIONAL IMAGE UPLOAD & INTAKE REVIEW                 */}
        {/* ============================================================= */}
        {step === 4 && (
          <div className="max-w-2xl mx-auto bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-slate-200/90 animate-in fade-in space-y-6">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-health-600">STEP 4 OF 4</span>
              <h2 className="text-xl font-bold text-slate-900 mt-0.5">
                {hasVisualSymptom ? 'Add a Photo of the Affected Area (Optional)' : 'Optional Photo & Final Review'}
              </h2>
              <p className="text-xs text-slate-500 mt-1">
                {hasVisualSymptom 
                  ? 'Your reported complaints include visual skin or superficial indicators. Adding a clear photo helps provide context for your assessment.'
                  : 'If you have any visual changes (rash, swelling, wound), you can attach a photo. Otherwise, review your details below and analyze.'}
              </p>
            </div>

            {/* Visual Highlight Banner if applicable */}
            {hasVisualSymptom && (
              <div className="p-3.5 rounded-2xl bg-tealAccent-50/70 border border-tealAccent-200 text-xs text-tealAccent-950 flex items-start gap-2.5">
                <Eye className="w-4 h-4 text-tealAccent-600 shrink-0 mt-0.5" />
                <div>
                  <strong className="block mb-0.5 font-bold">Visual Problem Detected</strong>
                  <span>
                    A well-lit photo of the rash, redness, or lesion assists specialist evaluation. Photo upload is completely optional.
                  </span>
                </div>
              </div>
            )}

            {/* Secure Image Uploader Component */}
            <div className="border-2 border-dashed border-slate-300 rounded-3xl p-6 text-center hover:border-health-400 transition-all bg-slate-50/60">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleImageChange}
                className="hidden"
                id="medical-image-upload"
              />

              {!imagePreview ? (
                <div className="space-y-3">
                  <div className="w-14 h-14 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center justify-center mx-auto text-slate-400">
                    <Camera className="w-7 h-7 text-health-600" />
                  </div>
                  <div>
                    <label
                      htmlFor="medical-image-upload"
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-health-600 hover:bg-health-700 text-white font-bold text-xs cursor-pointer shadow-sm transition-all"
                    >
                      <Upload className="w-3.5 h-3.5" /> Upload or Take Photo
                    </label>
                    <p className="text-[11px] text-slate-500 mt-2">
                      Supported: JPG, JPEG, PNG, WEBP (Max 5 MB)
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="relative inline-block">
                    <img
                      src={imagePreview}
                      alt="Uploaded symptom preview"
                      className="max-h-60 max-w-full rounded-2xl object-cover border border-slate-200 shadow-sm mx-auto"
                    />
                    <button
                      type="button"
                      onClick={handleRemoveImage}
                      className="absolute -top-2 -right-2 p-1.5 rounded-full bg-red-600 text-white shadow-md hover:bg-red-700 transition-colors"
                      title="Remove image"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <div className="flex items-center justify-center gap-3">
                    <label
                      htmlFor="medical-image-upload"
                      className="px-3 py-1.5 rounded-xl bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold text-xs cursor-pointer"
                    >
                      Replace Photo
                    </label>
                    <button
                      type="button"
                      onClick={handleRemoveImage}
                      className="px-3 py-1.5 rounded-xl text-red-600 hover:bg-red-50 font-semibold text-xs"
                    >
                      Remove
                    </button>
                  </div>

                  <div className="text-[11px] text-slate-500">
                    {imageFile?.name} ({(imageFile.size / 1024).toFixed(0)} KB)
                  </div>
                </div>
              )}

              {imageError && (
                <p className="text-xs text-red-600 font-medium mt-3">{imageError}</p>
              )}
            </div>

            {/* Privacy Guarantee Disclosure */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-1">
              <div className="flex items-center gap-1.5 font-bold text-slate-800">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span>Medical Image Privacy & Security</span>
              </div>
              <p className="text-[11px] leading-relaxed">
                Images are used only to assist this health assessment and are securely stored in protected medical directories. Images are never indexed by search engines or shared publicly.
              </p>
            </div>

            {/* Review Summary Card */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2.5 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-200">
                <span className="text-slate-500 font-semibold">Patient Demographics:</span>
                <span className="font-bold text-slate-900">{gender}, {age ? `${age} yrs` : 'Age unspecified'}</span>
              </div>
              {existingConditions.length > 0 && (
                <div className="flex justify-between py-1 border-b border-slate-200">
                  <span className="text-slate-500 font-semibold">Pre-existing Conditions:</span>
                  <span className="font-bold text-slate-900">{existingConditions.join(', ')}</span>
                </div>
              )}
              {problemDescription && (
                <div className="py-1 border-b border-slate-200">
                  <span className="text-slate-500 font-semibold block mb-0.5">Problem Description:</span>
                  <span className="text-slate-800 italic line-clamp-2">"{problemDescription}"</span>
                </div>
              )}
              <div>
                <span className="text-slate-500 font-semibold block mb-1">Reported Symptoms ({selectedSymptoms.length}):</span>
                <div className="flex flex-wrap gap-1">
                  {selectedSymptoms.map(s => (
                    <span key={s} className="px-2 py-0.5 rounded-md bg-white border border-slate-200 font-bold text-slate-800 text-[11px]">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Submit Action */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <button
                type="button"
                onClick={() => setStep(3)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition-colors flex items-center gap-1.5"
              >
                <ArrowLeft className="w-3.5 h-3.5" /> Edit Symptoms
              </button>

              <button
                type="button"
                onClick={handleSubmitAnalysis}
                className="px-8 py-3 rounded-xl bg-gradient-to-r from-health-600 to-tealAccent-600 hover:from-health-700 hover:to-tealAccent-700 text-white font-bold text-sm sm:text-base shadow-lg shadow-health-600/20 active:scale-95 transition-all flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4" />
                Analyze My Symptoms
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};

export default SymptomChecker;
