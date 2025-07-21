import React from 'react';

interface AvatarDisplayProps {
  status: 'idle' | 'listening' | 'thinking' | 'speaking';
  imageUrl?: string;
}

export const AvatarDisplay: React.FC<AvatarDisplayProps> = ({ 
  status, 
  imageUrl = '/avatar.png' 
}) => {
  const getStatusText = () => {
    switch (status) {
      case 'listening':
        return '聞いています...';
      case 'thinking':
        return '考えています...';
      case 'speaking':
        return '話しています...';
      default:
        return '待機中';
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'listening':
        return '#ff9800';
      case 'thinking':
        return '#2196f3';
      case 'speaking':
        return '#4caf50';
      default:
        return '#9e9e9e';
    }
  };

  return (
    <div className="avatar-display" style={{
      textAlign: 'center',
      marginBottom: '30px'
    }}>
      <div style={{
        position: 'relative',
        display: 'inline-block'
      }}>
        <img
          src={imageUrl}
          alt="AI Assistant Avatar"
          style={{
            width: '200px',
            height: '200px',
            borderRadius: '50%',
            objectFit: 'cover',
            border: `4px solid ${getStatusColor()}`,
            transition: 'border-color 0.3s ease'
          }}
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiByeD0iMTAwIiBmaWxsPSIjRTBFMEUwIi8+CjxjaXJjbGUgY3g9IjEwMCIgY3k9IjgwIiByPSIzMCIgZmlsbD0iIzlFOUU5RSIvPgo8cGF0aCBkPSJNNjAgMTUwQzYwIDEzMCA4MCAxMTAgMTAwIDExMEMxMjAgMTEwIDE0MCAxMzAgMTQwIDE1MEg2MFoiIGZpbGw9IiM5RTlFOUUiLz4KPC9zdmc+';
          }}
        />
        <div style={{
          position: 'absolute',
          bottom: '10px',
          left: '50%',
          transform: 'translateX(-50%)',
          backgroundColor: getStatusColor(),
          color: 'white',
          padding: '5px 15px',
          borderRadius: '20px',
          fontSize: '14px',
          whiteSpace: 'nowrap'
        }}>
          {getStatusText()}
        </div>
      </div>
    </div>
  );
};