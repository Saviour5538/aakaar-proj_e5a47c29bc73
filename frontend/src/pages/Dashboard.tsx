import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { listDocuments as fetchDocuments, listConversations as fetchConversations } from '../api/client';
import { Document, Conversation } from '../types';
import { toast } from 'react-toastify';

const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [docsResponse, convResponse] = await Promise.all([
          fetchDocuments(),
          fetchConversations(),
        ]);
        setDocuments(docsResponse);
        setConversations(convResponse);
      } catch (err) {
        setError('Failed to load data. Please try again.');
        toast.error('Error fetching dashboard data.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleUploadClick = () => {
    navigate('/upload');
  };

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>
      {loading ? (
        <div className="text-center text-gray-600">Loading...</div>
      ) : error ? (
        <div className="text-center text-red-600">{error}</div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-700">Documents</h2>
              <p className="text-3xl font-bold text-gray-900">{documents.length}</p>
            </div>
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-700">Conversations</h2>
              <p className="text-3xl font-bold text-gray-900">{conversations.length}</p>
            </div>
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-700">Quick Actions</h2>
              <div className="mt-4">
                <button
                  onClick={handleUploadClick}
                  className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                >
                  Upload Document
                </button>
                <button
                  onClick={handleChatClick}
                  className="w-full mt-2 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
                >
                  Start Chat
                </button>
              </div>
            </div>
          </div>
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">Recent Documents</h2>
            {documents.length > 0 ? (
              <ul className="divide-y divide-gray-200">
                {documents.slice(0, 5).map((doc) => (
                  <li key={doc.id} className="py-2">
                    <span className="text-gray-800">{doc.name}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-600">No documents available.</p>
            )}
          </div>
          <div className="bg-white shadow rounded-lg p-6 mt-6">
            <h2 className="text-lg font-semibold text-gray-700 mb-4">Recent Conversations</h2>
            {conversations.length > 0 ? (
              <ul className="divide-y divide-gray-200">
                {conversations.slice(0, 5).map((conv) => (
                  <li key={conv.id} className="py-2">
                    <span className="text-gray-800">{conv.title}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-600">No conversations available.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;