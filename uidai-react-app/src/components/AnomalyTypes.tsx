import React from 'react';

const ANOMALY_DETAILS = [
  {
    title: "Phantom Village (Fake ID Ring)",
    criticality: "CRITICAL",
    color: "#EF4444",
    description: "Identifies clusters of new adult enrolments ('age_18_greater') that statistically exceed district norms. This anomaly detects 'ghost' centers creating fake IDs for non-existent residents, often indicated by a sudden spike in registrations in areas with stable populations."
  },
  {
    title: "Update Mill (Unauthorized Bulk Operations)",
    criticality: "HIGH",
    color: "#F59E0B",
    description: "Flags districts with an abnormally high Z-Score for demographic updates ('demo_age_17_'). This pattern suggests unauthorized bulk operations, where operators might be changing address or mobile details for large groups of people simultaneously, potentially for election fraud or benefit manipulation."
  },
  {
    title: "Biometric Bypass (Incomplete Verification)",
    criticality: "HIGH",
    color: "#8B5CF6",
    description: "Detects centers performing high volumes of demographic updates without corresponding biometric validations. Calculated using a risk ratio (Demo Updates / Bio Updates). This indicates operators are bypassing mandatory security protocols to update profiles without the resident being physically present."
  },
  {
    title: "Scholarship Ghost (Child Age Mismatch)",
    criticality: "MEDIUM",
    color: "#3B82F6",
    description: "Identifies discrepancies where child demographic updates (Name/DOB) significantly outnumber biometric updates. This suggests age manipulation to keep children eligible for scholarships or benefits even after they have aged out, or to create 'ghost' child beneficiaries."
  },
  {
    title: "Bot Operator (Pattern Fabrication)",
    criticality: "MEDIUM",
    color: "#10B981",
    description: "Uses Benford's Law and pattern analysis to find enrolment counts that are suspiciously 'clean' (e.g., ending in 0 or 5 consistently). A high percentage (>80%) of round numbers indicates data is being fabricated by bots or lazy operators rather than reflecting natural human footfall."
  },
  {
    title: "Sunday Shift (Temporal Fraud)",
    criticality: "HIGH",
    color: "#EC4899",
    description: "Flags significant enrolment activity on Sundays or public holidays when official centers are mandated to be closed. This temporal anomaly is a strong indicator of unauthorized 'black market' camps operating off the grid to process illegal or fraudulent registrations."
  }
];

const AnomalyTypes: React.FC = () => {
  return (
    <div className="card" style={{ height: '100%', padding: '32px', overflowY: 'auto' }}>
      <p style={{ color: '#6B7280', marginBottom: '32px' }}>
        Detailed breakdown of the 6 fraud detection algorithms used by UIDAI Sentinel.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
        {ANOMALY_DETAILS.map((item) => (
          <div key={item.title} style={{ 
            border: '1px solid #E5E7EB', borderRadius: '12px', padding: '24px',
            backgroundColor: '#FAFAFA', position: 'relative', overflow: 'hidden' 
          }}>
            {/* Colored Accent Line */}
            <div style={{ 
              position: 'absolute', left: 0, top: 0, bottom: 0, width: '6px', 
              backgroundColor: item.color 
            }} />
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
              <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#111827', margin: 0 }}>
                {item.title}
              </h3>
              <span style={{ 
                backgroundColor: item.criticality === 'CRITICAL' ? '#FEF2F2' : item.criticality === 'HIGH' ? '#FFFBEB' : '#ECFDF5',
                color: item.criticality === 'CRITICAL' ? '#EF4444' : item.criticality === 'HIGH' ? '#F59E0B' : '#10B981',
                padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 700, border: `1px solid ${item.color}40`
              }}>
                {item.criticality}
              </span>
            </div>
            
            <p style={{ fontSize: '15px', lineHeight: '1.6', color: '#4B5563' }}>
              {item.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnomalyTypes;