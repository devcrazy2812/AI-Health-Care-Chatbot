import React, { useState } from 'react';

const initialFormData = {
  age: 45, sex: 1, cp: 1, trestbps: 120, chol: 200, fbs: 0,
  restecg: 1, thalach: 150, exang: 0, oldpeak: 1.0, slope: 1, ca: 0, thal: 2
};

const SymptomCard = () => {
  const [formData, setFormData] = useState(initialFormData);
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/predict/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  if (prediction) {
    const riskClass = prediction.risk_level.toLowerCase().replace(' ', '-');
    return (
      <div className={`prediction-result ${riskClass}`}>
        <h4>Analysis Complete: {prediction.risk_level}</h4>
        <p style={{marginTop: '8px', fontSize: '14px', lineHeight: '1.4'}}>{prediction.recommendation}</p>
        <p style={{marginTop: '12px', fontSize: '12px', opacity: 0.7}}>
          Confidence: {(prediction.probability * 100).toFixed(1)}% | Internal ML Model
        </p>
      </div>
    );
  }

  return (
    <div className="symptom-form">
      <div className="form-header">
        <h3>Heart Disease Risk Assessment</h3>
        <p>Please enter your clinical details for an ML-based prediction.</p>
      </div>
      
      <div className="form-grid">
        <div className="form-group">
          <label>Age</label>
          <input type="number" name="age" value={formData.age} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Sex (1:M, 0:F)</label>
          <select name="sex" value={formData.sex} onChange={handleChange}>
            <option value={1}>Male</option>
            <option value={0}>Female</option>
          </select>
        </div>
        <div className="form-group">
          <label>Chest Pain (0-3)</label>
          <select name="cp" value={formData.cp} onChange={handleChange}>
            <option value={0}>0 - Typical Angina</option>
            <option value={1}>1 - Atypical Angina</option>
            <option value={2}>2 - Non-anginal Pain</option>
            <option value={3}>3 - Asymptomatic</option>
          </select>
        </div>
        <div className="form-group">
          <label>Resting BP (mm Hg)</label>
          <input type="number" name="trestbps" value={formData.trestbps} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Cholesterol (mg/dl)</label>
          <input type="number" name="chol" value={formData.chol} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Max Heart Rate</label>
          <input type="number" name="thalach" value={formData.thalach} onChange={handleChange} />
        </div>
      </div>
      
      <button onClick={handleSubmit} disabled={isLoading} className="submit-symptoms-btn">
        {isLoading ? 'Analyzing...' : 'Run Prediction Model'}
      </button>
    </div>
  );
};

export default SymptomCard;
