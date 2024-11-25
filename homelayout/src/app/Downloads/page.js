'use client'
export default function DownloadPage() {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen text-black bg-white p-8">
        <h1 className="text-2xl font-bold mb-8">Description:</h1>
        <div className="w-64 h-48 bg-pink-300 mb-6"></div>
        <button className="px-6 py-2 bg-purple-900 text-white rounded-md shadow-lg hover:bg-purple-700">
          Download
        </button>
      </div>
    );
  }
  