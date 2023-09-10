'use client'

import React, { useState } from 'react';
import useSWR from 'swr';
import { getWorkflow } from '../services/backend';

type Message = {
  user: string;
  text: string;
};

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const { data, error } = useSWR("/workflow", getWorkflow);

  const handleSend = () => {
    setMessages([...messages, { user: 'User1', text: input }]);
    setInput('');
  };

  return (
    <div className="flex flex-col items-center p-4">
      <div className="overflow-auto h-64 w-64 border rounded-lg p-4 mb-4">
        {messages.map((message, index) => (
          <div key={index} className="mb-2">
            <strong>{message.user}: </strong>
            <span>{message.text}</span>
          </div>
        ))}
      </div>
      <div className="flex items-center">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow rounded-l-lg p-4 border-t mr-0 border-b border-l text-gray-800 border-gray-200 bg-white"
          placeholder="Write something..."
        />
        <button
          onClick={handleSend}
          className="px-8 rounded-r-lg bg-blue-500 text-white font-bold p-4 uppercase border-blue-500 border-t border-b border-r"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;