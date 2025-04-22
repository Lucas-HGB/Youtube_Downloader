import React from 'react';

interface NotificationToastProps {
  message: string;
  onClose: () => void;
}

export function NotificationToast({ message, onClose }: NotificationToastProps) {
  return (
    <div className="fixed bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 max-w-sm animate-slide-up">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-800">{message}</p>
        <button
          onClick={onClose}
          className="ml-4 text-gray-400 hover:text-gray-600"
        >
          ×
        </button>
      </div>
    </div>
  );
}