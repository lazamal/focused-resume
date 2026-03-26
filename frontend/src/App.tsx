import React, { useState } from "react";
import axios from "axios";
import {
  Upload,
  Link as LinkIcon,
  FileText,
  Send,
  Link,
  AlignLeft,
} from "lucide-react";
import { Toaster, toast } from "sonner";
import { MissingSkillCard } from "./components/MissingSkillCard";
import { OverallMatchCard } from "./components/OverallMatchCard";
import { SkillDisplayCard } from "./components/SkillsDisplayCard";
import { MatchSkillCard } from "./components/MatchSkillCard";
import { SkillFooterCard } from "./components/SkillFooterCard";

import { SkeletonDemo } from "./components/SkeletonDemo";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [url, setUrl] = useState<string | null>("");
  const [textareaInput, setTextAreaInput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>();
  const [inputMode, setInputMode] = useState<"link" | "text">("link");

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    const maxFileSize = 5 * 1024 * 1024; // 5MB

    // 1. Client-side Validation
    if (!file) {
      toast.error("Please upload your resume.");
      return;
    }

    if (!url && !textareaInput) {
      toast.error("Please provide a job link or paste the description.");
      return;
    }

    if (file.size > maxFileSize) {
      toast.error("File is too big. Please upload a file below 5MB.");
      return;
    }

    // 2. Prepare UI State

    setResults(undefined);
    setLoading(true);

    // פונקציית עזר לקריאת הקובץ כ-ArrayBuffer (בינארי)
    const readFileAsArrayBuffer = (fileToRead: File): Promise<ArrayBuffer> => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as ArrayBuffer);
        reader.onerror = reject;
        reader.readAsArrayBuffer(fileToRead); // זה השלב שבו הדרוג מוריד את הקובץ
      });
    };

    let fileContent: Blob;
    try {
      // נציג הודעה ספציפית אם זה לוקח זמן
      toast.info("Reading resume from cloud storage...");
      const arrayBuffer = await readFileAsArrayBuffer(file); // ניצור Blob חדש ומלא מהתוכן שקראנו מהזיכרון
      fileContent = new Blob([arrayBuffer], { type: file.type });
    } catch (error) {
      console.error("Error reading file:", error);
      toast.error(
        "Could not read the Drive file. Please try downloading it locally first.",
      );
      setLoading(false);
      return; // עוצרים כאן אם אי אפשר לקרוא את הקובץ
    }

    // 3. Construct Multipart Form Data
    // This matches the 'decoder.MultipartDecoder' logic in your Python post() method
    const formData = new FormData();
    toast.success("Analysis may take several seconds...");
    formData.append("file", fileContent, file.name); // Becomes data['file_content'] on backend

    if (url) {
      formData.append("url", url); // Becomes data['url'] on backend
    }

    if (textareaInput) {
      formData.append("textarea", textareaInput); // Becomes data['textarea'] on backend
    }

    try {
      const response = await axios.post(
        "https://xwgr5b3vpcrh6whmpw676x5vve0bluls.lambda-url.eu-central-1.on.aws/",
        formData,
      );

      console.log("Backend Response:", response.data);
      setResults(response.data);
      toast.success("Analysis complete!");
    } catch (error: any) {
      console.error("Submission error:", error);
      const serverError = error.response?.data?.error;

      if (serverError) {
        toast.error(serverError);
      } else if (error.response?.status === 408) {
        toast.error(
          "The request timed out. LinkedIn might be blocking the scraper.",
        );
      } else if (error.response?.status === 429) {
        toast.error("Too many requests. Please wait a moment.");
      } else {
        toast.error("Something went wrong with the server.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4">
      <Toaster position="top-center" />

      <header className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-2">
          Stop Guessing.{" "}
          <span className="text-orange-400">Start Matching.</span>
        </h1>
        <p className="text-gray-500 text-lg">
          Know which skills you're missing before you apply
        </p>
      </header>

      <main className="w-full max-w-3xl bg-white rounded-2xl shadow-xl p-8">
        <form
          onSubmit={handleSubmit}
          className="space-y-6"
          encType="multipart/form-data"
        >
          {/* שדה העלאת קובץ */}
          <div className="space-y-2 bg">
            <div className="flex flex-row-reverse justify-end gap-2">
              <label className="block text-sm font-semibold text-gray-700">
                Resume (PDF)
              </label>
              <FileText className="w-4 h-4 text-orange-500" />
            </div>
            <div className="w-full bg-orange-100 border-2 border-dashed border-orange-200 rounded-xl p-2  from-orange-50 to-amber-50 hover:border-orange-300 transition-colors cursor-pointer group">
              <label className="">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  {file ? (
                    <div className="flex flex-row gap-3 items-center text-blue-600">
                      <div className="bg-white rounded-lg p-3 shadow-sm group-hover:shadow-md transition-shadow">
                        <FileText className="w-6 h-6 text-blue-500" />
                      </div>
                      <span className="font-medium text-blue-600">
                        {file.name}
                      </span>
                    </div>
                  ) : (
                    <>
                      <Upload className="w-6 h-6 text-orange-400" />
                      <p className=" text-gray-700">Upload</p>
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
            <div className="flex items-center justify-between mb-3">
              <div className="flex flex-row gap-2">
                <Link className="w-4 h-4 text-orange-500" />
                <label className="text-sm font-semibold text-gray-700  ">
                  Job description link
                </label>
              </div>
              <div className="flex bg-gray-100 rounded-lg p-1">
                <button
                  type="button"
                  onClick={() => setInputMode("link")}
                  className={`px-4 py-2 rounded-md text-sm font-semibold transition-all ${
                    inputMode === "link"
                      ? "bg-white text-blue-600 shadow-sm"
                      : "text-gray-600 hover:text-gray-900"
                  }`}
                >
                  {inputMode === "link" ? (
                    <Link className="w-4 h-4 inline mr-1 text-orange-500" />
                  ) : (
                    <Link className="w-4 h-4 inline mr-1" />
                  )}
                  Link
                </button>
                <button
                  type="button"
                  onClick={() => setInputMode("text")}
                  className={`px-4 py-2 rounded-md text-sm font-semibold transition-all ${
                    inputMode === "text"
                      ? "bg-white text-blue-600 shadow-sm"
                      : "text-gray-600 hover:text-gray-900"
                  }`}
                >
                  {inputMode === "text" ? (
                    <AlignLeft className="w-4 h-4 inline mr-1 text-orange-500" />
                  ) : (
                    <AlignLeft className="w-4 h-4 inline mr-1" />
                  )}
                  Text
                </button>
              </div>
            </div>

            {inputMode === "link" ? (
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LinkIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="url"
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 text-sm"
                  placeholder="https://www.linkedin.com/jobs/..."
                  value={url ?? ""}
                  onChange={(e) => {
                    setTextAreaInput(null);
                    setUrl(e.target.value);
                  }}
                  name="url"
                />
              </div>
            ) : (
              <div className="relative">
                <textarea
                  name="textarea"
                  rows={8}
                  className="w-full px-4 py-4 border-2 border-gray-200 rounded-xl focus:border-orange-400 focus:outline-none focus:ring-4 focus:ring-orange-100 transition-all bg-gray-50 resize-none"
                  placeholder="Paste job description text here..."
                  value={textareaInput ?? ""}
                  onChange={(e) => {
                    setUrl(null);
                    setTextAreaInput(e.target.value);
                  }}
                />
              </div>
            )}
          </div>

          {/* כפתור שליחה */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-white  transition-all ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? (
              "Analyzing..."
            ) : (
              <>
                Analyze My Resume
                <Send className="w-4 h-4 ml-2" />
              </>
            )}
          </button>
        </form>
      </main>

      {/* if no results and is loading show skeleton */}
      {/* if results and is not loading show interface */}
      {/*  if no results and is not loading show nothing */}
      {loading && !results ? (
        <SkeletonDemo />
      ) : results && !loading ? (
        <div className="w-full max-w-3xl flex flex-col items-stretch">
          <OverallMatchCard
            score={results?.overall_score}
            numberOfMatchedSkills={results?.number_of_matched_skills}
            totalSkillsForJob={results?.total_skills_for_job}
          />
          <div className="flex flex-row items-stretch">
            <div className="flex-1 basis-0 flex flex-col">
              <SkillDisplayCard
                headline="Matched skills"
                skillsToShow={results.matched_skills}
                SkillCardToUse={MatchSkillCard}
              />
            </div>

            <div className="flex-1 basis-0 flex flex-col ">
              <SkillDisplayCard
                headline="Skills to learn"
                skillsToShow={results.skills_to_learn}
                SkillCardToUse={MissingSkillCard}
              />
            </div>
          </div>
          <SkillFooterCard
            score={results?.overall_score}
            numberOfMatchedSkills={results?.number_of_matched_skills}
            numberOfSkillsToLearn={results?.number_of_skills_to_learn}
          />
        </div>
      ) : null}
    </div>
  );
}

export default App;
