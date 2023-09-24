'use client'

import React, { useState, useEffect, useCallback } from 'react';
import { getWorkflowSWR, sendMessage } from '../services/backend';

type LogMessage = {
  text: string;
};

type Message = {
  source: string;
  message: LogMessage
};

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  const { data, error } = getWorkflowSWR()

  useEffect(() => {
    if (data) {
      // TODO: Get the last completed step rather than the last step, which may be in progress
      const lastStepIndex = data.workflow.length - 1;
      setMessages(data.workflow[lastStepIndex].log);
    }
  }, [data]);

  const handleSend = async () => {
    const userInput = { source: 'user', message: { text: input } };
    const agentInput = { source: 'agent', message: { text: '' } };
    setMessages([...messages, userInput, agentInput]);
    setInput('');

    const reader = await sendMessage(input);

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      setMessages(prevMessages => {
        const lastMessage = prevMessages[prevMessages.length - 1];
        lastMessage.message.text += new TextDecoder().decode(value);
        return [...prevMessages];
      });
    }
  };

  return (
    <div className="flex flex-col h-full items-center p-4">
      <div className="overflow-auto h-full w-1/2 border rounded-lg p-4 mb-4">
        {messages.map((message, index) => (
          <div key={index} className="mb-2">
            <strong>{message.source}: </strong>
            <span>{message.message.text}</span>
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
