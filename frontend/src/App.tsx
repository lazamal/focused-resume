import React, { useState } from "react";
import axios from "axios";
import { Upload, Link as LinkIcon, FileText, Send } from "lucide-react";
import { Toaster, toast } from "sonner";
import { MissingSkillCard } from "./components/MissingSkillCard";
import { OverallMatchCard } from "./components/OverallMatchCard";
import { SkillDisplayCard } from "./components/SkillsDisplayCard";
import { MatchSkillCard } from "./components/MatchSkillCard";
import { SkillFooterCard } from "./components/SkillFooterCard";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>();

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file || !url) {
      toast.error("Upload a file and a link to a job description");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("url", url);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      toast.success("Analysis may take several seconds...");
      console.log(response.data);
      setResults(response.data);
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
          Skill Gap
        </h1>
        <p className="text-gray-600 text-3xl">
          See what the recruiter sees before they do
        </p>
      </header>

      <main className="w-full max-w-2xl bg-white rounded-2xl shadow-xl p-8">
        <form
          onSubmit={handleSubmit}
          className="space-y-6"
          encType="multipart/form-data"
        >
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
                  name="file"
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
                name="url"
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
              "Analyzing..."
            ) : (
              <>
                Analyze <Send className="w-4 h-4 ml-2" />
              </>
            )}
          </button>
        </form>
      </main>
      <div className="w-full max-w-5xl flex flex-col items-stretch">
        <OverallMatchCard
          score={results?.overall_score}
          numberOfMatchedSkills={results?.number_of_matched_skills}
          totalSkillsForJob={results?.total_skills_for_job}
        />
        <div className="flex flex-row items-stretch">
          <div className="flex-1 basis-0 flex flex-col">
            {results?.matched_skills && (
              <SkillDisplayCard
                headline="Matched skills"
                skillsToShow={results.matched_skills}
                SkillCardToUse={MatchSkillCard}
              />
            )}
          </div>

          <div className="flex-1 basis-0 flex flex-col ">
            {results?.skills_to_learn && (
              <SkillDisplayCard
                headline="Skills to learn"
                skillsToShow={results.skills_to_learn}
                SkillCardToUse={MissingSkillCard}
              />
            )}
          </div>
        </div>
        <SkillFooterCard
          score={results?.overall_score}
          numberOfMatchedSkills={results?.number_of_matched_skills}
          numberOfSkillsToLearn={results?.number_of_skills_to_learn}
        />
      </div>
    </div>
  );
}

export default App;
