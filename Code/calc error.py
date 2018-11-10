import numpy as np

def calculate_error(m_rawData):
    error = 0
    
    m_minLineLengthInSeconds = 0.0

    m_maxLineLengthInSeconds = 1.5

    m_maxValueDiff = 0.5

    m_maxError = 1.5
    
    m_sampleTime=1.5

    if (m_rawData.size() == 0):
        return error

    eps = 1e-10
    N = m_rawData.size()

    if (m_maxLineLengthInSeconds > 0 and ( m_rawData.size() * m_sampleTime) > m_maxLineLengthInSeconds):
        return m_maxError + eps
	
    if (m_minLineLengthInSeconds > 0 and ( m_rawData.size() * m_sampleTime) < m_minLineLengthInSeconds):
        return eps

    a = m_rawData[0]
    b = m_rawData[N]
    h = (b-a)/(N - 1)

    if (m_maxValueDiff > 0 and np.abs(a - b) > m_maxValueDiff):
        return (m_maxError + eps)

    if (N - 1 == 0):
        return error		

    val = a
    
    for i in range(0,N):
        diff = m_rawData[i] - val
        val = val + h
        error = error + diff * diff
    return error