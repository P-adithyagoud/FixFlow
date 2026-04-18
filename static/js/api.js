/**
 * Incident API Service
 * Handles communication with the backend for incident analysis.
 */
const IncidentAPI = {
    /**
     * Send incident text to backend for analysis.
     * @param {string} text - The incident description or logs.
     * @returns {Promise<Object>} - The analysis result.
     */
    async analyze(text) {
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ incident: text })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Analysis failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};
