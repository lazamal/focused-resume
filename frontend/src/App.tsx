import React, { useState, type EventHandler } from "react";
import axios from "axios";
import { Upload, Link as LinkIcon, FileText, Send } from "lucide-react";
import { Toaster, toast } from "sonner";
import { SkillCard } from "../components/SkillCard";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file || !url) {
      toast.error("Upload a file and a link to a job description");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("cv", file);
    formData.append("job_url", url);

    try {
      // כאן יקרה החיבור הממשי לשרת ה-Django שלך בעתיד
      // const response = await axios.post('http://localhost:8000/api/analyze', formData);

      toast.success("Analysis may take several seconds...");
    } catch (error) {
      toast.error("something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4">
      <Toaster position="top-center" />

      <header className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-2">
          Focused resume reviewer
        </h1>
        <p className="text-gray-600 text-3xl">Get Noticed</p>
      </header>

      <main className="w-full max-w-2xl bg-white rounded-2xl shadow-xl p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* שדה העלאת קובץ */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Resume (PDF)
            </label>
            <div className="flex items-center justify-center w-full">
              <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  {file ? (
                    <div className="flex items-center text-blue-600">
                      <FileText className="w-8 h-8 mr-2" />
                      <span className="font-medium">{file.name}</span>
                    </div>
                  ) : (
                    <>
                      <Upload className="w-8 h-8 text-gray-400 mb-2" />
                      <p className="text-sm text-gray-500">לחץ להעלאה</p>
                    </>
                  )}
                </div>
                <input
                  type="file"
                  className="hidden"
                  accept=".pdf"
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      setFile(e.target.files[0]);
                    }
                  }}
                />
              </label>
            </div>
          </div>

          {/* שדה לינק למשרה */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Job description link
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LinkIcon className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="url"
                className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 text-sm"
                placeholder="https://www.linkedin.com/jobs/..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
            </div>
          </div>

          {/* כפתור שליחה */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-white font-bold transition-all ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? (
              "מנתח נתונים..."
            ) : (
              <>
                נתח התאמה <Send className="w-4 h-4 ml-2" />
              </>
            )}
          </button>
        </form>
      </main>
      <div className="w-full  mt-10 max-w-2xl bg-white rounded-2xl shadow-xl p-8">
        <p className="text-center text-1xl font-medium text-gray-700">
          skill matched
        </p>
        <div className="mt-4 flex flex-row gap-3 flex-wrap">
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
        </div>
      </div>

      <div className="w-full  mt-10 max-w-2xl bg-white rounded-2xl shadow-xl p-8">
        <p className="text-center text-1xl  font-medium text-gray-700">
          skill gaps
        </p>
        <div className="mt-4 flex flex-row gap-3 flex-wrap">
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
          <SkillCard skillName="skill" />
        </div>
      </div>
    </div>
  );
}

export default App;
