import React from 'react';
import { NotificationToast } from './NotificationToast';

interface NotificationListProps {
  notifications: Array<{ id: string; message: string }>;
  onDismiss: (id: string) => void;
}

export function NotificationList({ notifications, onDismiss }: NotificationListProps) {
  return (
    <div className="fixed bottom-4 right-4 space-y-2">
      {notifications.map(({ id, message }) => (
        <NotificationToast
          key={id}
          message={message}
          onClose={() => onDismiss(id)}
        />
      ))}
    </div>
  );
}